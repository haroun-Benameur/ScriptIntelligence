"""
Orchestrateur : coordonne les agents FSD, Drift et Test pour les différents workflows.
"""

import os
from typing import List, Dict, Any, Optional

from agents.fsd_agent import extract_requirements, generate_tests_with_llm
from agents.drift_agent import (
    read_fsd_text,
    analyze_fsd,
    load_pending_state,
    commit_pending_state,
    save_uploaded_fsd,
    load_state,
)
from agents.test_agent import (
    load_tests,
    save_tests,
    write_generated_tests,
    run_pytest,
    save_pytest_status,
    load_pytest_status,
)

CRITICAL_REQUIREMENTS = {"REQ-USER-001", "REQ-USER-002", "REQ-ORDER-001", "REQ-ORDER-002"}
_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_workflow() -> Dict[str, Any]:
    """
    Workflow complet : lit FSD, détecte drift, régénère tests (partie modifiée uniquement),
    génère rapports et exécute pytest.
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

    existing_tests = load_tests()
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
    save_tests(all_tests)
    commit_pending_state(fsd_content=fsd_content, new_requirements=new_requirements)

    from utils.report_generator import (
        generate_test_generation_report,
        generate_drift_report,
        generate_pytest_execution_report,
    )

    report1_path = generate_test_generation_report(all_tests)
    report2_path = generate_drift_report(
        old_fsd=drift_result.get("old_fsd_content", ""),
        new_fsd=fsd_content,
        changes=changes,
        generated_tests=new_tests,
        old_requirements=drift_result.get("old_requirements"),
    )
    write_generated_tests(all_tests)
    pytest_results: Dict[str, Any] = {"passed": 0, "failed": 0, "total": 0, "results": [], "duration": 0}
    if new_tests:
        write_generated_tests(new_tests, subset=new_tests)
        drift_path = os.path.join(_APP_DIR, "tests", "test_generated_drift.py")
        pytest_results = run_pytest(drift_path)
    save_pytest_status(pytest_results)
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


def generate_tests_initial() -> Dict[str, Any]:
    """
    Génération initiale : extrait toutes les exigences, génère les tests,
    exécute pytest et produit les rapports.
    """
    fsd_content = read_fsd_text()
    requirements = extract_requirements(fsd_content)
    if not requirements:
        raise ValueError(
            "Aucune exigence trouvée dans le FSD. Format attendu: ## REQ-XXX: Title"
        )

    new_tests = generate_tests_with_llm(requirements, fsd_content)
    save_tests(new_tests)
    commit_pending_state(fsd_content=fsd_content, new_requirements=requirements)

    from utils.report_generator import (
        generate_test_generation_report,
        generate_pytest_execution_report,
    )

    report_path = generate_test_generation_report(new_tests)
    write_generated_tests(new_tests)
    pytest_results = run_pytest()
    save_pytest_status(pytest_results)
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


def analyze_fsd_workflow() -> Dict[str, Any]:
    """Analyse le FSD pour détecter le drift et stocke l'état pending."""
    fsd_content = read_fsd_text()
    result = analyze_fsd(fsd_content=fsd_content, persist_pending=True)
    return {"drift_detected": result["drift_detected"], "changes": result["changes"]}


def regenerate_tests_workflow() -> Dict[str, Any]:
    """
    Régénère uniquement les tests pour les exigences ajoutées/modifiées
    détectées lors du dernier analyze_fsd.
    """
    pending = load_pending_state()
    if pending is None:
        raise ValueError(
            "No pending FSD analysis to regenerate from. Call /analyze-fsd first."
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

    existing_tests = load_tests()
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
    save_tests(all_tests)
    commit_pending_state(fsd_content=fsd_content, new_requirements=new_requirements)

    from utils.report_generator import (
        generate_test_generation_report,
        generate_drift_report,
        generate_pytest_execution_report,
    )

    report1_path = generate_test_generation_report(all_tests)
    report2_path = generate_drift_report(
        old_fsd=old_fsd,
        new_fsd=fsd_content,
        changes=changes,
        generated_tests=new_tests,
        old_requirements=old_requirements,
    )

    write_generated_tests(all_tests)
    pytest_results: Dict[str, Any] = {"passed": 0, "failed": 0, "total": 0, "results": [], "duration": 0}
    if new_tests:
        write_generated_tests(new_tests, subset=new_tests)
        drift_pytest_path = os.path.join(_APP_DIR, "tests", "test_generated_drift.py")
        pytest_results = run_pytest(drift_pytest_path)
    save_pytest_status(pytest_results)
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


def get_spec_coverage() -> Dict[str, Any]:
    """Retourne le Spec Coverage pour le frontend."""
    state = load_state()
    requirements = state.get("requirements", [])
    if not requirements:
        fsd_content = read_fsd_text()
        requirements = extract_requirements(fsd_content)
    tests = load_tests()
    pytest_status = load_pytest_status()
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


def upload_fsd_workflow(content: str) -> Dict[str, Any]:
    """Sauvegarde le FSD uploadé."""
    save_uploaded_fsd(content)
    return {"status": "uploaded"}


def list_tests_workflow() -> List[Dict[str, Any]]:
    """Liste tous les tests."""
    return load_tests()


def get_tests_for_requirement_workflow(requirement_id: str) -> List[Dict[str, Any]]:
    """Retourne les tests d'une exigence donnée."""
    tests = load_tests()
    filtered = [t for t in tests if t.get("requirement_id") == requirement_id]
    return filtered


def delete_tests_for_requirement_workflow(requirement_id: str) -> Dict[str, Any]:
    """Supprime les tests d'une exigence donnée."""
    tests = load_tests()
    remaining = [t for t in tests if t.get("requirement_id") != requirement_id]
    deleted_count = len(tests) - len(remaining)
    if deleted_count > 0:
        save_tests(remaining)
    return {"deleted_count": deleted_count}
