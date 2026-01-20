from pathlib import Path

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

ROOT_DIR = Path(__file__).resolve().parent

class AllSettings(BaseSettings):
    # jwt토큰 검증 pydantic모델, 토큰 기본값은 2시간
    SECRET_KEY: str =Field(..., min_length=32)
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # db 세팅
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_CHARSET: str = "utf8mb4"

    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", ROOT_DIR / ".env_DB")
    )



jwt_settings = AllSettings()