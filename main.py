from typing import Annotated, Optional
from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel, Field
from starlette import status
from pydantic import EmailStr
from routers import posts, users, comments, likes

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.get("/")
async def read_root():
    return {"root": "루트입니다"}
