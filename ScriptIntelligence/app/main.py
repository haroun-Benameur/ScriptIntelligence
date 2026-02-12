# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

from agents.fsd_agent import generate_tests_with_llm
from services.drift_service import (
    analyze_fsd,
    read_fsd_text,
    load_pending_state,
    commit_pending_state,
)

app = FastAPI()

TESTS_FILE = "tests/generated_tests.json"


class RegenerateRequest(BaseModel):
    confirm: bool


class TestCase(BaseModel):
    requirement_id: str
    test_name: str
    description: str
    inputs: Dict[str, Any]
    expected_output: str


def _load_tests() -> List[Dict[str, Any]]:
    if not os.path.exists(TESTS_FILE):
        return []
    with open(TESTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_tests(tests: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(TESTS_FILE), exist_ok=True)
    with open(TESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)


@app.get("/run-workflow")
def run_workflow():
    """
    Lit docs/FSD.md, détecte le drift, régénère uniquement les tests
    des exigences ajoutées/modifiées, génère les rapports MD.
    """
    fsd_content = read_fsd_text()
    drift_result = analyze_fsd(fsd_content, persist_pending=False)

    if not drift_result["drift_detected"]:
        return {"drift_detected": False, "message": "No changes detected in FSD."}

    changes = drift_result["changes"]
    new_requirements = drift_result["new_requirements"]
    added = changes.get("added", [])
    updated = changes.get("updated", [])
    removed = changes.get("removed", [])
    to_generate = added + updated

    existing_tests = _load_tests()
    ids_to_replace = {r["requirement_id"] for r in to_generate}
    ids_removed = {r["requirement_id"] for r in removed}
    filtered = [
        t
        for t in existing_tests
        if t.get("requirement_id") not in ids_to_replace | ids_removed
    ]

    new_tests: List[Dict[str, Any]] = []
    if to_generate:
        new_tests = generate_tests_with_llm(to_generate, fsd_content)

    all_tests = filtered + new_tests
    _save_tests(all_tests)
    commit_pending_state(fsd_content=fsd_content, new_requirements=new_requirements)

    from utils.report_generator import generate_test_generation_report, generate_drift_report

    report1_path = generate_test_generation_report(all_tests)
    report2_path = generate_drift_report(
        old_fsd=drift_result.get("old_fsd_content", ""),
        new_fsd=fsd_content,
        changes=changes,
        generated_tests=new_tests,
        old_requirements=drift_result.get("old_requirements"),
    )

    return {
        "drift_detected": True,
        "message": "FSD changed. Tests (added/updated) regenerated.",
        "details": {
            "status": "tests_generated",
            "requirements_count": len(new_requirements),
            "added": [r["requirement_id"] for r in added],
            "updated": [r["requirement_id"] for r in updated],
            "removed": [r["requirement_id"] for r in removed],
            "generated_tests": new_tests,
        },
        "reports": {
            "test_generation_report": report1_path,
            "drift_report": report2_path,
        },
    }


@app.get("/analyze-fsd")
def analyze_fsd_endpoint():
    """
    Lit docs/FSD.md, détecte le drift et stocke l'état pending.
    """
    fsd_content = read_fsd_text()
    result = analyze_fsd(fsd_content=fsd_content, persist_pending=True)
    return {"drift_detected": result["drift_detected"], "changes": result["changes"]}


@app.post("/regenerate-tests")
def regenerate_tests(request: RegenerateRequest):
    """
    Régénère UNIQUEMENT les tests pour les exigences ajoutées/modifiées
    détectées lors du dernier /analyze-fsd. Génère les rapports MD.
    """
    if not request.confirm:
        return {"status": "cancelled", "message": "Regeneration not confirmed."}

    pending = load_pending_state()
    if pending is None:
        raise HTTPException(
            status_code=400,
            detail="No pending FSD analysis to regenerate from. Call /analyze-fsd first.",
        )

    fsd_content = pending["fsd_content"]
    changes = pending["changes"]
    new_requirements = pending["new_requirements"]
    old_fsd = pending.get("old_fsd_content", "")
    old_requirements = pending.get("old_requirements", [])

    added = changes.get("added", [])
    updated = changes.get("updated", [])
    removed = changes.get("removed", [])
    to_generate = added + updated

    existing_tests = _load_tests()
    ids_to_replace = {r["requirement_id"] for r in to_generate}
    ids_removed = {r["requirement_id"] for r in removed}
    filtered = [
        t
        for t in existing_tests
        if t.get("requirement_id") not in ids_to_replace | ids_removed
    ]

    new_tests: List[Dict[str, Any]] = []
    if to_generate:
        new_tests = generate_tests_with_llm(to_generate, fsd_content)

    all_tests = filtered + new_tests
    _save_tests(all_tests)
    commit_pending_state(fsd_content=fsd_content, new_requirements=new_requirements)

    from utils.report_generator import generate_test_generation_report, generate_drift_report

    report1_path = generate_test_generation_report(all_tests)
    report2_path = generate_drift_report(
        old_fsd=old_fsd,
        new_fsd=fsd_content,
        changes=changes,
        generated_tests=new_tests,
        old_requirements=old_requirements,
    )

    return {
        "status": "tests_generated",
        "generated_tests_count": len(new_tests),
        "total_tests": len(all_tests),
        "generated_tests": new_tests,
        "reports": {
            "test_generation_report": report1_path,
            "drift_report": report2_path,
        },
    }


@app.get("/tests", response_model=List[TestCase])
def list_tests():
    return _load_tests()


@app.get("/tests/{requirement_id}", response_model=List[TestCase])
def get_tests_for_requirement(requirement_id: str):
    tests = _load_tests()
    filtered = [t for t in tests if t.get("requirement_id") == requirement_id]
    if not filtered:
        raise HTTPException(
            status_code=404, detail="No tests found for this requirement_id."
        )
    return filtered


@app.delete("/tests/{requirement_id}")
def delete_tests_for_requirement(requirement_id: str):
    tests = _load_tests()
    remaining = [t for t in tests if t.get("requirement_id") != requirement_id]
    deleted_count = len(tests) - len(remaining)
    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="No tests found for this requirement_id."
        )
    _save_tests(remaining)
    return {
        "status": "deleted",
        "requirement_id": requirement_id,
        "deleted_count": deleted_count,
    }

