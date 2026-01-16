"""
User Repository
- 사용자 데이터 CRUD
"""
from datetime import datetime, timezone
from typing import Any

from app.repositories.base import BaseRepository
from app.utils.id_generator import generate_user_id
from app.core.security import get_password_hash


class UserRepository(BaseRepository):
    """
    사용자 데이터 저장소
    
    Attributes:
        data_dir: 데이터 디렉토리 경로
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Args:
            data_dir: 데이터 디렉토리 경로
        """
        super().__init__(f"{data_dir}/users.json")
        self.data_dir = data_dir
    
    # ========== 조회 메서드 ==========
    
    def find_by_user_id(self, user_id: int) -> dict[str, Any] | None:
        """
        사용자 ID로 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            dict[str, Any] | None: 사용자 데이터 또는 None
        """
        return self.find_by_id("user_id", user_id)
    
    def find_by_email(self, email: str) -> dict[str, Any] | None:
        """
        이메일로 조회
        
        Args:
            email: 이메일 주소
            
        Returns:
            dict[str, Any] | None: 사용자 데이터 또는 None
        """
        return self.handler.find_one(lambda x: x.get("email") == email)
    
    def find_by_nickname(self, nickname: str) -> dict[str, Any] | None:
        """
        닉네임으로 조회
        
        Args:
            nickname: 닉네임
            
        Returns:
            dict[str, Any] | None: 사용자 데이터 또는 None
        """
        return self.handler.find_one(lambda x: x.get("nickname") == nickname)
    
    def exists_by_email(self, email: str) -> bool:
        """
        이메일 존재 여부 확인
        
        Args:
            email: 이메일 주소
            
        Returns:
            bool: 존재 여부
        """
        return self.find_by_email(email) is not None
    
    def exists_by_nickname(self, nickname: str) -> bool:
        """
        닉네임 존재 여부 확인
        
        Args:
            nickname: 닉네임
            
        Returns:
            bool: 존재 여부
        """
        return self.find_by_nickname(nickname) is not None
    
    # ========== 생성 메서드 ==========
    
    def create_user(
        self,
        email: str,
        password: str,
        nickname: str,
        profile_image: str | None = None
    ) -> dict[str, Any]:
        """
        사용자 생성
        
        Args:
            email: 이메일 주소
            password: 비밀번호 (평문)
            nickname: 닉네임
            profile_image: 프로필 이미지 URL (선택)
            
        Returns:
            dict[str, Any]: 생성된 사용자 데이터
        """
        now = datetime.now(timezone.utc).isoformat()
        
        user_data = {
            "user_id": generate_user_id(self.data_dir),
            "email": email,
            "password": get_password_hash(password),  # 해싱된 비밀번호
            "nickname": nickname,
            "profile_image": profile_image or "https://example.com/default-profile.jpg",
            "created_at": now,
            "updated_at": now
        }
        
        return self.create(user_data)
    
    # ========== 수정 메서드 ==========
    
    def update_user(self, user_id: int, **updates) -> bool:
        """
        사용자 정보 수정
        
        Args:
            user_id: 사용자 ID
            **updates: 수정할 필드들 (nickname, profile_image, password 등)
            
        Returns:
            bool: 수정 성공 여부
            
        Example:
            >>> repo.update_user(123, nickname="새닉네임", profile_image="...")
        """
        # updated_at 자동 갱신
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        # 비밀번호가 포함되어 있으면 해싱
        if "password" in updates:
            updates["password"] = get_password_hash(updates["password"])
        
        return self.update("user_id", user_id, updates)
    
    # ========== 삭제 메서드 ==========
    
    def delete_user(self, user_id: int) -> bool:
        """
        사용자 삭제
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        return self.delete("user_id", user_id)