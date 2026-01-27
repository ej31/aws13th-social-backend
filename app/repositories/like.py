"""
Like Repository
- 좋아요 데이터 CRUD (SQL 쿼리 기반)
"""
from typing import Any

from app.repositories.base import BaseRepository


class LikeRepository(BaseRepository):
    """
    좋아요 데이터 저장소
    """
    
    def __init__(self):
        """likes 테이블 사용"""
        super().__init__("likes")
    
    # 조회 메서드
    
    def find_by_post_and_user(
        self,
        post_id: int,
        user_id: int
    ) -> dict[str, Any] | None:
        """
        특정 게시글에 특정 사용자가 누른 좋아요 조회
        """
        query = "SELECT * FROM likes WHERE post_id = %s AND user_id = %s"
        return self.db.execute_query(query, (post_id, user_id), fetch_one=True)
    
    def find_by_post_id(self, post_id: int) -> list[dict[str, Any]]:
        """
        게시글의 모든 좋아요 조회
        """
        query = "SELECT * FROM likes WHERE post_id = %s"
        result = self.db.execute_query(query, (post_id,), fetch_all=True)
        return result if result else []
    
    def find_by_user_id(self, user_id: int) -> list[dict[str, Any]]:
        """
        사용자가 누른 모든 좋아요 조회
        """
        query = "SELECT * FROM likes WHERE user_id = %s ORDER BY created_at DESC"
        result = self.db.execute_query(query, (user_id,), fetch_all=True)
        return result if result else []
    
    def find_by_user_id_with_pagination(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        """
        사용자가 좋아요한 게시글 목록 페이지네이션 조회
        """
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        
        # 전체 개수 조회
        count_query = "SELECT COUNT(*) as cnt FROM likes WHERE user_id = %s"
        count_result = self.db.execute_query(count_query, (user_id,), fetch_one=True)
        total = count_result['cnt'] if count_result else 0
        
        # 페이지네이션
        offset = (page - 1) * limit
        query = """
            SELECT * FROM likes 
            WHERE user_id = %s 
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        
        likes = self.db.execute_query(query, (user_id, limit, offset), fetch_all=True)
        return (likes if likes else [], total)
    
    def count_by_post_id(self, post_id: int) -> int:
        """
        게시글의 좋아요 수 조회
        """
        query = "SELECT COUNT(*) as cnt FROM likes WHERE post_id = %s"
        result = self.db.execute_query(query, (post_id,), fetch_one=True)
        return result['cnt'] if result else 0
    
    def is_liked(self, post_id: int, user_id: int) -> bool:
        """
        사용자가 게시글에 좋아요를 눌렀는지 확인
        """
        query = "SELECT COUNT(*) as cnt FROM likes WHERE post_id = %s AND user_id = %s"
        result = self.db.execute_query(query, (post_id, user_id), fetch_one=True)
        return result['cnt'] > 0 if result else False
    
    # 생성 메서드
    
    def create_like(self, post_id: int, user_id: int) -> dict[str, Any]:
        """
        좋아요 생성
        """
        query = "INSERT INTO likes (post_id, user_id) VALUES (%s, %s)"
        
        try:
            self.db.execute_query(query, (post_id, user_id), commit=True)
            # 생성된 좋아요 조회
            return self.find_by_post_and_user(post_id, user_id)
        except Exception as e:
            # UNIQUE 제약조건 위반 시 기존 데이터 반환
            if "Duplicate entry" in str(e) or "1062" in str(e):
                return self.find_by_post_and_user(post_id, user_id)
            raise
    
    # 삭제 메서드
    
    def delete_like(self, post_id: int, user_id: int) -> bool:
        """
        좋아요 삭제
        """
        query = "DELETE FROM likes WHERE post_id = %s AND user_id = %s"
        affected = self.db.execute_query(query, (post_id, user_id), commit=True)
        return affected > 0 if affected else False
    
    def delete_by_post_id(self, post_id: int) -> int:
        """
        게시글의 모든 좋아요 삭제
        """
        query = "DELETE FROM likes WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected if affected else 0