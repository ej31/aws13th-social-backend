from typing import Annotated, Optional
from datetime import datetime, timezone, timedelta
import json,os,uuid
from fastapi import FastAPI, Form, HTTPException, Depends, status, APIRouter
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from jose import jwt

#
# import json
# from pathlib import Path
# from fastapi import HTTPException
#
# POSTS_FILE = Path("posts.json")
#
# def load_posts():
#     if POSTS_FILE.exists():
#         return json.loads(POSTS_FILE.read_text())
#     return []
#
# def save_posts(posts):
#     POSTS_FILE.write_text(json.dumps(posts, indent=2))
#
# `@app.get`("/posts/{post_id}")
# async def get_post(post_id: int):
#     posts = load_posts()
#     post = next((p for p in posts if p["id"] == post_id), None)
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return post
app = FastAPI()
router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/posts")
async def create_post(title: str, content: str):
    return {"title": title, "content": content}

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    return {"post_id": post_id}
@router.patch("/posts/{post_id}")
async def update_post(post_id: int, title: str, content: str):
    return {"post_id": post_id, "title": title, "content": content}
@router.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return {"post_id": post_id}