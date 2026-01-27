from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Post


class PostRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_all(self) -> list[Post]:
        result = await self.db.execute(select(Post).order_by(Post.created_at.desc()))
        return list(result.scalars().all())

    async def find_by_id(self, post_id: int) -> dict | None:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalars().first()

    async def add(self, post_obj: Post) -> Post:
        self.db.add(post_obj)
        await self.db.commit()
        await self.db.refresh(post_obj)
        return post_obj

    async def delete(self, post_id: int) -> bool:
        query = delete(Post).where(Post.id == post_id)
        result = await self.db.execute(query)
        await self.db.commit()

        return result.rowcount > 0

    async def update_like_count(self, post_id: int, like_count: int) -> bool:
        """특정 게시글의 좋아요 숫자를 업데이트 """
        query = (
            update(Post)
            .where(Post.id == post_id)
            .values(like_count=like_count)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0

    async def increment_views(self, post_id: int) -> bool:
        query = (
            update(Post)
            .where(Post.id == post_id)
            .values(views=Post.views + 1)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
