import json
import os
from pathlib import Path

from core.db_connection import get_db_connection


def get_all_comments_db():
    con= get_db_connection()
    with con:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM likes")
            return cursor.fetchall()

def get_like_by_id(like_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM likes WHERE like_id = %s", (like_id,))
            return cursor.fetchone()




DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "likes.json"

def get_likes() -> list[dict]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_likes(post: list[dict]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(post, f, indent=4, ensure_ascii=False)
