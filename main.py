from fastapi import FastAPI
from data import models
from data.database import engine

import routers.auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}