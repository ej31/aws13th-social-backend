from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers import users, posts, comments, likes
from utils.database import init_pool, close_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(likes.router)
app.include_router(posts.router)
app.include_router(comments.router)
