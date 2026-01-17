from pydantic import Field
from pathlib import Path
from pydantic_settings import SettingsConfigDict, BaseSettings

#jwt토큰 검증 pydantic모델, 토큰 기본값은 2시간
class JwtSettings(BaseSettings):
    SECRET_KEY: str =Field(..., min_length=32)
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    model_config = SettingsConfigDict(env_file = Path(__file__).resolve().parents[1] / ".env")

jwt_settings = JwtSettings()