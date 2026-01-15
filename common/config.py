from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_path: str = "data/users.json"
    upload_dir: str = "static/profiles"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    HASHIDS_SALT : str

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()