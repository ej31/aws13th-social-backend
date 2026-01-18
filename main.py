from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from routers import users, posts, comments, likes

app = FastAPI()

os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router, prefix="", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/posts/{post_id}/comments", tags=["Comments"])
app.include_router(likes.router, prefix="/posts/{post_id}/likes", tags=["Likes"])

@app.get("/")
def read_root():
    return {"message": "Cloud Community Server is Running!"}