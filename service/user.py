import logging
from datetime import datetime, timezone
from typing import Dict, Any
from filelock import FileLock, Timeout

from schemas.user import UserCreate
from utils.data import load_json, save_json, generate_id
from utils.auth import hash_password

logger = logging.getLogger(__name__)

LOCK_PATH = "data/users.json.lock"

class DuplicateResourceError(Exception):
    def __init__(self, field: str):
        self.field = field

class UserCreateFailedError(Exception):
    pass


class DataPersistenceError:
    pass


class ResourceBusyError:
    pass


def create_user(user: UserCreate) -> Dict[str, Any]:
    lock = FileLock(LOCK_PATH, timeout=5)

    try:
        with lock:
            # 1. 파일에서 데이터 로드 (lock 안에서!)
            users = load_json("users.json")

            # 2. 중복 검사
            if any(u["email"] == user.email for u in users):
                raise DuplicateResourceError(field="email")

            if any(u["nickname"] == user.nickname for u in users):
                raise DuplicateResourceError(field="nickname")

            # 3. 새 사용자 생성
            new_user = {
                "id": generate_id("user", users),
                "email": user.email,
                "nickname": user.nickname,
                "profile_image_url": user.profile_image_url,
                "password": hash_password(user.password),
                "created_at": datetime.utcnow().isoformat(),
            }

            # 4. Copy-on-Write 방식으로 리스트 생성
            updated_users = users + [new_user]

            # 5. 원자적 저장
            if not save_json("users.json", updated_users):
                logger.error("users.json 저장 실패")
                raise UserCreateFailedError()

            return new_user

    except Timeout:
        logger.error("파일 잠금 획득 실패 (동시 요청 과다)")
        raise UserCreateFailedError()

    except Exception:
        logger.exception("회원 생성 중 시스템 오류 발생")
        raise UserCreateFailedError()