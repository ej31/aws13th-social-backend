from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.refresh_token import RefreshToken
from datetime import datetime, timezone


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, token_hash: str, user_id: int, expires_at: datetime) -> RefreshToken:
        """리프레시 토큰 생성"""
        token = RefreshToken(
            tokenHash=token_hash,
            userId=user_id,
            expiresAt=expires_at
        )
        self.db.add(token)
        await self.db.flush()
        await self.db.refresh(token)
        return token

    async def get_by_id(self, token_id: int) -> RefreshToken | None:
        """ID로 토큰 조회"""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.tokenId == token_id)
        )
        return result.scalar_one_or_none()

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        """토큰 해시로 조회"""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.tokenHash == token_hash)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[RefreshToken]:
        """특정 사용자의 모든 토큰 조회"""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.userId == user_id)
        )
        return list(result.scalars().all())

    async def delete(self, token_id: int) -> bool:
        """토큰 삭제 (ID로)"""
        token = await self.get_by_id(token_id)
        if not token:
            return False

        await self.db.delete(token)
        await self.db.flush()
        return True

    async def delete_by_hash(self, token_hash: str) -> bool:
        """토큰 삭제 (해시로)"""
        token = await self.get_by_hash(token_hash)
        if not token:
            return False

        await self.db.delete(token)
        await self.db.flush()
        return True

    async def delete_by_user_id(self, user_id: int) -> int:
        """특정 사용자의 모든 토큰 삭제 (회원 탈퇴 시)"""
        result = await self.db.execute(
            delete(RefreshToken).where(RefreshToken.userId == user_id)
        )
        await self.db.flush()
        return result.rowcount

    async def delete_expired(self) -> int:
        """만료된 토큰 모두 삭제"""
        # timezone-aware datetime으로 비교
        now = datetime.now(timezone.utc).replace(tzinfo=None)  # DB는 naive이므로 naive로 변환
        result = await self.db.execute(
            delete(RefreshToken).where(RefreshToken.expiresAt < now)
        )
        await self.db.flush()
        return result.rowcount

    async def is_valid(self, token_hash: str) -> bool:
        """토큰이 유효한지 확인 (존재하고 만료되지 않았는지)"""
        token = await self.get_by_hash(token_hash)
        if not token:
            return False

        # timezone-aware datetime으로 비교
        now = datetime.now(timezone.utc)
        expires_at = token.expiresAt
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        return expires_at > now
