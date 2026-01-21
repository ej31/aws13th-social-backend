from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models.user import User
from datetime import datetime


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, email: str, password: str, nickname: str, profile_image: str = None) -> User:
        """사용자 생성"""
        user = User(
            email=email,
            password=password,
            nickname=nickname,
            profileImage=profile_image
        )
        self.db.add(user)
        await self.db.flush()  # ID 생성을 위해 flush
        await self.db.refresh(user)  # 생성된 user 객체 새로고침
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        """ID로 사용자 조회"""
        result = await self.db.execute(
            select(User).where(User.userId == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """이메일로 사용자 조회"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def update(self, user_id: int, **kwargs) -> User | None:
        """사용자 정보 수정"""
        user = await self.get_by_id(user_id)
        if not user:
            return None

        # 업데이트할 필드만 수정
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        """사용자 삭제"""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        await self.db.delete(user)
        await self.db.flush()
        return True

    async def email_exists(self, email: str) -> bool:
        """이메일 중복 확인"""
        user = await self.get_by_email(email)
        return user is not None
