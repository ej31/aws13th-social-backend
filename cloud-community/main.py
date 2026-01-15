from fastapi import FastAPI
from routers import users, likes, posts, comments

app=FastAPI()

@app.get("/")
def root():
    return {"status" : "ok"}