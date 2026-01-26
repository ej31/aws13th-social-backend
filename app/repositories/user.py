"""
User Repository
- 사용자 데이터 CRUD
"""
from datetime import datetime, timezone
from typing import Any

from app.repositories.base import BaseRepository
from app.core.security import get_password_hash


class UserRepository(BaseRepository):
    """
    사용자 데이터 저장소
    """
    
    def __init__(self):
        """users 테이블 사용"""
        super().__init__("users")
    
    # 조회 메서드
    
    def find_by_user_id(self, user_id: int) -> dict[str, Any] | None:
        """
        사용자 ID로 조회
        """
        return self.find_by_id("user_id", user_id)
    
    def find_by_email(self, email: str) -> dict[str, Any] | None:
        """
        이메일로 조회
        """
        query = "SELECT * FROM users WHERE email = %s"
        return self.db.execute_query(query, (email,), fetch_one=True)
    
    def find_by_nickname(self, nickname: str) -> dict[str, Any] | None:
        """
        닉네임으로 조회
        """
        query = "SELECT * FROM users WHERE nickname = %s"
        return self.db.execute_query(query, (nickname,), fetch_one=True)
    
    def exists_by_email(self, email: str) -> bool:
        """
        이메일 존재 여부 확인
        """
        query = "SELECT COUNT(*) as cnt FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,), fetch_one=True)
        return result['cnt'] > 0 if result else False
    
    def exists_by_nickname(self, nickname: str) -> bool:
        """
        닉네임 존재 여부 확인
        """
        query = "SELECT COUNT(*) as cnt FROM users WHERE nickname = %s"
        result = self.db.execute_query(query, (nickname,), fetch_one=True)
        return result['cnt'] > 0 if result else False
    
    # 생성 메서드
    
    def create_user(
        self,
        email: str,
        password: str,
        nickname: str,
        profile_image: str | None = None
    ) -> dict[str, Any]:
        """
        사용자 생성
        """
        hashed_password = get_password_hash(password)
        default_image = profile_image or "https://example.com/default-profile.jpg"
        
        query = """
            INSERT INTO users (email, password, nickname, profile_image)
            VALUES (%s, %s, %s, %s)
        """
        
        with self.db.get_cursor(commit=True) as cursor:
            cursor.execute(query, (email, hashed_password, nickname, default_image))
            user_id = cursor.lastrowid
        
        # 생성된 사용자 조회
        return self.find_by_user_id(user_id)
    
    # 수정 메서드
    
    def update_user(self, user_id: int, **updates) -> bool:
        """
        사용자 정보 수정
        """
        if not updates:
            return False
        
        # 비밀번호가 포함되어 있으면 해싱
        if "password" in updates and updates["password"]:
            updates["password"] = get_password_hash(updates["password"])
        
        # SET 절 생성
        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"UPDATE users SET {set_clause} WHERE user_id = %s"
        
        params = list(updates.values()) + [user_id]
        affected = self.db.execute_query(query, tuple(params), commit=True)
        
        return affected > 0 if affected else False
    
    # 삭제 메서드
    
    def delete_user(self, user_id: int) -> bool:
        """
        사용자 삭제
        """
        return self.delete("user_id", user_id)