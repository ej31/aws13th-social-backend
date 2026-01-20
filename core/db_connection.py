import pymysql
import os
from dotenv import load_dotenv
from pathlib import Path
from pymysql.cursors import DictCursor

BASE_DIR = Path(__file__).resolve().parent
env_db_path = BASE_DIR / ".env .DB"

# verbose=True를 넣으면 로드 과정을 상세히 출력해줍니다.
if load_dotenv(dotenv_path=env_db_path, verbose=True):
    print(f"✅ .env_DB 로드 성공! (경로: {env_db_path})")
else:
    print(f"❌ .env_DB 로드 실패! (파일이 해당 경로에 있는지 확인하세요: {env_db_path})")

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