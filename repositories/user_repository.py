import json
import os
from typing import Optional

from common.config import settings


class UserRepository:
    def __init__(self) -> None:
        self.file_path = settings.users_json_path
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
    def _save_all(self, users: list[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def find_by_email(self,email:str) -> Optional[dict]:
        users = self._load_all()
        for user in users:
            if user["email"] == email:
                return user

        return None

    def find_by_id(self,id:int) -> Optional[dict]:
        users = self._load_all()
        for user in users:
            if user["id"] == id:
                return user

        return None

    def save(self,user_data: dict) -> dict:
        #새로운 유저를 추가하거나 기존 유저 정보를 업데이트 한다.
        users = self._load_all()

        for i, user in enumerate(users):
            if user["id"] == user_data["id"]:
                users[i] = user_data
                break
        else:
            raise ValueError(f"ID가 {user_data['id']}인 유저를 찾을 수 없어 수정할 수 없습니다.")

        self._save_all(users)

        #저장한 데이터 반환
        return user_data

    def get_next_id(self) -> int:
        users = self._load_all()

        #유저가 존재하지 않으면 id는 1이 된다.
        if not users:
            return 1
        #id값이 제일 높은 값을 찾은 뒤 1을 더한 값을 id로 함
        return max(user["id"] for user in users) + 1

    def delete_by_email(self,email:str):
        #유저 전체를 메모리로 가져온다.
        users = self._load_all()

        #삭제할 이메일이 아닌 유저들만 골라낸다.
        filter_user = [user for user in users if user["email"]!=email]

        #걸러낸 목록을 파일에 저장한다.
        self._save_all(filter_user)

