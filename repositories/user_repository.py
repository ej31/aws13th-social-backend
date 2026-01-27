from typing import Optional

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def find_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def add(self, user_obj: User) -> User:
        # 기존 유저에 대한 중복 체크는 DB의 유니크 조건이 처리하게 한다.
        self.db.add(user_obj)
        await self.db.commit()  # DB에 저장
        await self.db.refresh(user_obj)  # 생성된 Id 값 등을 객체에 동기화
        return user_obj

    async def update(self, user_obj: User) -> User:
        # SQLAlchemy는 세션 내 객체의 변경을 감지하므로 commit만 하면 됨 (변경감지)
        await self.db.commit()
        await self.db.refresh(user_obj)
        # 저장한 데이터 반환
        return user_obj

    async def delete_by_email(self, email: str) -> bool:
        query = delete(User).where(User.email == email)

        result = await self.db.execute(query)

        await self.db.commit()

        return result.rowcount > 0
