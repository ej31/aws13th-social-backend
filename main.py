from fastapi import FastAPI
from routers import users, posts, comments, likes

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/post", tags=["Comments"])
app.include_router(likes.router, prefix="/post", tags=["Likes"])
@app.get("/")
def read_root():
    return {"message": "Cloud Community Server is Running!"}


# [PR 올리기 전 테스트 코드 - 확인 후 삭제]
from utils.data import load_data, save_data


@app.get("/test-utility")
def test_utility():
    # 1. users.json 파일 읽기
    users = load_data("users.json")

    # 2. 테스트 데이터 추가
    users.append({"test": "성공!"})

    # 3. users.json 파일에 저장
    save_data("users.json", users)

    return {"message": "utils/data.py 작동 성공! users.json을 확인하세요."}