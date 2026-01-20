# main.py
from fastapi import FastAPI
from app.routers import users, posts, comments, likes, auth

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(auth.router)
