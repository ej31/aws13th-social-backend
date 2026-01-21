import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 필수 환경변수 검증
if not DB_USER:
    raise RuntimeError("DB_USER 환경변수가 설정되지 않았습니다.")
if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD 환경변수가 설정되지 않았습니다.")
if not DB_NAME:
    raise RuntimeError("DB_NAME 환경변수가 설정되지 않았습니다.")

# SQLAlchemy 데이터베이스 URL (aiomysql 사용)
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",  # 환경변수로 SQL 로그 제어
    pool_pre_ping=True,  # 연결 확인
    pool_recycle=3600,  # 1시간마다 연결 재활용
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 모델 베이스 클래스
Base = declarative_base()


# 데이터베이스 세션 의존성 (FastAPI에서 사용)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# 데이터베이스 초기화 함수
async def init_db():
    """모든 테이블 생성"""
    # 모든 모델 import (테이블 생성을 위해 필요)
    from models import User, Post, Comment, Like, RefreshToken

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 데이터베이스 연결 종료
async def close_db():
    """데이터베이스 연결 종료"""
    await engine.dispose()
