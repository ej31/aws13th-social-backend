import json
import os
from pathlib import Path

from core.db_connection import get_db_connection

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "comments.json"


def get_all_comments_db():
    con= get_db_connection()
    with con:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM comments")
            return cursor.fetchall()

def get_comment_by_id(comment_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE comment_id = %s", (comment_id,))
            return cursor.fetchone()





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
