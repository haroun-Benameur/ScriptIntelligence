"""
Génère des rapports Markdown :
1. Rapport de génération de tests - test cases par module
2. Rapport de drift - diff FSD + nouveaux tests pour la partie modifiée
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import difflib


REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def _ensure_reports_dir() -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    return REPORTS_DIR


def _group_tests_by_requirement(tests: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Regroupe les tests par requirement_id (module)."""
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for t in tests:
        rid = t.get("requirement_id", "UNKNOWN")
        if rid not in groups:
            groups[rid] = []
        groups[rid].append(t)
    return groups


def generate_test_generation_report(tests: List[Dict[str, Any]]) -> str:
    """
    Génère un rapport MD avec les test cases par module.
    Appelé lors de la génération/analyse des tests.
    """
    _ensure_reports_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_generation_report_{ts}.md"
    path = os.path.join(REPORTS_DIR, filename)

    groups = _group_tests_by_requirement(tests)

    lines = [
        "# Rapport de génération des tests",
        "",
        f"**Date:** {datetime.now().isoformat()}",
        f"**Total tests:** {len(tests)}",
        f"**Modules:** {len(groups)}",
        "",
        "---",
        "",
    ]

    for req_id in sorted(groups.keys()):
        module_tests = groups[req_id]
        lines.append(f"## Module: {req_id}")
        lines.append("")
        for i, tc in enumerate(module_tests, 1):
            lines.append(f"### Test {i}: {tc.get('test_name', 'N/A')}")
            lines.append("")
            lines.append(f"- **Description:** {tc.get('description', '')}")
            lines.append(f"- **Inputs:** `{tc.get('inputs', {})}`")
            lines.append(f"- **Expected output:** {tc.get('expected_output', '')}")
            lines.append("")
        lines.append("---")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path


def generate_drift_report(
    old_fsd: str,
    new_fsd: str,
    changes: Dict[str, List[Dict[str, Any]]],
    generated_tests: List[Dict[str, Any]],
    old_requirements: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Génère un rapport MD lors du changement FSD :
    - Diff entre ancien et nouveau FSD
    - Nouveaux test cases uniquement pour la partie modifiée
    """
    _ensure_reports_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drift_report_{ts}.md"
    path = os.path.join(REPORTS_DIR, filename)

    added = changes.get("added", [])
    updated = changes.get("updated", [])
    removed = changes.get("removed", [])

    # Diff texte (unified)
    old_lines = (old_fsd or "").splitlines(keepends=True)
    new_lines = (new_fsd or "").splitlines(keepends=True)
    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="ancien_FSD.md",
            tofile="nouveau_FSD.md",
            lineterm="",
        )
    )
    diff_text = "".join(diff_lines) if diff_lines else "(Aucune diff ou génération initiale)"

    lines = [
        "# Rapport de changement FSD (Drift)",
        "",
        f"**Date:** {datetime.now().isoformat()}",
        f"**Exigences ajoutées:** {len(added)}",
        f"**Exigences modifiées:** {len(updated)}",
        f"**Exigences supprimées:** {len(removed)}",
        f"**Nouveaux tests générés:** {len(generated_tests)}",
        "",
        "---",
        "",
        "## 1. Différence FSD (ancien vs nouveau)",
        "",
        "```diff",
        diff_text,
        "```",
        "",
        "---",
        "",
        "## 2. Exigences impactées",
        "",
    ]

    if added:
        lines.append("### Ajoutées")
        for r in added:
            lines.append(f"- **{r.get('requirement_id', '')}**")
            lines.append("")
            lines.append("```")
            lines.append(r.get("description", "")[:500])
            lines.append("```")
            lines.append("")
        lines.append("")

    if updated:
        lines.append("### Modifiées")
        old_by_id = {r["requirement_id"]: r for r in (old_requirements or [])}
        for r in updated:
            rid = r.get("requirement_id", "")
            lines.append(f"- **{rid}**")
            old_desc = old_by_id.get(rid, {}).get("description", "")
            if old_desc:
                lines.append("**Ancien:**")
                lines.append("```")
                lines.append(old_desc[:300])
                lines.append("```")
            lines.append("**Nouveau:**")
            lines.append("```")
            lines.append(r.get("description", "")[:300])
            lines.append("```")
            lines.append("")
        lines.append("")

    if removed:
        lines.append("### Supprimées")
        for r in removed:
            lines.append(f"- **{r.get('requirement_id', '')}**")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. Nouveaux test cases (partie modifiée uniquement)")
    lines.append("")

    groups = _group_tests_by_requirement(generated_tests)
    for req_id in sorted(groups.keys()):
        module_tests = groups[req_id]
        lines.append(f"### {req_id}")
        lines.append("")
        for i, tc in enumerate(module_tests, 1):
            lines.append(f"#### Test {i}: {tc.get('test_name', 'N/A')}")
            lines.append("")
            lines.append(f"- **Description:** {tc.get('description', '')}")
            lines.append(f"- **Inputs:** `{tc.get('inputs', {})}`")
            lines.append(f"- **Expected output:** {tc.get('expected_output', '')}")
            lines.append("")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path


def generate_pytest_execution_report(pytest_results: dict, filename_prefix: str = "pytest_execution") -> str:
    """
    Génère un rapport MD des résultats pytest (success/failed).
    pytest_results: dict avec passed, failed, total, results[], duration, error?
    """
    _ensure_reports_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{ts}.md"
    path = os.path.join(REPORTS_DIR, filename)

    passed = pytest_results.get("passed", 0)
    failed = pytest_results.get("failed", 0)
    total = pytest_results.get("total", passed + failed)
    duration = pytest_results.get("duration", 0)
    results = pytest_results.get("results", [])
    error = pytest_results.get("error")

    lines = [
        "# Rapport d'exécution Pytest",
        "",
        f"**Date:** {datetime.now().isoformat()}",
        f"**Total:** {total} | **Réussis:** {passed} | **Échoués:** {failed} | **Durée:** {duration}s",
        "",
    ]
    if error:
        lines.append(f"**Erreur:** {error}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Détail des tests")
    lines.append("")

    for r in results:
        status = r.get("status", "unknown")
        name = r.get("name", "?")
        dur = r.get("duration", 0)
        icon = "✅" if status == "passed" else "❌"
        status_fr = "réussi" if status == "passed" else "échoué"
        lines.append(f"- {icon} **{name}** — {status_fr} ({dur}s)")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path
