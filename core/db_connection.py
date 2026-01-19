import pymysql
import os
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

load_dotenv()

def get_db_connection():
    return pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DB"),
    charset=os.getenv("MYSQL_CHARSET"),
    cursorclass=DictCursor
    )

# conn = get_db_connection()
#
# with conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM users")
#         rows=cursor.fetchall()
#         for row in rows:
#             print(row)

#
# cursor = conn.cursor()
# # 3. SQL 실행
# cursor.execute("SELECT * FROM users")
#
# # 4. 결과 가져오기
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# # 5. 종료 (커서 → 연결 순서)
# cursor.close()
# conn.close()
