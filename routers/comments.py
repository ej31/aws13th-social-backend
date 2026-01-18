from fastapi import APIRouter

router = APIRouter(tags=["comments"])

@router.get("posts/{post_id}/comments")
def get_comments(post_id: int):
    return get_comments(post_id)

@router.post("/posts/{post_id}/comments")
def post_comments(post_id: int):
    return post_comments(post_id)

@router.patch("/comments/{comment_id}")
def update_comments(comment_id: int):
    return comment_id

@router.delete("/comments/{comment_id}")
def delete_comments(comment_id: int):
    return comment_id

@router.get("/comments/me")
def get_me():
    return get_me()
