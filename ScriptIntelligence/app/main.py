# main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

from agents.fsd_agent import generate_tests_with_llm, extract_requirements
from services.drift_service import (
    analyze_fsd,
    read_fsd_text,
    load_pending_state,
    commit_pending_state,
    save_uploaded_fsd,
    load_state,
)

app = FastAPI()

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TESTS_FILE = "tests/generated_tests.json"
PYTEST_STATUS_FILE = "storage/last_pytest.json"
CRITICAL_REQUIREMENTS = {"REQ-USER-001", "REQ-USER-002", "REQ-ORDER-001", "REQ-ORDER-002"}  # Exigences critiques


def _load_pytest_status() -> Dict[str, Any]:
    if not os.path.exists(PYTEST_STATUS_FILE):
        return {"passed": 0, "failed": 0, "total": 0}
    try:
        with open(PYTEST_STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"passed": 0, "failed": 0, "total": 0}


def _save_pytest_status(pytest_results: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(PYTEST_STATUS_FILE), exist_ok=True)
    with open(PYTEST_STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"passed": pytest_results.get("passed", 0), "failed": pytest_results.get("failed", 0), "total": pytest_results.get("total", 0)},
            f,
        )


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

    from utils.report_generator import (
        generate_test_generation_report,
        generate_drift_report,
        generate_pytest_execution_report,
    )
    from utils.test_code_generator import write_generated_tests
    from utils.pytest_runner import run_pytest

    report1_path = generate_test_generation_report(all_tests)
    report2_path = generate_drift_report(
        old_fsd=drift_result.get("old_fsd_content", ""),
        new_fsd=fsd_content,
        changes=changes,
        generated_tests=new_tests,
        old_requirements=drift_result.get("old_requirements"),
    )
    write_generated_tests(all_tests)
    pytest_results = {"passed": 0, "failed": 0, "total": 0, "results": [], "duration": 0}
    if new_tests:
        write_generated_tests(new_tests, subset=new_tests)
        drift_path = os.path.join(os.path.dirname(__file__), "tests", "test_generated_drift.py")
        pytest_results = run_pytest(drift_path)
    _save_pytest_status(pytest_results)
    pytest_report_path = generate_pytest_execution_report(
        pytest_results, filename_prefix="pytest_drift_execution"
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
        "pytest_results": pytest_results,
        "reports": {
            "test_generation_report": os.path.basename(report1_path),
            "drift_report": os.path.basename(report2_path),
            "pytest_execution_report": os.path.basename(pytest_report_path),
        },
    }


