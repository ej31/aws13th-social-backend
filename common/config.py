from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    users_json_path: str = "data/users.json"
    posts_json_path: str = "data/posts.json"
    comments_json_path: str= "data/comments.json"
    likes_json_path: str = "data/likes.json"
    upload_dir: str = "static/profiles"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24 * 14 # 14일
    HASHIDS_SALT: str

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()