from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from common.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True # SQL 로그 확인
)

AsyncSessionLocal = async_sessionmaker(
    bind= engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#db 의존성 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session