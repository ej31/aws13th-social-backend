from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"root": "루트입니다"}

@app.post("/auth/signup")
async def signup():
    return {"signup": "ok"}

@app.post("/auth/login")
async def login():
    return {"login": "ok"}

@app.post("/auth/logout")
async def logout():
    return {"logout": "ok"}

@app.get("/users/me")
async def read_users_me():
    return {"username": "admin", "email": "", "password": ""}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.patch("/users/me")
async def update_user(user_id: int):
    return {"user_id": user_id}

@app.delete("/users/me")
async def delete_user(user_id: int):
    return {"user_id": user_id}

@app.post("/posts")
async def create_post(title: str, content: str):
    return {"title": title, "content": content}

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return {"post_id": post_id}
@app.patch("/posts/{post_id}")
async def update_post(post_id: int, title: str, content: str):
    return {"post_id": post_id, "title": title, "content": content}
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return {"post_id": post_id}

@app.get("/posts/{post_id}/comments")
async def get_post_comments(post_id: int):
    return {"post_id": post_id, "comments": []}
