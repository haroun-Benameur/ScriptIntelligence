import json
import re
from typing import Any


def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```", 2)
        if len(parts) >= 2:
            text = parts[1]
        if "```" in text:
            text = text.split("```", 1)[0]
    return text.strip()


def _extract_main_json_block(text: str) -> str:
    start_candidates = [i for i in (text.find("["), text.find("{")) if i != -1]
    if not start_candidates:
        return text
    start = min(start_candidates)

    end_bracket = text.rfind("]")
    end_brace = text.rfind("}")
    end_candidates = [i for i in (end_bracket, end_brace) if i != -1]
    if not end_candidates:
        return text[start:]
    end = max(end_candidates) + 1
    return text[start:end]


def _remove_llm_noise(text: str) -> str:
    # Supprime les artefacts Part(...), thought_signature, etc.
    text = re.sub(r"Part\([^)]*\)", "", text)
    text = re.sub(r'"thought_signature"\s*:\s*".*?"\s*,?', "", text)
    text = re.sub(r'"thoughts"\s*:\s*".*?"\s*,?', "", text)
    # Nettoie les virgules surnuméraires avant ] ou }
    text = re.sub(r",(\s*[\]\}])", r"\1", text)
    return text


def clean_json_text(raw: str) -> str:
    text = raw.strip()
    text = _strip_markdown_fences(text)
    text = _extract_main_json_block(text)
    text = _remove_llm_noise(text)
    return text.strip()


def clean_and_parse_json(raw: str) -> Any:
    """
    Nettoie la sortie LLM (Markdown, Part(), thought_signature, etc.)
    puis parse avec json.loads.
    """
    cleaned = clean_json_text(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM JSON output: {e}\nCleaned text: {cleaned[:500]}")

