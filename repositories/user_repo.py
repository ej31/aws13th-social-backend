import json, os
from typing import Optional
from pathlib import Path
from pymysql.cursors import DictCursor

from core.db_connection import get_db_connection

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "users.json"

def get_users_db():
    con= get_db_connection()
    with con:
        with DictCursor(con) as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

def get_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users: list[dict]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def find_user_by_id(user_id: str) -> Optional[dict]:
    users = get_users()
    return next((u for u in users if u["user_id"] == user_id), None)