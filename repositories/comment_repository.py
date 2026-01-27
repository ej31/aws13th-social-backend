import os
import json
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from common.config import settings
from models.base import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all_by_post_id(self, post_id: int) -> list[Comment]:
        """특정 게시글에 속한 모든 댓글 조회 (최신순)"""
        # SQL: SELECT * FROM comments WHERE post_id = :post_id ORDER BY created_at DESC
        from sqlalchemy import select
        query =  select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_by_id(self, comment_id: int) -> Optional[Comment]:
        """ID로 특정 댓글 조회"""
        from sqlalchemy import select
        result = await self.db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalars().first()

    async def add(self, comment_obj: Comment) -> Comment:
        """새로운 댓글 생성 (ID 자동 생성)"""
        self.db.add(comment_obj)
        await self.db.commit()
        await self.db.refresh(comment_obj)
        return comment_obj

    async def update(self, comment_obj: Comment) -> Comment:
        """기존 댓글 수정"""
        # SQLAlchemy 객체는 세션 내에서 변경 사항이 추적되므로 commit만 수행
        await self.db.commit()
        await self.db.refresh(comment_obj)
        return comment_obj

    async def delete(self, comment_id: int) -> bool:
        """댓글 삭제"""
        from sqlalchemy import delete
        query = delete(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
