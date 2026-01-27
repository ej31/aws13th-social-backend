"""
Post Repository
- 게시글 데이터 CRUD (SQL 쿼리 기반)
"""
from typing import Any, Literal

from app.repositories.base import BaseRepository


class PostRepository(BaseRepository):
    """
    게시글 데이터 저장소
    """
    
    def __init__(self):
        """posts 테이블 사용"""
        super().__init__("posts")
    
    # 조회 메서드
    
    def find_by_post_id(self, post_id: int) -> dict[str, Any] | None:
        """
        게시글 ID로 조회
        """
        query = """
            SELECT 
                p.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.post_id = %s
        """
        return self.db.execute_query(query, (post_id,), fetch_one=True)
    
    def find_by_author_id(self, author_id: int) -> list[dict[str, Any]]:
        """
        작성자 ID로 게시글 목록 조회
        """
        query = """
            SELECT 
                p.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.user_id = %s 
            ORDER BY p.created_at DESC
        """
        result = self.db.execute_query(query, (author_id,), fetch_all=True)
        return result if result else []
    
    def find_with_pagination(
        self,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        sort: Literal["latest", "views", "likes"] = "latest"
    ) -> tuple[list[dict[str, Any]], int]:
        """
        페이지네이션 및 검색/정렬을 적용한 게시글 목록 조회
        """
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        
        # 검색 조건
        where_clause = ""
        params = []
        
        if search:
            # LIKE 와일드카드 이스케이프 처리
            escaped_search = search.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
            search_param = f"%{escaped_search}%"
            where_clause = "WHERE p.title LIKE %s OR p.content LIKE %s"
            params = [search_param, search_param]
        
        # 전체 개수 조회
        count_query = f"""
            SELECT COUNT(*) as cnt 
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            {where_clause}
        """
        count_result = self.db.execute_query(count_query, tuple(params), fetch_one=True)
        total = count_result['cnt'] if count_result else 0
        
        # 정렬 기준
        order_by = {
            "latest": "p.created_at DESC",
            "views": "p.views DESC",
            "likes": "p.likes DESC"
        }.get(sort, "p.created_at DESC")
        
        # 페이지네이션
        offset = (page - 1) * limit
        
        query = f"""
            SELECT 
                p.*,
                u.user_id as author_id,
                u.nickname as author_nickname,
                u.profile_image as author_profile_image
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            {where_clause}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
        """
        
        params.extend([limit, offset])
        posts = self.db.execute_query(query, tuple(params), fetch_all=True)
        
        return (posts if posts else [], total)
    
    # 생성 메서드
    
    def create_post(
        self,
        title: str,
        content: str,
        author_id: int,
        author_nickname: str,
        author_profile_image: str
    ) -> dict[str, Any]:
        """
        게시글 생성
        """
        query = """
            INSERT INTO posts (title, content, user_id)
            VALUES (%s, %s, %s)
        """
        
        with self.db.get_cursor(commit=True) as cursor:
            cursor.execute(query, (title, content, author_id))
            post_id = cursor.lastrowid
        
        # 생성된 게시글 조회 (JOIN으로 author 정보 포함)
        return self.find_by_post_id(post_id)
    
    # 수정 메서드
    
    def update_post(self, post_id: int, **updates) -> bool:
        """
        게시글 정보 수정
        """
        # 화이트리스트: 업데이트 가능한 필드만 허용
        ALLOWED_FIELDS = {'title', 'content'}
        
        if not updates:
            return False
        
        # 허용되지 않은 필드 필터링
        filtered_updates = {k: v for k, v in updates.items() if k in ALLOWED_FIELDS}
        
        if not filtered_updates:
            return False
        
        # SET 절 생성
        set_clause = ", ".join([f"{key} = %s" for key in filtered_updates.keys()])
        query = f"UPDATE posts SET {set_clause} WHERE post_id = %s"
        
        params = list(filtered_updates.values()) + [post_id]
        affected = self.db.execute_query(query, tuple(params), commit=True)
        
        # affected가 None이면 실패, 0 이상이면 성공 (같은 값 업데이트도 성공으로 간주)
        return affected is not None and affected >= 0
    
    def increment_views(self, post_id: int) -> bool:
        """
        조회수 증가 (원자적 연산)
        """
        query = "UPDATE posts SET views = views + 1 WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected > 0 if affected else False
    
    def increment_likes(self, post_id: int) -> bool:
        """
        좋아요 수 증가 (원자적 연산)
        """
        query = "UPDATE posts SET likes = likes + 1 WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected > 0 if affected else False
    
    def decrement_likes(self, post_id: int) -> bool:
        """
        좋아요 수 감소
        """
        query = "UPDATE posts SET likes = GREATEST(likes - 1, 0) WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected > 0 if affected else False
    
    def increment_comments_count(self, post_id: int) -> bool:
        """
        댓글 수 증가
        """
        query = "UPDATE posts SET comments_count = comments_count + 1 WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected > 0 if affected else False
    
    def decrement_comments_count(self, post_id: int) -> bool:
        """
        댓글 수 감소
        """
        query = "UPDATE posts SET comments_count = GREATEST(comments_count - 1, 0) WHERE post_id = %s"
        affected = self.db.execute_query(query, (post_id,), commit=True)
        return affected > 0 if affected else False
    
    # 삭제 메서드
    
    def delete_post(self, post_id: int) -> bool:
        """
        게시글 삭제
        """
        return self.delete("post_id", post_id)
    
    # 권한 확인 메서드
    
    def is_author(self, post_id: int, user_id: int) -> bool:
        """
        게시글 작성자 여부 확인
        """
        query = "SELECT COUNT(*) as cnt FROM posts WHERE post_id = %s AND user_id = %s"
        result = self.db.execute_query(query, (post_id, user_id), fetch_one=True)
        return result['cnt'] > 0 if result else False