from fastapi import FastAPI, Depends

from routers import users, posts
from schemas.commons import PostId, CommentId, Page

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)





# ----- COMMENTS ----- #

# List all comments for a post
@app.get("/posts/{post_id}/comments")
async def get_comments(post_id: PostId, page: Page):
    pass


# post comment
@app.post("/posts/{post_id}/comments")
async def post_comment(post_id: PostId):
    pass


# edit comment
@app.patch("/posts/{post_id}/comments/{comment_id}")
async def update_comment(post_id: PostId, comment_id: CommentId):
    pass


# delete comment
@app.delete("/posts/{post_id}/comments/{comment_id}")
async def delete_comment(post_id: PostId, comment_id: CommentId):
    pass


# comment list I wrote
@app.get("/comments/me")
async def get_comments_mine(page: Page):
    pass


# ----- LIKES ----- #

# register like
@app.post("/posts/{post_id}/likes")
async def post_like(post_id: PostId):
    pass


# delete like
@app.delete("/posts/{post_id}/likes")
async def delete_like(post_id: PostId):
    pass


# check like status
@app.get("/posts/{post_id}/likes")
async def get_likes_status(post_id: PostId):
    pass


# post list I liked
@app.get("/posts/liked")
async def get_posts_liked(page: Page):
    pass
