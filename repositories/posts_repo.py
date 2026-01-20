import json
import os
from pathlib import Path

from core.db_connection import get_db_connection

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "posts.json"

def get_all_posts():
    con =None
    try:
        con = get_db_connection()
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM posts")
            return cursor.fetchall()
    finally:
        if con :
            con.close()

def get_post_by_id(post_id):
    con = None
    try:
        con = get_db_connection()
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
            return cursor.fetchone()
    finally:
        if con :
            con.close()

def get_post():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_post(post: list[dict]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(post, f, indent=4, ensure_ascii=False)
