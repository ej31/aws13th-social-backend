from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_, func
from sqlalchemy.exc import IntegrityError
from models.like import Like
from typing import List


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, post_id: int, user_id: int) -> Like | None:
        """좋아요 생성 (중복 시 None 반환)"""
        try:
            like = Like(
                postId=post_id,
                userId=user_id
            )
            self.db.add(like)
            await self.db.flush()
            await self.db.refresh(like)
            return like
        except IntegrityError:
            return None

    async def get_by_id(self, like_id: int) -> Like | None:
        """ID로 좋아요 조회"""
        result = await self.db.execute(
            select(Like).where(Like.likeId == like_id)
        )
        return result.scalar_one_or_none()

    async def get_by_post_and_user(self, post_id: int, user_id: int) -> Like | None:
        """특정 게시글과 사용자로 좋아요 조회"""
        result = await self.db.execute(
            select(Like).where(
                and_(Like.postId == post_id, Like.userId == user_id)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_post_id(self, post_id: int, skip: int = 0, limit: int = 100) -> List[Like]:
        """특정 게시글의 좋아요 목록 조회"""
        result = await self.db.execute(
            select(Like)
            .where(Like.postId == post_id)
            .order_by(desc(Like.createdAt))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Like]:
        """특정 사용자의 좋아요 목록 조회"""
        result = await self.db.execute(
            select(Like)
            .where(Like.userId == user_id)
            .order_by(desc(Like.createdAt))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete(self, like_id: int) -> bool:
        """좋아요 삭제 (ID로)"""
        like = await self.get_by_id(like_id)
        if not like:
            return False

        await self.db.delete(like)
        await self.db.flush()
        return True

    async def delete_by_post_and_user(self, post_id: int, user_id: int) -> bool:
        """좋아요 삭제 (게시글 ID와 사용자 ID로)"""
        like = await self.get_by_post_and_user(post_id, user_id)
        if not like:
            return False

        await self.db.delete(like)
        await self.db.flush()
        return True

    async def is_liked(self, post_id: int, user_id: int) -> bool:
        """사용자가 게시글에 좋아요를 했는지 확인"""
        like = await self.get_by_post_and_user(post_id, user_id)
        return like is not None

    async def count_by_post_id(self, post_id: int) -> int:
        """게시글의 좋아요 개수 조회"""
        result = await self.db.execute(
            select(func.count(Like.likeId)).where(Like.postId == post_id)
        )
        return result.scalar()
