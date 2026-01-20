from fastapi import FastAPI
from routers import users

app = FastAPI()



app.include_router(users.router,prefix="/users",tags=["Users"])
@app.get("/")
def read_root():
    return {"message": "Cloud Community Server is Running!"}