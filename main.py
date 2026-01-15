from typing import Annotated, Optional
from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel, Field
from starlette import status
from pydantic import EmailStr

app = FastAPI()

@app.get("/")
async def read_root():
    return {"root": "루트입니다"}
