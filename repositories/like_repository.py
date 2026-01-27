from typing import Optional

from sqlalchemy import func
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Like


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all(self) -> list[Like]:
        result = await self.db.execute(select(Like))
        return list(result.scalars().all())

    async def find_by_post_and_user(self, post_id: int, user_id: int) -> Optional[Like]:
        """특정 유저가 특정 게시글에 남긴 좋아요 확인 """
        query = select(Like).where(
            Like.post_id == post_id,
            Like.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def count_by_post_id(self, post_id: int) -> int:
        """게시글별 총 좋아요 개수 집계 """
        query = select(func.count(Like.id)).where(Like.post_id == post_id)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def add(self, like_obj: Like) -> Like:
        """좋아요 정보 저장 (Insert)"""
        self.db.add(like_obj)
        await self.db.commit()
        await self.db.refresh(like_obj)
        return like_obj

    async def delete(self, like_id: int) -> bool:
        """좋아요 취소 (Delete)"""
        query = delete(Like).where(Like.id == like_id)

        result = await self.db.execute(query)

        await self.db.commit()

        return result.rowcount > 0
