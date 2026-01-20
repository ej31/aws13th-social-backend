import logging
from datetime import datetime
from typing import Dict, Any

from schemas.user import UserCreate
from utils.data import load_json, save_json, generate_id
from utils.auth import hash_password

logger = logging.getLogger(__name__)


class DuplicateResourceError(Exception):
    def __init__(self, field: str):
        self.field = field


class UserCreateFailedError(Exception):
    pass


def create_user(user: UserCreate) -> Dict[str, Any]:
    try:
        users = load_json("users.json")

        # 이메일 중복 검사
        if any(u["email"] == user.email for u in users):
            raise DuplicateResourceError(field="email")

        #닉네임 중복 검사
        if any(u["nickname"] == user.nickname for u in users):
            raise DuplicateResourceError(field="nickname")

        new_user = {
            "id": generate_id("user", users),
            "email": user.email,
            "nickname": user.nickname,
            "profile_image_url": user.profile_image_url,
            "password": hash_password(user.password),
            "created_at": datetime.utcnow().isoformat()
        }

        users.append(new_user)

        if not save_json("users.json", users):
            logger.error("users.json 저장 실패")
            raise UserCreateFailedError()

        return new_user

    except DuplicateResourceError:
        raise

    except Exception as e:
        logger.exception("회원 생성 중 예외 발생")
        raise UserCreateFailedError()
