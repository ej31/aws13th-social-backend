import json, os
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "comments.json"

def get_comments()->list[dict]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_comments(post: list[dict]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(post, f, indent=4, ensure_ascii=False)
