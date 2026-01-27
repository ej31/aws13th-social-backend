from typing import Annotated
from fastapi import Depends, HTTPException, status

from repositories.like_repository import LikeRepository
from repositories.post_repository import PostRepository
from models.base import Like as LikeTable


class LikeService:
    def __init__(self,
                 like_repo: Annotated[LikeRepository, Depends(LikeRepository)],
                 post_repo: Annotated[PostRepository, Depends(PostRepository)]):
        self.like_repo = like_repo
        self.post_repo = post_repo

    async def add_like(self, post_id: int, user_id: int) -> dict:
        """좋아요 등록 (Atomic Update 적용 가능)"""
        await self._ensure_post_exists(post_id)

        existing_like = await self.like_repo.find_by_post_and_user(post_id, user_id)

        if not existing_like:
            new_like = LikeTable(post_id=post_id, user_id=user_id)
            await self.like_repo.add(new_like)

            await self._sync_post_like_count(post_id)

        return await self.get_like_status(post_id, user_id)

    async def remove_like(self, post_id: int, user_id: int) -> dict:
        """좋아요 취소"""
        existing_like = await self.like_repo.find_by_post_and_user(post_id, user_id)

        if existing_like:
            await self.like_repo.delete(existing_like.id)
            await self._sync_post_like_count(post_id)

        return await self.get_like_status(post_id, user_id)

    async def get_like_status(self, post_id: int, user_id: int) -> dict:
        """현재 사용자의 좋아요 여부 및 실시간 집계 정보 반환"""
        await self._ensure_post_exists(post_id)

        existing_like = await self.like_repo.find_by_post_and_user(post_id, user_id)
        like_count = await self.like_repo.count_by_post_id(post_id)

        return {
            "like_id": existing_like.id if existing_like else None,
            "post_id": post_id,
            "is_liked": bool(existing_like),
            "like_count": like_count
        }

    async def _ensure_post_exists(self, post_id: int):
        """헬퍼 메서드: 비동기로 변경"""
        post = await self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")

    async def _sync_post_like_count(self, post_id: int):
        """좋아요 실제 개수를 Post 테이블에 동기화 (Data Consistency)"""
        actual_count = await self.like_repo.count_by_post_id(post_id)
        await self.post_repo.update_like_count(post_id, actual_count)