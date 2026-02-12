import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

from agents.fsd_agent import extract_requirements

FSD_PATH = "../docs/FSD.md"
STATE_FILE = "storage/fsd_state.json"
PENDING_FILE = "storage/pending_fsd_analysis.json"


def _compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _load_state() -> Dict[str, Any]:
    if not os.path.exists(STATE_FILE):
        return {"current_hash": None, "requirements": [], "history": [], "fsd_content": None}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"current_hash": None, "requirements": [], "history": [], "fsd_content": None}


def _save_state(state: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _detect_changes(
    old_requirements: List[Dict[str, Any]],
    new_requirements: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    old_by_id = {r["requirement_id"]: r for r in old_requirements}
    new_by_id = {r["requirement_id"]: r for r in new_requirements}

    added: List[Dict[str, Any]] = []
    updated: List[Dict[str, Any]] = []
    removed: List[Dict[str, Any]] = []

    for rid, new_req in new_by_id.items():
        if rid not in old_by_id:
            added.append(new_req)
        else:
            if new_req.get("description") != old_by_id[rid].get("description"):
                updated.append(new_req)

    for rid, old_req in old_by_id.items():
        if rid not in new_by_id:
            removed.append(old_req)

    return {"added": added, "updated": updated, "removed": removed}


def read_fsd_text() -> str:
    with open(FSD_PATH, "r", encoding="utf-8") as f:
        return f.read()


def analyze_fsd(fsd_content: str, persist_pending: bool) -> Dict[str, Any]:
    new_hash = _compute_hash(fsd_content)
    state = _load_state()
    old_hash = state.get("current_hash")
    old_requirements = state.get("requirements", [])

    if old_hash == new_hash:
        # Pas de drift
        if persist_pending and os.path.exists(PENDING_FILE):
            os.remove(PENDING_FILE)
        return {
            "drift_detected": False,
            "changes": {"added": [], "updated": [], "removed": []},
            "new_requirements": old_requirements,
        }

    # Extraire les nouvelles exigences (basé sur le parsing local, pas LLM)
    new_requirements = extract_requirements(fsd_content)
    changes = _detect_changes(old_requirements, new_requirements)

    old_fsd_content = state.get("fsd_content") or ""

    result = {
        "drift_detected": True,
        "changes": changes,
        "new_requirements": new_requirements,
        "new_hash": new_hash,
        "old_fsd_content": old_fsd_content,
        "old_requirements": old_requirements,
    }

    if persist_pending:
        os.makedirs(os.path.dirname(PENDING_FILE), exist_ok=True)
        pending_payload = {
            "fsd_content": fsd_content,
            "fsd_hash": new_hash,
            "new_requirements": new_requirements,
            "changes": changes,
            "old_fsd_content": old_fsd_content,
            "old_requirements": old_requirements,
        }
        with open(PENDING_FILE, "w", encoding="utf-8") as f:
            json.dump(pending_payload, f, indent=2, ensure_ascii=False)

    return result


def load_pending_state() -> Optional[Dict[str, Any]]:
    if not os.path.exists(PENDING_FILE):
        return None
    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return None


def commit_pending_state(fsd_content: str, new_requirements: List[Dict[str, Any]]) -> None:
    new_hash = _compute_hash(fsd_content)
    state = _load_state()

    history = state.get("history", [])
    history.append({"hash": new_hash, "timestamp": datetime.utcnow().isoformat() + "Z"})

    state["current_hash"] = new_hash
    state["requirements"] = new_requirements
    state["history"] = history
    state["fsd_content"] = fsd_content

    _save_state(state)

    if os.path.exists(PENDING_FILE):
        os.remove(PENDING_FILE)

