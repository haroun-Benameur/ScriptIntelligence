"""
Agent Test : génération du code pytest, exécution des tests, gestion des tests JSON.
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_FILE = os.path.join(_APP_DIR, "tests", "generated_tests.json")
PYTEST_STATUS_FILE = os.path.join(_APP_DIR, "storage", "last_pytest.json")


def load_tests() -> List[Dict[str, Any]]:
    """Charge les tests depuis generated_tests.json."""
    if not os.path.exists(TESTS_FILE):
        return []
    with open(TESTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tests(tests: List[Dict[str, Any]]) -> None:
    """Sauvegarde les tests dans generated_tests.json."""
    os.makedirs(os.path.dirname(TESTS_FILE), exist_ok=True)
    with open(TESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)


def write_generated_tests(
    tests: List[Dict[str, Any]], subset: Optional[List[Dict[str, Any]]] = None
) -> Tuple[str, str]:
    """
    Génère et écrit le code pytest.
    - subset=None : écrit tous les tests dans test_generated.py
    - subset=[...] : écrit uniquement ces tests dans test_generated_drift.py
    Retourne (chemin_fichier, chemin_pour_pytest).
    """
    from utils.test_code_generator import write_generated_tests as _write
    return _write(tests, subset=subset)


def run_pytest(test_path: Optional[str] = None) -> Dict[str, Any]:
    """Exécute pytest et retourne les résultats (passed, failed, total, results, duration)."""
    from utils.pytest_runner import run_pytest as _run
    return _run(test_path)


def save_pytest_status(pytest_results: Dict[str, Any]) -> None:
    """Sauvegarde le statut pytest (passed, failed, total) pour le frontend."""
    os.makedirs(os.path.dirname(PYTEST_STATUS_FILE), exist_ok=True)
    with open(PYTEST_STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "passed": pytest_results.get("passed", 0),
                "failed": pytest_results.get("failed", 0),
                "total": pytest_results.get("total", 0),
            },
            f,
        )


def load_pytest_status() -> Dict[str, Any]:
    """Charge le dernier statut pytest."""
    if not os.path.exists(PYTEST_STATUS_FILE):
        return {"passed": 0, "failed": 0, "total": 0}
    try:
        with open(PYTEST_STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"passed": 0, "failed": 0, "total": 0}
