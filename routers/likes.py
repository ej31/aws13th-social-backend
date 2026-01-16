from fastapi import APIRouter

router = APIRouter(tags=["likes"])

@router.get("/posts/{post_id}/likes")
def like_post(post_id: int):
    return like_post(post_id)

@router.get("/comments/{comment_id}/likes")
def like_comment(comment_id: int):
    return like_comment(comment_id)

@router.get("/likes/me")
def like_me():
    return like_me()

@router.post("posts/{post_id}/likes")
def like_post(post_id: int):
    return like_post(post_id)

@router.post("/comments/{comment_id}/likes")
def like_comment(comment_id: int):
    return like_comment(comment_id)

@router.delete("/posts/{post_id}/likes")
def like_post(post_id: int):
    return like_post(post_id)

@router.delete("/comments/{comment_id}/likes")
def like_comment(comment_id: int):
    return like_comment(comment_id)