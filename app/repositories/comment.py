"""
Comment Repository
- 댓글 데이터 CRUD
"""
from datetime import datetime, timezone
from typing import Any

from app.repositories.base import BaseRepository
from app.utils.id_generator import generate_comment_id


class CommentRepository(BaseRepository):
    """
    댓글 데이터 저장소
    
    Attributes:
        data_dir: 데이터 디렉토리 경로
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Args:
            data_dir: 데이터 디렉토리 경로
        """
        super().__init__(f"{data_dir}/comments.json")
        self.data_dir = data_dir
    
    # 조회 메서드
    
    def find_by_comment_id(self, comment_id: int) -> dict[str, Any] | None:
        """
        댓글 ID로 조회
        
        Args:
            comment_id: 댓글 ID
            
        Returns:
            dict[str, Any] | None: 댓글 데이터 또는 None
        """
        return self.find_by_id("comment_id", comment_id)
    
    def find_by_post_id(self, post_id: int) -> list[dict[str, Any]]:
        """
        게시글 ID로 댓글 목록 조회
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            list[dict[str, Any]]: 댓글 목록
        """
        comments = self.find_many(lambda x: x.get("post_id") == post_id)
        # 생성일시 기준 정렬 (오래된 것부터)
        comments.sort(key=lambda x: x.get("created_at", ""))
        return comments
    
    def find_by_author_id(self, author_id: int) -> list[dict[str, Any]]:
        """
        작성자 ID로 댓글 목록 조회
        
        Args:
            author_id: 작성자 ID
            
        Returns:
            list[dict[str, Any]]: 댓글 목록
        """
        comments = self.find_many(lambda x: x.get("author_id") == author_id)
        # 최신순 정렬
        comments.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return comments
    
    def find_by_post_id_with_pagination(
        self,
        post_id: int,
        page: int = 1,
        limit: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        """
        게시글의 댓글 목록 페이지네이션 조회
        
        Args:
            post_id: 게시글 ID
            page: 페이지 번호 (1부터 시작)
            limit: 페이지당 항목 수
            
        Returns:
            tuple[list[dict[str, Any]], int]: (댓글 목록, 전체 개수)
        """
        # 페이지 입력 검증
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        all_comments = self.find_by_post_id(post_id)
        
        total = len(all_comments)
        start = (page - 1) * limit
        end = start + limit
        
        return all_comments[start:end], total
    
    def find_by_author_id_with_pagination(
        self,
        author_id: int,
        page: int = 1,
        limit: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        """
        사용자의 댓글 목록 페이지네이션 조회
        
        Args:
            author_id: 작성자 ID
            page: 페이지 번호 (1부터 시작)
            limit: 페이지당 항목 수
            
        Returns:
            tuple[list[dict[str, Any]], int]: (댓글 목록, 전체 개수)
        """
        
        # 페이지 입력 검증
        if page < 1 or limit < 1:
            raise ValueError("page and limit must be >=1")
        all_comments = self.find_by_author_id(author_id)
        
        total = len(all_comments)
        start = (page - 1) * limit
        end = start + limit
        
        return all_comments[start:end], total
    
    def count_by_post_id(self, post_id: int) -> int:
        """
        게시글의 댓글 수 조회
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            int: 댓글 수
        """
        return len(self.find_by_post_id(post_id))
    
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
        
        Args:
            post_id: 게시글 ID
            content: 댓글 내용
            author_id: 작성자 ID
            author_nickname: 작성자 닉네임
            author_profile_image: 작성자 프로필 이미지
            
        Returns:
            dict[str, Any]: 생성된 댓글 데이터
        """
        now = datetime.now(timezone.utc).isoformat()
        
        comment_data = {
            "comment_id": generate_comment_id(self.data_dir),
            "post_id": post_id,
            "content": content,
            "author_id": author_id,
            "author_nickname": author_nickname,
            "author_profile_image": author_profile_image,
            "created_at": now,
            "updated_at": now
        }
        
        return self.create(comment_data)
    
    # 수정 메서드
    
    def update_comment(self, comment_id: int, content: str) -> bool:
        """
        댓글 내용 수정
        
        Args:
            comment_id: 댓글 ID
            content: 수정할 내용
            
        Returns:
            bool: 수정 성공 여부
        """
        updates = {
            "content": content,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        return self.update("comment_id", comment_id, updates)
    
    # 삭제 메서드
    
    def delete_comment(self, comment_id: int) -> bool:
        """
        댓글 삭제
        
        Args:
            comment_id: 댓글 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        return self.delete("comment_id", comment_id)
    
    def delete_by_post_id(self, post_id: int) -> int:
        """
        게시글의 모든 댓글 삭제
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            int: 삭제된 댓글 수
        """
        comments = self.find_by_post_id(post_id)
        deleted_count = 0
        
        for comment in comments:
            if self.delete_comment(comment["comment_id"]):
                deleted_count += 1
        
        return deleted_count
    
    # 권한 확인 메서드
    
    def is_author(self, comment_id: int, user_id: int) -> bool:
        """
        댓글 작성자 여부 확인
        
        Args:
            comment_id: 댓글 ID
            user_id: 사용자 ID
            
        Returns:
            bool: 작성자 여부
        """
        comment = self.find_by_comment_id(comment_id)
        if not comment:
            return False
        return comment.get("author_id") == user_id