"""
Génère du code pytest exécutable à partir des test cases JSON.
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple

TESTS_DIR = os.path.join(os.path.dirname(__file__), "..", "tests")
GENERATED_PY_FILE = os.path.join(TESTS_DIR, "test_generated.py")


REQ_TO_FUNC = {
    "REQ-USER-001": ("user_service", "create_user", ["name", "email"]),
    "REQ-USER-002": ("user_service", "get_user_by_email", ["email"]),
    "REQ-ORDER-001": ("order_service", "create_order", ["user_email", "product_name", "quantity"]),
    "REQ-ORDER-002": ("order_service", "calculate_order_total", ["unit_price", "quantity"]),
}


def _expects_value_error(expected: str) -> bool:
    return expected and "valueerror" in str(expected).lower().replace(" ", "")


def _expects_numeric(expected: str) -> bool:
    s = str(expected).strip()
    try:
        float(s)
        return True
    except ValueError:
        return False


def _get_expected_value(expected: str) -> str:
    s = str(expected).strip()
    try:
        f = float(s)
        return str(f) if "." in s else str(int(f))
    except ValueError:
        return s


def _safe_test_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)[:80]


def generate_pytest_code(tests: List[Dict[str, Any]]) -> str:
    """Génère le code Python pytest à partir des test cases."""
    lines = [
        '"""Tests auto-générés - Ne pas modifier manuellement."""',
        "",
        "import pytest",
        "from app import user_service, order_service",
        "",
        "",
        "def _reset_db():",
        "    user_service.reset_for_testing()",
        "    order_service.reset_for_testing()",
        "",
        "",
    ]

    for i, tc in enumerate(tests):
        rid = tc.get("requirement_id", "UNKNOWN")
        test_name = tc.get("test_name", f"test_{i}")
        inputs = tc.get("inputs", {})
        expected = tc.get("expected_output", "")
        safe_name = _safe_test_name(test_name)

        mapping = REQ_TO_FUNC.get(rid)
        if not mapping:
            # Test non mappé - génère un test skip
            lines.append(f"@pytest.mark.skip(reason='{rid} non mappé')")
            lines.append(f"def test_{i}_{safe_name}():")
            lines.append("    pass")
            lines.append("")
            continue

        mod_name, func_name, param_order = mapping

        # Build call args
        args = []
        for p in param_order:
            if p in inputs:
                val = inputs[p]
                if isinstance(val, str):
                    args.append(f'"{val}"')
                else:
                    args.append(str(val))
            else:
                args.append("None")

        args_str = ", ".join(args)
        call = f"{mod_name}.{func_name}({args_str})"

        lines.append(f"def test_{i}_{safe_name}():")
        lines.append("    _reset_db()")
        if rid == "REQ-ORDER-001" and not _expects_value_error(expected):
            user_email = inputs.get("user_email", "john.doe@example.com")
            lines.append(f"    user_service.create_user('Test User', '{user_email}')  # setup")
        elif rid == "REQ-USER-001" and _expects_value_error(expected):
            # Duplicate email: create user first
            email = inputs.get("email", "john.doe@example.com")
            lines.append(f"    user_service.create_user('Existing User', '{email}')  # setup")
        elif rid == "REQ-USER-002" and not _expects_value_error(expected):
            email = inputs.get("email", "john.doe@example.com")
            lines.append(f"    user_service.create_user('Test User', '{email}')  # setup")
        lines.append("")

        if _expects_value_error(expected):
            lines.append("    with pytest.raises(ValueError):")
            lines.append(f"        {call}")
        elif _expects_numeric(expected):
            exp_val = _get_expected_value(expected)
            lines.append(f"    result = {call}")
            lines.append(f"    assert result == {exp_val}")
        else:
            lines.append(f"    result = {call}")
            lines.append("    assert result is not None")
            if rid in ("REQ-ORDER-001", "REQ-ORDER-002"):
                if rid == "REQ-ORDER-002":
                    lines.append("    assert isinstance(result, (int, float))")
                else:
                    lines.append("    assert hasattr(result, 'order_id') and hasattr(result, 'quantity')")
            else:
                lines.append("    assert hasattr(result, 'email') or hasattr(result, 'name')")

        lines.append("")

    return "\n".join(lines)


def write_generated_tests(tests: List[Dict[str, Any]], subset: Optional[List[Dict[str, Any]]] = None) -> Tuple[str, str]:
    """
    Écrit le fichier pytest.
    - subset=None: écrit tous les tests dans test_generated.py
    - subset=[...]: écrit uniquement ces tests dans test_generated_drift.py (pour drift)
    Retourne (chemin_fichier, chemin_pour_pytest).
    """
    os.makedirs(TESTS_DIR, exist_ok=True)
    tests_to_write = subset if subset is not None else tests
    filename = "test_generated_drift.py" if subset is not None else "test_generated.py"
    path = os.path.join(TESTS_DIR, filename)
    code = generate_pytest_code(tests_to_write)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return path, path
