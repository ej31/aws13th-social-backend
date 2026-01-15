from typing import Annotated, Optional
from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel, Field
from starlette import status
from pydantic import EmailStr

app = FastAPI()

@app.get("/")
async def read_root():
    """
    루트 경로에 대한 요청에 간단한 JSON 응답을 반환합니다.
    
    Returns:
        dict: {"root": "루트입니다"} 형태의 응답 객체.
    """
    return {"root": "루트입니다"}