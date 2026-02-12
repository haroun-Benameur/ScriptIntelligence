
import hashlib
import json
import os

FSD_PATH = "../docs/FSD.md"
HASH_STORAGE = "storage/fsd_hash.json"


def compute_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def has_fsd_changed():
    current_hash = compute_hash(FSD_PATH)

    if not os.path.exists(HASH_STORAGE):
        save_hash(current_hash)
        return True

    with open(HASH_STORAGE, "r") as f:
        stored_hash = json.load(f).get("hash")

    if stored_hash != current_hash:
        save_hash(current_hash)
        return True

    return False


def save_hash(new_hash):
    os.makedirs("storage", exist_ok=True)
    with open(HASH_STORAGE, "w") as f:
        json.dump({"hash": new_hash}, f)
