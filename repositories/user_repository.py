import json
import os
from typing import Optional

from common.config import settings


class UserRepository:
    def __init__(self):
        self.file_path = settings.database_path
        if not os.path.exists(self.file_path):
            self._save_all([])

    #내부용 함수
    def _load_all(self) -> list[dict]:
        with open(self.file_path,"r",encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    #내부용 함수
    def _save_all(self, users: list[dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def find_by_email(self,email:str) -> Optional[dict]:
        users = self._load_all()

        for user in users:
            if user["email"] == email:
                return user

        return None

    def find_by_id(self,id:str) -> Optional[dict]:
        users = self._load_all()
        for user in users:
            if user["id"] == id:
                return user

        return None

    def save(self,user_data: dict):
        #새로운 유저를 추가하거나 기존 유저 정보를 업데이트 한다.
        users = self._load_all()

        for i, user in enumerate(users):
            if user["id"] == user_data["id"]:
                users[i] = user_data
                break
        else:
            users.append(user_data)

        self._save_all(users)

        #저장한 데이터 반환
        return user_data

    def get_next_id(self) -> int:
        users = self._load_all()
        if not users:
            return 1
        return max(user["id"] for user in users) + 1
