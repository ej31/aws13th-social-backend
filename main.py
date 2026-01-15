import fastapi
from starlette.staticfiles import StaticFiles

from routers import users

app = fastapi.FastAPI()

# 정적 파일 이미지를 외부에서 볼 수 있게 한다.
# "static" 폴더의 내용을 "/static" 주소로 연결하게 한다.
app.mount("/static",StaticFiles(directory="static"), name="static")

app.include_router(users.router)

@app.get("/")
async def healthcheck():
    return {"message":"api 서버가 정상적으로 동작하고 있습니다."}