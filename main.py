from fastapi import FastAPI
from routers.users import router as users_router
from routers.posts import router as posts_router
from routers.likes import router as likes_router
from routers.comments import router as comments_router
from routers.auth import router as auth_router

from dotenv import load_dotenv
app = FastAPI()

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(likes_router)
app.include_router(comments_router)
app.include_router(auth_router)

load_dotenv() # .env에서 키값 등 접근