"""
Comment Repository
- 댓글 데이터 CRUD (SQL 쿼리 기반)
"""
from typing import Any

from app.repositories.base import BaseRepository


class CommentRepository(BaseRepository):
    """
    댓글 데이터 저장소
    """
    
    def __init__(self):
        """comments 테이블 사용"""
        super().__init__("comments")
    
    # 조회 메서드
    
    def find_by_comment_id(self, comment_id: int) -> dict[str, Any] | None:
        """
        댓글 ID로 조회
        """
        query = """
            SELECT 
                c.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.comment_id = %s
        """
        return self.db.execute_query(query, (comment_id,), fetch_one=True)
    
    def find_by_post_id(self, post_id: int) -> list[dict[str, Any]]:
        """
        게시글 ID로 댓글 목록 조회
        """
        query = """
            SELECT 
                c.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.post_id = %s 
            ORDER BY c.created_at ASC
        """
        result = self.db.execute_query(query, (post_id,), fetch_all=True)
        return result if result else []
    
    def find_by_author_id(self, author_id: int) -> list[dict[str, Any]]:
        """
        작성자 ID로 댓글 목록 조회
        """
        query = """
            SELECT 
                c.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.user_id = %s 
            ORDER BY c.created_at DESC
        """
        result = self.db.execute_query(query, (author_id,), fetch_all=True)
        return result if result else []
    
    def find_by_post_id_with_pagination(
        self,
        post_id: int,
        page: int = 1,
        limit: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        """
        게시글의 댓글 목록 페이지네이션 조회
        """
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        
        # 전체 개수 조회
        count_query = """
            SELECT COUNT(*) as cnt 
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.post_id = %s
        """
        count_result = self.db.execute_query(count_query, (post_id,), fetch_one=True)
        total = count_result['cnt'] if count_result else 0
        
        # 페이지네이션
        offset = (page - 1) * limit
        query = """
            SELECT 
                c.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.post_id = %s 
            ORDER BY c.created_at ASC
            LIMIT %s OFFSET %s
        """
        
        comments = self.db.execute_query(query, (post_id, limit, offset), fetch_all=True)
        return (comments if comments else [], total)
    
    def find_by_author_id_with_pagination(
        self,
        author_id: int,
        page: int = 1,
        limit: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        """
        사용자의 댓글 목록 페이지네이션 조회
        """
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        
        # 전체 개수 조회
        count_query = """
            SELECT COUNT(*) as cnt 
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.user_id = %s
        """
        count_result = self.db.execute_query(count_query, (author_id,), fetch_one=True)
        total = count_result['cnt'] if count_result else 0
        
        # 페이지네이션
        offset = (page - 1) * limit
        query = """
            SELECT 
                c.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.user_id = %s 
            ORDER BY c.created_at DESC
            LIMIT %s OFFSET %s
        """
        
        comments = self.db.execute_query(query, (author_id, limit, offset), fetch_all=True)
        return (comments if comments else [], total)
    
    def count_by_post_id(self, post_id: int) -> int:
        """
        게시글의 댓글 수 조회
        """
        query = "SELECT COUNT(*) as cnt FROM comments WHERE post_id = %s"
        result = self.db.execute_query(query, (post_id,), fetch_one=True)
        return result['cnt'] if result else 0
    
    # 생성 메서드
    
    def create_comment(
        self,
        post_id: int,
        content: str,
        author_id: int,
        author_nickname: str,
        author_profile_image: str
    ) -> dict[str, Any]:
        """
        댓글 생성
        """
        query = """
            INSERT INTO comments (post_id, user_id, content)
            VALUES (%s, %s, %s)
        """
        
        with self.db.get_cursor(commit=True) as cursor:
            cursor.execute(query, (post_id, author_id, content))
            comment_id = cursor.lastrowid
        
        # 생성된 댓글 조회 (JOIN으로 author 정보 포함)
        return self.find_by_comment_id(comment_id)
    
    # 수정 메서드
    
    def update_comment(self, comment_id: int, content: str) -> bool:
        """
        댓글 내용 수정
        """
        query = "UPDATE comments SET content = %s WHERE comment_id = %s"
        affected = self.db.execute_query(query, (content, comment_id), commit=True)
        return affected > 0 if affected else False
    
    # 삭제 메서드
    
    def delete_comment(self, comment_id: int) -> bool:
        """
        댓글 삭제
        """
        return self.delete("comment_id", comment_id)
    
    def delete_by_post_id(self, post_id: int) -> int:
        """
        게시글의 모든 댓글 삭제
        """
        query = "DELETE FROM comments WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected if affected else 0
    
    # 권한 확인 메서드
    
    def is_author(self, comment_id: int, user_id: int) -> bool:
        """
        댓글 작성자 여부 확인

        """
        query = "SELECT COUNT(*) as cnt FROM comments WHERE comment_id = %s AND user_id = %s"
        result = self.db.execute_query(query, (comment_id, user_id), fetch_one=True)
        return result['cnt'] > 0 if result else False