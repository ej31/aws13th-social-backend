"""
애플리케이션 설정
- MariaDB 연결 정보 포함
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cache


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 애플리케이션 기본 설정
    PROJECT_NAME: str = "FastAPI Community"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # 보안 설정
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database 설정 (MariaDB)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_CHARSET: str = "utf8mb4"
    
    # Connection Pool 설정
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600  # 1시간
    DB_POOL_PRE_PING: bool = True
    
    # 기존 JSON 방식 (마이그레이션 완료 후 제거 예정)
    DATA_DIR: str = "./data"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def database_url(self) -> str:
        """
        PyMySQL 연결 문자열 생성
        """
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            f"?charset={self.DATABASE_CHARSET}"
        )


@cache
def get_settings() -> Settings:
    """설정 싱글톤 인스턴스 반환"""
    return Settings()