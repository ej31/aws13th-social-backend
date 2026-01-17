from fastapi import FastAPI
from routers.users import router as users_router

app = FastAPI(
    title="Cloud Community API",
    version="1.0.0"
)

app.include_router(users_router)
