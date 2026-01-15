from typing import Annotated, Optional
from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel, Field
from starlette import status
from pydantic import EmailStr

app = FastAPI()


@app.post("/posts")
async def create_post(title: str, content: str):
    return {"title": title, "content": content}

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return {"post_id": post_id}
@app.patch("/posts/{post_id}")
async def update_post(post_id: int, title: str, content: str):
    return {"post_id": post_id, "title": title, "content": content}
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return {"post_id": post_id}