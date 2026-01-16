import json, os
from typing import Optional
DB_FILE = "./DB/users.json"

def get_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users: list):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def find_user_by_id(user_id: str) -> Optional[dict]:
    users = get_users()
    return next((u for u in users if u["user_id"] == user_id), None)