from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, update
from models.post import Post
from datetime import datetime
from typing import List


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, content: str, user_id: int) -> Post:
        """게시글 생성"""
        post = Post(
            title=title,
            content=content,
            userId=user_id,
            viewCount=0,
        )

        self.db.add(post)
        await self.db.flush()
        await self.db.refresh(post)
        return post

    async def get_by_id(self, post_id: int) -> Post | None:
        """ID로 게시글 조회"""
        result = await self.db.execute(
            select(Post).where(Post.postId == post_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[Post]:
        """전체 게시글 조회 (페이지네이션)"""
        result = await self.db.execute(
            select(Post)
            .order_by(desc(Post.createdAt))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Post]:
        """특정 사용자의 게시글 조회"""
        result = await self.db.execute(
            select(Post)
            .where(Post.userId == user_id)
            .order_by(desc(Post.createdAt))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, post_id: int, **kwargs) -> Post | None:
        """게시글 수정"""
        post = await self.get_by_id(post_id)
        if not post:
            return None

        for key, value in kwargs.items():
            if hasattr(post, key) and value is not None:
                setattr(post, key, value)

        await self.db.flush()
        await self.db.refresh(post)
        return post

    async def delete(self, post_id: int) -> bool:
        """게시글 삭제"""
        post = await self.get_by_id(post_id)
        if not post:
            return False

        await self.db.delete(post)
        await self.db.flush()
        return True

    async def increment_view_count(self, post_id: int) -> bool:
        """조회수 증가"""
        await self.db.execute(
            update(Post)
            .where(Post.postId == post_id)
            .values(viewCount=Post.viewCount + 1)
        )
        await self.db.flush()
        return True

