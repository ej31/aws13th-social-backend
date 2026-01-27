from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings


BASE_DIR = Path(__file__).resolve().parent
env_db_path = BASE_DIR / ".env"

# verbose=True를 넣으면 로드 과정을 상세히 출력해줍니다.
if load_dotenv(dotenv_path=env_db_path, verbose=True):
    print(f"✅ .env 로드 성공! (경로: {env_db_path})")
else:
    print(f"❌ .env 로드 실패! (파일이 해당 경로에 있는지 확인하세요: {env_db_path})")

class AllSettings(BaseSettings):
    # jwt토큰 검증 pydantic모델, 토큰 기본값은 2시간
    SECRET_KEY: str =Field(..., min_length=32)
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

jwt_settings = AllSettings()