
import os
import json
import re
from typing import List, Dict, Any

from agents.llm_client import call_llm_json

FSD_PATH = "../docs/FSD.md"
TESTS_FOLDER = "tests"


def read_fsd() -> str:
    with open(FSD_PATH, "r", encoding="utf-8") as f:
        return f.read()


def extract_requirements(fsd_text: str) -> List[Dict[str, Any]]:
    """
    Extraction des exigences avec le bloc complet pour détecter les changements.
    Retourne requirement_id, description (titre), et content (bloc complet pour comparaison).
    """
    pattern = r"## (REQ-[A-Z0-9-]+): ([^\n]+)"
    matches = list(re.finditer(pattern, fsd_text))
    result = []
    for i, m in enumerate(matches):
        rid, title = m.group(1), m.group(2).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(fsd_text)
        content = fsd_text[start:end].strip()
        result.append({
            "requirement_id": rid,
            "description": title,
            "content": content,
        })
    return result


def generate_tests_with_llm(requirements: List[Dict[str, Any]], fsd_text: str) -> List[Dict[str, Any]]:
    """
    Utilise Gemini pour générer des tests au format JSON structuré.
    Retourne une liste d'objets tests (déjà parsés).
    """
    requirements_json = json.dumps(requirements, ensure_ascii=False, indent=2)
    prompt = f"""
You are a QA automation agent.

Based on the following Functional Specification Document (FSD) and the list of requirements,
generate structured unit/integration test cases.

Return ONLY a JSON array (no markdown, no explanations) with objects like:
{{
  "requirement_id": "REQ-USER-001",
  "test_name": "Short test name",
  "description": "Detailed test scenario.",
  "inputs": {{"field": "value"}},
  "expected_output": "Expected behavior."
}}

FSD:
\"\"\"
{fsd_text}
\"\"\"

Requirements:
{requirements_json}
"""

    response = call_llm_json(prompt)
    if not isinstance(response, list):
        raise ValueError("LLM did not return a JSON array for tests.")
    return response


def save_tests_json(tests: List[Dict[str, Any]]):
    os.makedirs(TESTS_FOLDER, exist_ok=True)
    file_path = os.path.join(TESTS_FOLDER, "generated_tests.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)


def run_fsd_agent():
    """
    Workflow existant utilisé par /run-workflow (compatibilité).
    Lit le FSD, génère les tests pour toutes les exigences et sauvegarde en JSON pur.
    """
    fsd_text = read_fsd()
    requirements = extract_requirements(fsd_text)

    tests = generate_tests_with_llm(requirements, fsd_text)
    save_tests_json(tests)

    return {
        "status": "tests_generated",
        "requirements_count": len(requirements)
    }
