from typing import Annotated, Optional
from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel, Field
from starlette import status
from pydantic import EmailStr

app = FastAPI()


@app.post("/posts")
async def create_post(title: str, content: str):
    """
    제목과 내용을 포함하는 게시물 표현을 생성합니다.
    
    Parameters:
        title (str): 게시물의 제목
        content (str): 게시물의 본문 내용
    
    Returns:
        dict: 키 `title`과 `content`를 가진 생성된 게시물 사전
    """
    return {"title": title, "content": content}

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """
    게시물을 ID로 조회하여 해당 ID를 포함한 딕셔너리를 반환합니다.
    
    Returns:
        dict: 키 'post_id'에 조회한 게시물 ID를 담은 사전
    """
    return {"post_id": post_id}
@app.patch("/posts/{post_id}")
async def update_post(post_id: int, title: str, content: str):
    """
    지정한 ID의 게시물을 주어진 제목과 내용으로 업데이트하고 업데이트된 게시물 정보를 반환합니다.
    
    Parameters:
        post_id (int): 업데이트할 게시물의 식별자.
        title (str): 게시물의 새로운 제목.
        content (str): 게시물의 새로운 내용.
    
    Returns:
        dict: 업데이트된 게시물 정보를 담은 사전. 키는 `post_id`, `title`, `content` 입니다.
    """
    return {"post_id": post_id, "title": title, "content": content}
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    """
    게시물을 삭제하고 삭제된 게시물의 ID를 반환합니다.
    
    Parameters:
        post_id (int): 삭제할 게시물의 고유 식별자.
    
    Returns:
        dict: 키 `'post_id'`에 삭제된 게시물의 ID를 담은 사전.
    """
    return {"post_id": post_id}