"""
Post Repository
- 게시글 데이터 CRUD
"""
from datetime import datetime, timezone
from typing import Any

from app.repositories.base import BaseRepository
from app.utils.id_generator import generate_post_id


class PostRepository(BaseRepository):
    """
    게시글 데이터 저장소
    
    Attributes:
        data_dir: 데이터 디렉토리 경로
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Args:
            data_dir: 데이터 디렉토리 경로
        """
        super().__init__(f"{data_dir}/posts.json")
        self.data_dir = data_dir
    
    # 조회 메서드
    
    def find_by_post_id(self, post_id: int) -> dict[str, Any] | None:
        """
        게시글 ID로 조회
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            dict[str, Any] | None: 게시글 데이터 또는 None
        """
        return self.find_by_id("post_id", post_id)
    
    def find_by_author_id(self, author_id: int) -> list[dict[str, Any]]:
        """
        작성자 ID로 게시글 목록 조회
        
        Args:
            author_id: 작성자 ID
            
        Returns:
            list[dict[str, Any]]: 게시글 목록
        """
        return self.find_many(lambda x: x.get("author_id") == author_id)
    
    def find_with_pagination(
        self,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        sort: str = "latest"
    ) -> tuple[list[dict[str, Any]], int]:
        """
        페이지네이션 및 검색/정렬을 적용한 게시글 목록 조회
        
        Args:
            page: 페이지 번호 (1부터 시작)
            limit: 페이지당 항목 수
            search: 검색 키워드 (제목, 내용에서 검색)
            sort: 정렬 기준 (latest, views, likes)
            
        Returns:
            tuple[list[dict[str, Any]], int]: (게시글 목록, 전체 개수)
        """
        
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        all_posts = self.find_all()
        
        # 검색 필터
        if search:
            search_lower = search.lower()
            all_posts = [
                post for post in all_posts
                if search_lower in post.get("title", "").lower()
                or search_lower in post.get("content", "").lower()
            ]
        
        # 정렬
        if sort == "latest":
            all_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        elif sort == "views":
            all_posts.sort(key=lambda x: x.get("views", 0), reverse=True)
        elif sort == "likes":
            all_posts.sort(key=lambda x: x.get("likes", 0), reverse=True)
        
        # 페이지네이션
        total = len(all_posts)
        start = (page - 1) * limit
        end = start + limit
        
        return all_posts[start:end], total
    
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
        
        Args:
            title: 게시글 제목
            content: 게시글 내용
            author_id: 작성자 ID
            author_nickname: 작성자 닉네임
            author_profile_image: 작성자 프로필 이미지
            
        Returns:
            dict[str, Any]: 생성된 게시글 데이터
        """
        now = datetime.now(timezone.utc).isoformat()
        
        post_data = {
            "post_id": generate_post_id(self.data_dir),
            "title": title,
            "content": content,
            "author_id": author_id,
            "author_nickname": author_nickname,
            "author_profile_image": author_profile_image,
            "views": 0,
            "likes": 0,
            "comments_count": 0,
            "created_at": now,
            "updated_at": now
        }
        
        return self.create(post_data)
    
    # 수정 메서드
    
    def update_post(self, post_id: int, **updates) -> bool:
        """
        게시글 정보 수정
        
        Args:
            post_id: 게시글 ID
            **updates: 수정할 필드들 (title, content 등)
            
        Returns:
            bool: 수정 성공 여부
        """
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        return self.update("post_id", post_id, updates)
    
    def increment_views(self, post_id: int) -> bool:
        """
        조회수 증가 (원자적 연산)
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            bool: 수정 성공 여부
        """
        return self.handler.atomic_increment(
            lambda x: x.get("post_id") == post_id,
            "views",
            1
        )
    
    def increment_likes(self, post_id: int) -> bool:
        """
        좋아요 수 증가 (원자적 연산)
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            bool: 수정 성공 여부
        """
        
        return self.handler.atomic_increment(
            lambda x: x.get("post_id") == post_id,
            "likes",
            1
        )
    
    def decrement_likes(self, post_id: int) -> bool:
        """
        좋아요 수 감소
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            bool: 수정 성공 여부
        """

        return self.handler.atomic_increment(
            lambda x: x.get("post_id") == post_id,
            "likes",
            -1
        )
    
    def increment_comments_count(self, post_id: int) -> bool:
        """
        댓글 수 증가
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            bool: 수정 성공 여부
        """
        
        return self.handler.atomic_increment(
            lambda x: x.get("post_id") == post_id,
            "comment_count",
            1
        )
    
    def decrement_comments_count(self, post_id: int) -> bool:
        """
        댓글 수 감소
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            bool: 수정 성공 여부
        """
        return self.handler.atomic_increment(
            lambda x: x.get("post_id") == post_id,
            "comment_count",
            -1
        )
    
    # 삭제 메서드
    
    def delete_post(self, post_id: int) -> bool:
        """
        게시글 삭제
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        return self.delete("post_id", post_id)
    
    # 권한 확인 메서드
    
    def is_author(self, post_id: int, user_id: int) -> bool:
        """
        게시글 작성자 여부 확인
        
        Args:
            post_id: 게시글 ID
            user_id: 사용자 ID
            
        Returns:
            bool: 작성자 여부
        """
        post = self.find_by_post_id(post_id)
        if not post:
            return False
        return post.get("author_id") == user_id