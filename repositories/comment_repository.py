from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from models.comment import Comment
from typing import List


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, post_id: int, user_id: int, content: str) -> Comment:
        """댓글 생성"""
        comment = Comment(
            postId=post_id,
            userId=user_id,
            content=content
        )
        self.db.add(comment)
        await self.db.flush()
        await self.db.refresh(comment)
        return comment

    async def get_by_id(self, comment_id: int) -> Comment | None:
        """ID로 댓글 조회"""
        result = await self.db.execute(
            select(Comment).where(Comment.commentId == comment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_post_id(self, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        """특정 게시글의 댓글 조회"""
        result = await self.db.execute(
            select(Comment)
            .where(Comment.postId == post_id)
            .order_by(Comment.createdAt)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        """특정 사용자의 댓글 조회"""
        result = await self.db.execute(
            select(Comment)
            .where(Comment.userId == user_id)
            .order_by(desc(Comment.createdAt))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, comment_id: int, content: str) -> Comment | None:
        """댓글 수정"""
        comment = await self.get_by_id(comment_id)
        if not comment:
            return None

        comment.content = content

        await self.db.flush()
        await self.db.refresh(comment)
        return comment

    async def delete(self, comment_id: int) -> bool:
        """댓글 삭제"""
        comment = await self.get_by_id(comment_id)
        if not comment:
            return False

        await self.db.delete(comment)
        await self.db.flush()
        return True
