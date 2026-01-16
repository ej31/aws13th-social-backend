"""
Like Repository
- 좋아요 데이터 CRUD
"""
from datetime import datetime, timezone
from typing import Any

from app.repositories.base import BaseRepository


class LikeRepository(BaseRepository):
    """
    좋아요 데이터 저장소
    
    Attributes:
        data_dir: 데이터 디렉토리 경로
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Args:
            data_dir: 데이터 디렉토리 경로
        """
        super().__init__(f"{data_dir}/likes.json")
        self.data_dir = data_dir
    
    # 조회 메서드
    
    def find_by_post_and_user(
        self,
        post_id: int,
        user_id: int
    ) -> dict[str, Any] | None:
        """
        특정 게시글에 특정 사용자가 누른 좋아요 조회
        
        Args:
            post_id: 게시글 ID
            user_id: 사용자 ID
            
        Returns:
            dict[str, Any] | None: 좋아요 데이터 또는 None
        """
        return self.handler.find_one(
            lambda x: x.get("post_id") == post_id and x.get("user_id") == user_id
        )
    
    def find_by_post_id(self, post_id: int) -> list[dict[str, Any]]:
        """
        게시글의 모든 좋아요 조회
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            list[dict[str, Any]]: 좋아요 목록
        """
        return self.find_many(lambda x: x.get("post_id") == post_id)
    
    def find_by_user_id(self, user_id: int) -> list[dict[str, Any]]:
        """
        사용자가 누른 모든 좋아요 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            list[dict[str, Any]]: 좋아요 목록
        """
        likes = self.find_many(lambda x: x.get("user_id") == user_id)
        # 최신순 정렬
        likes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return likes
    
    def find_by_user_id_with_pagination(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        """
        사용자가 좋아요한 게시글 목록 페이지네이션 조회
        
        Args:
            user_id: 사용자 ID
            page: 페이지 번호 (1부터 시작)
            limit: 페이지당 항목 수
            
        Returns:
            tuple[list[dict[str, Any]], int]: (좋아요 목록, 전체 개수)
        """
        # 페이지 입력 검증
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        all_likes = self.find_by_user_id(user_id)
        
        total = len(all_likes)
        start = (page - 1) * limit
        end = start + limit
        
        return all_likes[start:end], total
    
    def count_by_post_id(self, post_id: int) -> int:
        """
        게시글의 좋아요 수 조회
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            int: 좋아요 수
        """
        return len(self.find_by_post_id(post_id))
    
    def is_liked(self, post_id: int, user_id: int) -> bool:
        """
        사용자가 게시글에 좋아요를 눌렀는지 확인
        
        Args:
            post_id: 게시글 ID
            user_id: 사용자 ID
            
        Returns:
            bool: 좋아요 여부
        """
        return self.find_by_post_and_user(post_id, user_id) is not None
    
    # 생성 메서드
    
    def create_like(self, post_id: int, user_id: int) -> dict[str, Any]:
        """
        좋아요 생성
        
        Args:
            post_id: 게시글 ID
            user_id: 사용자 ID
            
        Returns:
            dict[str, Any]: 생성된 좋아요 데이터
        """
        
        existing = self.find_by_post_and_user(post_id, user_id)
        if existing:
            return existing
        now = datetime.now(timezone.utc).isoformat()
        
        like_data = {
            "post_id": post_id,
            "user_id": user_id,
            "created_at": now
        }
        
        return self.create(like_data)
    
    # 삭제 메서드
    
    def delete_like(self, post_id: int, user_id: int) -> bool:
        """
        좋아요 삭제
        
        Args:
            post_id: 게시글 ID
            user_id: 사용자 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        return self.handler.delete(
            lambda x: x.get("post_id") == post_id and x.get("user_id") == user_id
        )
    
    def delete_by_post_id(self, post_id: int) -> int:
        """
        게시글의 모든 좋아요 삭제
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            int: 삭제된 좋아요 수
        """
        likes = self.find_by_post_id(post_id)
        deleted_count = 0
        
        for like in likes:
            if self.delete_like(like["post_id"], like["user_id"]):
                deleted_count += 1
        
        return deleted_count