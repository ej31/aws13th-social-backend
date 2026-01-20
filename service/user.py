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

def create_user(user: UserCreate) -> Dict[str, Any]:
    # 파일 접근을 제어하기 위한 잠금 장치 설정
    lock = FileLock(LOCK_PATH, timeout=5)

    try:
        with lock:
            # 1. 기존 데이터 로드 (메모리로 가져오기)
            users = load_json("users.json")

            # 2. 중복 검사 (비즈니스 로직)
            if any(u["email"] == user.email for u in users):
                raise DuplicateResourceError(field="email")

            if any(u["nickname"] == user.nickname for u in users):
                raise DuplicateResourceError(field="nickname")

            # 3. 새로운 유저 객체 생성 (아직 리스트에 넣지 않음)
            new_user = {
                "id": generate_id("user", users),
                "email": user.email,
                "nickname": user.nickname,
                "profile_image_url": user.profile_image_url,
                "password": hash_password(user.password),
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            # 기존 users 리스트를 직접 수정하지 않고,
            # 새로운 리스트를 만들어 저장을 시도 (Copy-on-Write 방식)
            updated_users = users + [new_user]

            # 4. 파일 저장 시도
            if not save_json("users.json", updated_users):
                logger.error("users.json 파일 저장 실패")
                raise UserCreateFailedError()

            # 저장에 성공했을 때만 생성된 유저 정보를 반환.
            return new_user

    except DuplicateResourceError:
        raise

    except Timeout:
        logger.error("파일 잠금 획득 시간 초과")
        raise UserCreateFailedError()

    except Exception:
        # 민감 정보 누출 방지를 위해 구체적인 데이터 대신 예외 유형만 기록
        logger.exception("회원 생성 프로세스 중 시스템 오류 발생")
        raise UserCreateFailedError()