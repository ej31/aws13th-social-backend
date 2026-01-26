from pathlib import Path

from core.db_connection import get_db_connection

DB_FILE = Path(__file__).resolve().parent.parent / "DB" / "users.json"

# def get_all_users_db():
#     conn  = None
#     try:
#         conn = get_db_connection()
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT * FROM users")
#             return cursor.fetchall()
#     finally:
#         if conn :
#             conn.close()

def get_user_by_id(user_id):
   conn  = None
   try:
       conn  = get_db_connection()
       with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, email, nickname, profile_image_url FROM users WHERE user_id = %s", (user_id,))
            return cursor.fetchone()
   finally:
       if conn:
            conn.close()