@app.post("/upload-fsd")
async def upload_fsd(file: UploadFile = File(...)):
    """
    Upload un fichier FSD (.md). Le contenu est sauvegardé et utilisé pour analyse/génération.
    """
    if not file.filename or not file.filename.lower().endswith(".md"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .md sont acceptés.")
    content = (await file.read()).decode("utf-8", errors="replace")
    save_uploaded_fsd(content)
    return {"status": "uploaded", "filename": file.filename}


@app.post("/generate-tests")
def generate_tests_initial():
    """
    Génération initiale : lit le FSD uploadé, extrait toutes les exigences, génère les tests,
    exécute pytest et produit un rapport d'exécution MD.
    """
    fsd_content = read_fsd_text()
    requirements = extract_requirements(fsd_content)
    if not requirements:
        raise HTTPException(status_code=400, detail="Aucune exigence trouvée dans le FSD. Format attendu: ## REQ-XXX: Title")

    new_tests = generate_tests_with_llm(requirements, fsd_content)
    _save_tests(new_tests)
    commit_pending_state(fsd_content=fsd_content, new_requirements=requirements)

    from utils.report_generator import generate_test_generation_report, generate_pytest_execution_report
    from utils.test_code_generator import write_generated_tests
    from utils.pytest_runner import run_pytest

    report_path = generate_test_generation_report(new_tests)
    write_generated_tests(new_tests)
    pytest_results = run_pytest()
    _save_pytest_status(pytest_results)
    pytest_report_path = generate_pytest_execution_report(pytest_results)
    reports = {
        "test_generation_report": os.path.basename(report_path),
        "pytest_execution_report": os.path.basename(pytest_report_path),
    }
    return {
        "status": "tests_generated",
        "requirements_count": len(requirements),
        "generated_tests_count": len(new_tests),
        "generated_tests": new_tests,
        "pytest_results": pytest_results,
        "reports": reports,
    }


@app.get("/reports/{filename:path}")
def get_report(filename: str):
    """Récupère le contenu d'un rapport pour affichage ou téléchargement."""
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    safe_name = os.path.basename(filename)
    path = os.path.normpath(os.path.join(reports_dir, safe_name))
    if not os.path.abspath(path).startswith(os.path.abspath(reports_dir)):
        raise HTTPException(status_code=403, detail="Accès refusé")
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return FileResponse(path, filename=safe_name)


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

    from utils.report_generator import (
        generate_test_generation_report,
        generate_drift_report,
        generate_pytest_execution_report,
    )
    from utils.test_code_generator import write_generated_tests
    from utils.pytest_runner import run_pytest

    report1_path = generate_test_generation_report(all_tests)
    report2_path = generate_drift_report(
        old_fsd=old_fsd,
        new_fsd=fsd_content,
        changes=changes,
        generated_tests=new_tests,
        old_requirements=old_requirements,
    )

    write_generated_tests(all_tests)
    pytest_results = {"passed": 0, "failed": 0, "total": 0, "results": [], "duration": 0}
    if new_tests:
        write_generated_tests(new_tests, subset=new_tests)
        drift_pytest_path = os.path.join(os.path.dirname(__file__), "tests", "test_generated_drift.py")
        pytest_results = run_pytest(drift_pytest_path)
    _save_pytest_status(pytest_results)
    pytest_report_path = generate_pytest_execution_report(
        pytest_results, filename_prefix="pytest_drift_execution"
    )
    reports = {
        "test_generation_report": os.path.basename(report1_path),
        "drift_report": os.path.basename(report2_path),
        "pytest_execution_report": os.path.basename(pytest_report_path),
    }
    return {
        "status": "tests_generated",
        "generated_tests_count": len(new_tests),
        "total_tests": len(all_tests),
        "generated_tests": new_tests,
        "pytest_results": pytest_results,
        "reports": reports,
    }


@app.get("/spec-coverage")
def get_spec_coverage():
    """
    Retourne le Spec Coverage: scénarios (exigences FSD), couverture par tests, et qualité.
    Utilisé par le frontend pour afficher Spec Coverage et Quality Gate.
    """
    state = load_state()
    requirements = state.get("requirements", [])
    if not requirements:
        fsd_content = read_fsd_text()
        requirements = extract_requirements(fsd_content)
    tests = _load_tests()
    pytest_status = _load_pytest_status()
    covered_ids = {t.get("requirement_id") for t in tests}
    scenarios = [
        {
            "id": r["requirement_id"],
            "name": r.get("description", r["requirement_id"]),
            "covered": r["requirement_id"] in covered_ids,
            "critical": r["requirement_id"] in CRITICAL_REQUIREMENTS,
        }
        for r in requirements
    ]
    covered = sum(1 for s in scenarios if s["covered"])
    total = len(scenarios)
    percentage = round((covered / total) * 100) if total > 0 else 0
    uncovered_critical = [s for s in scenarios if not s["covered"] and s["critical"]]
    tests_pass = pytest_status.get("total", 0) > 0 and pytest_status.get("failed", 0) == 0
    spec_coverage_ok = percentage >= 80
    critical_covered = len(uncovered_critical) == 0
    return {
        "scenarios": scenarios,
        "covered": covered,
        "total": total,
        "percentage": percentage,
        "uncovered_critical": uncovered_critical,
        "quality_gate": {
            "tests_pass": tests_pass,
            "spec_coverage_ok": spec_coverage_ok,
            "critical_covered": critical_covered,
            "all_pass": tests_pass and spec_coverage_ok and critical_covered,
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

