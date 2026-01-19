from fastapi import FastAPI
from routers.users import router as users_router
import logging



app = FastAPI(
    title="Cloud Community API",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)
app.include_router(users_router)
