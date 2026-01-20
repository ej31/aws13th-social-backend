from pathlib import Path

from core.db_connection import get_db_connection

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "users.json"

def get_all_users_db():
    conn  = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
    finally:
        if conn :
            conn.close()

def get_user_by_id(user_id):
   conn  = None
   try:
       conn  = get_db_connection()
       with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            return cursor.fetchone()
   finally:
    conn.close()


# def get_users():
#     if not os.path.exists(DB_FILE):
#         return []
#     with open(DB_FILE, "r", encoding="utf-8") as f:
#         try:
#             return json.load(f)
#         except json.JSONDecodeError:
#             return []

# def save_users(users: list[dict]):
#     with open(DB_FILE, "w", encoding="utf-8") as f:
#         json.dump(users, f, indent=4, ensure_ascii=False)