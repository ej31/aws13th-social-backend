from typing import Annotated

from fastapi import Depends, HTTPException,status

from common.security import encode_id
from repositories.comment_repository import CommentRepository
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from schemas.comment import CommentCreateRequest, CommentUpdateRequest
from datetime import datetime, timezone

class CommentService:
    def __init__(self,comment_repository: Annotated[CommentRepository,Depends(CommentRepository)],
                 post_repository: Annotated[PostRepository,Depends(PostRepository)],
                 user_repository: Annotated[UserRepository,Depends(UserRepository)]) -> None:

        self.comment_repo = comment_repository
        self.post_repo = post_repository
        self.user_repo = user_repository

    def _assemble_comment_response(self, comment: dict) -> dict:
        """댓글 데이터에 작성자 정보를 결합하는 헬퍼 메서드"""
        author = self.user_repo.find_by_id(comment["author_id"])
        if author:
            author_info = {
                "id": encode_id(author["id"]),
                "nickname": author["nickname"]
            }
        else:
            author_info = {"id": "unknown", "nickname": "탈퇴한 사용자"}
        return {
            **comment, #딕셔너리 언패킹 즉 comment안에 있는 key,value에 해당하는 json을 붙여줌
            "author": author_info
        }

    @staticmethod
    def _comment_verify_author(comment: dict, current_user_id: str) -> None:
        """현재 사용자와 댓글 글쓴이가 맞는지 확인"""
        if comment["author_id"] != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="해당 게시글에 대한 수정/삭제 권한이 없습니다.")

    async def create_comment(self,post_id: int, req: CommentCreateRequest,author_id: str):
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="해당 게시글이 존재하지 않습니다.")
        comment_data = req.model_dump(exclude_none=True)

        comment_data.update({
            "post_id" : post_id,
            "author_id": author_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": None
        })

        saved_comment = self.comment_repo.save(comment_data)
        return self._assemble_comment_response(saved_comment)

    async def get_all_comments(self,post_id: int, page: int, limit: int):
        all_comments = self.comment_repo.find_all_by_post_id(post_id)

        all_comments.sort(key=lambda x: x["created_at"], reverse=True)

        start=(page-1) * limit
        end = start+limit
        paged_comments = all_comments[start:end]

        paged_comments_data = [self._assemble_comment_response(c) for c in paged_comments]

        return paged_comments_data,len(all_comments)

    async def update_comment(self,comment_id:int,req: CommentUpdateRequest,author_id: str):
        comment = self.comment_repo.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="댓글이 존재하지 않습니다.")

        self._comment_verify_author(comment, author_id)

        update_data= req.model_dump(exclude_none=True)

        for key,value in update_data.items():
            comment[key] = value

        comment["updated_at"] = datetime.now(timezone.utc).isoformat()
        updated_comment = self.comment_repo.save(comment)
        return self._assemble_comment_response(updated_comment)

    async def delete_comment(self,comment_id:int, author_id: str) -> bool:
        comment = self.comment_repo.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="댓글이 존재하지 않습니다.")
        self._comment_verify_author(comment, author_id)

        is_deleted = self.comment_repo.delete(comment_id)

        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="서버 오류가 발생했습니다.")
        return True