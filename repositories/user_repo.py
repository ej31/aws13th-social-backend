import json, os
from typing import Optional
from pathlib import Path
from pymysql.cursors import DictCursor

from core.db_connection import get_db_connection

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "users.json"

def get_all_users_db():
    con= get_db_connection()
    with con as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()


def get_user_by_id(user_id):
    """특정 id의 사용자를 반환"""
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            return cursor.fetchone()


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