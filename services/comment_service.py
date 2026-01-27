from typing import Annotated, List, Tuple
from fastapi import Depends, HTTPException, status

from common.security import encode_id
from repositories.comment_repository import CommentRepository
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from models.base import Comment as CommentTable
from schemas.comment import CommentCreateRequest, CommentUpdateRequest


class CommentService:
    def __init__(self,
                 comment_repository: Annotated[CommentRepository, Depends(CommentRepository)],
                 post_repository: Annotated[PostRepository, Depends(PostRepository)],
                 user_repository: Annotated[UserRepository, Depends(UserRepository)]) -> None:

        self.comment_repo = comment_repository
        self.post_repo = post_repository
        self.user_repo = user_repository

    async def _assemble_comment_response(self, comment: CommentTable) -> dict:
        """댓글 객체에 작성자 정보를 결합하여 반환"""
        # 비동기로 유저 정보 조회
        author = await self.user_repo.find_by_id(comment.author_id)

        if author:
            author_info = {
                "id": encode_id(author.id),
                "nickname": author.nickname
            }
        else:
            author_info = {"id": "unknown", "nickname": "탈퇴한 사용자"}

        return {
            "id": comment.id,
            "content": comment.content,
            "post_id": comment.post_id,
            "author": author_info,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at
        }

    @staticmethod
    def _comment_verify_author(comment: CommentTable, current_user_id: int) -> None:
        """현재 사용자와 댓글 작성자가 일치하는지 확인"""
        if comment.author_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="해당 댓글에 대한 수정/삭제 권한이 없습니다."
            )

    async def create_comment(self, post_id: int, req: CommentCreateRequest, author_id: int) -> dict:
        # 1. 게시글 존재 여부 확인
        post = await self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 게시글이 존재하지 않습니다."
            )

        # 2. SQLAlchemy 모델 객체 생성 (ID와 날짜는 DB 설정에 맡김)
        new_comment = CommentTable(
            content=req.content,
            post_id=post_id,
            author_id=author_id
        )

        # 3. DB 저장
        saved_comment = await self.comment_repo.add(new_comment)
        return await self._assemble_comment_response(saved_comment)

    async def get_all_comments(self, post_id: int, page: int, limit: int) -> Tuple[List[dict], int]:
        # 4. 특정 게시글의 모든 댓글 조회 (레포지토리에서 정렬되어 온다고 가정)
        all_comments = await self.comment_repo.find_all_by_post_id(post_id)

        # 페이징 처리 (추후 DB 레벨의 OFFSET/LIMIT으로 최적화 가능)
        start = (page - 1) * limit
        end = start + limit
        paged_comments = all_comments[start:end]

        # 비동기 조립
        paged_comments_data = [
            await self._assemble_comment_response(c) for c in paged_comments
        ]

        return paged_comments_data, len(all_comments)

    async def update_comment(self, comment_id: int, req: CommentUpdateRequest, author_id: int) -> dict:
        comment = await self.comment_repo.find_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글이 존재하지 않습니다."
            )

        self._comment_verify_author(comment, author_id)

        # 5. 필드 업데이트 (setattr 활용)
        update_data = req.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(comment, key, value)

        # updated_at은 모델의 onupdate=func.now()가 처리하거나 수동으로 갱신
        updated_comment = await self.comment_repo.update(comment)
        return await self._assemble_comment_response(updated_comment)

    async def delete_comment(self, comment_id: int, author_id: int) -> bool:
        comment = await self.comment_repo.find_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글이 존재하지 않습니다."
            )

        self._comment_verify_author(comment, author_id)

        is_deleted = await self.comment_repo.delete(comment_id)
        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="댓글 삭제 중 서버 오류가 발생했습니다."
            )
        return True