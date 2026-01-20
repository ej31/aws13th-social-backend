import json

from pathlib import Path

# 모듈 위치 기준으로 데이터 파일 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "data" / "users.json"
POSTS_FILE = BASE_DIR / "data" / "posts.json"

def read_users():
    try:
        with open(USERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in users.json: {e}")

def write_users(users: list[dict]) -> None:
    """사용자 목록을 JSON 파일에 저장합니다."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def find_user_by_email(email: str):
    users = read_users()
    for u in users:
        if u.get("email") == email:
            return u
    return None

def read_posts():
    try:
        with open(POSTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in posts.json: {e}")

def write_posts(posts: list[dict]) -> None:
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

