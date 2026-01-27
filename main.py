from contextlib import asynccontextmanager

import fastapi
import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import users, posts, comments,likes

# static 디렉토리가 없으면 생성
if not os.path.exists("static"):
    os.makedirs("static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 실행
    from common.database import engine
    async with engine.begin() as conn:
        # 테이블이 없으면 생성 (있으면 유지)
        from models.base import Base
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 서버 종료 시 실행 (필요하다면)

app = fastapi.FastAPI()

# 정적 파일 이미지를 외부에서 볼 수 있게 한다.
# "static" 폴더의 내용을 "/static" 주소로 연결하게 한다.
app.mount("/static",StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
@app.get("/")
async def healthcheck():
    return {"message":"api 서버가 정상적으로 동작하고 있습니다."}