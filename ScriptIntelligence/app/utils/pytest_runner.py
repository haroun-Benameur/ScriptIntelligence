"""
Exécute pytest et retourne les résultats (success/failed).
Utilise l'API programmatique pytest pour une collecte fiable des résultats.
"""

import os
import sys
import time
from typing import List, Dict, Any

TESTS_DIR = os.path.join(os.path.dirname(__file__), "..", "tests")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


class _PytestResultCollector:
    """Plugin pytest pour collecter les résultats de chaque test."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.start_times: Dict[str, float] = {}

    def pytest_runtest_setup(self, item):
        self.start_times[item.nodeid] = time.time()

    def pytest_runtest_makereport(self, item, call):
        if call.when == "call":
            name = item.name if hasattr(item, "name") else item.nodeid.split("::")[-1]
            duration = round(time.time() - self.start_times.get(item.nodeid, time.time()), 2)
            outcome = "passed" if call.excinfo is None else "failed"
            self.results.append({"name": name, "status": outcome, "duration": duration})


def run_pytest(test_path: str | None = None) -> Dict[str, Any]:
    """
    Exécute pytest sur test_path (ou tests/ si None).
    Retourne un dict avec: passed, failed, total, results[], duration.
    Ne lève jamais d'exception - même si pytest échoue, on retourne les résultats.
    """
    path = test_path or TESTS_DIR
    os.makedirs(REPORTS_DIR, exist_ok=True)

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    abs_path = path if os.path.isabs(path) else os.path.join(project_root, path)
    if not os.path.exists(abs_path):
        abs_path = os.path.join(TESTS_DIR, "test_generated.py")

    collector = _PytestResultCollector()
    start = time.time()
    old_cwd = os.getcwd()

    try:
        os.chdir(project_root)
        import pytest
        exit_code = pytest.main(
            [
                abs_path,
                "-v",
                "--tb=no",
                "-p", "no:cacheprovider",
            ],
            plugins=[collector],
        )
    except Exception as e:
        os.chdir(old_cwd)
        return {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "duration": 0,
            "results": [],
            "error": str(e),
        }
    finally:
        os.chdir(old_cwd)

    duration = round(time.time() - start, 2)
    results = collector.results
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    total = len(results)

    return {
        "passed": passed,
        "failed": failed,
        "total": total,
        "duration": duration,
        "results": results,
        "exit_code": exit_code,
    }
