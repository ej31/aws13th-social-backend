from typing import Annotated
from fastapi import Depends, HTTPException

from repositories.like_repository import LikeRepository
from repositories.post_repository import PostRepository
from schemas.like import LikeInternal


class LikeService:
    def __init__(self,
                 like_repo: Annotated[LikeRepository, Depends(LikeRepository)],
                 post_repo: Annotated[PostRepository, Depends(PostRepository)]):
        self.like_repo = like_repo
        self.post_repo = post_repo

    async def add_like(self, post_id: int, user_id: int) -> dict:
        """좋아요 등록 (이미 있으면 기존 정보 반환)"""
        # 게시글 존재 확인
        self._ensure_post_exists(post_id)

        # 중복 좋아요 확인
        existing_like = self.like_repo.find_by_post_and_user(post_id, user_id)

        if not existing_like:
            #LikeInternal 모델을 통한 안전한 데이터 생성
            next_id = self.like_repo.get_next_id()
            new_like = LikeInternal(like_id=next_id,post_id=post_id, user_id=user_id)
            self.like_repo.save(new_like.model_dump())

            #Post 테이블의 좋아요 수 업데이트 (정합성 유지)
            self._sync_post_like_count(post_id)

        return await self.get_like_status(post_id, user_id)

    async def remove_like(self, post_id: int, user_id: int) -> dict:
        """좋아요 취소 (Idempotent: 없어도 에러 없이 현재 상태 반환)"""
        existing_like = self.like_repo.find_by_post_and_user(post_id, user_id)

        if existing_like:
            self.like_repo.delete(existing_like["like_id"])
            # 좋아요 취소 후 카운트 업데이트
            self._sync_post_like_count(post_id)

        return await self.get_like_status(post_id, user_id)

    async def get_like_status(self, post_id: int, user_id: int) -> dict:
        """현재 사용자의 좋아요 여부 및 게시글의 총 좋아요 수 반환"""
        self._ensure_post_exists(post_id)

        existing_like = self.like_repo.find_by_post_and_user(post_id, user_id)
        like_count = self.like_repo.count_by_post_id(post_id)

        return {
            "like_id": existing_like["like_id"] if existing_like else "",
            "post_id": str(post_id),
            "is_liked": bool(existing_like),
            "like_count": like_count
        }

    def _ensure_post_exists(self, post_id: int):
        if not self.post_repo.find_by_id(post_id):
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    def _sync_post_like_count(self, post_id: int):
        """좋아요 DB의 실제 개수를 포스트 DB에 동기화"""
        actual_count = self.like_repo.count_by_post_id(post_id)
        self.post_repo.update_like_count(post_id, actual_count)