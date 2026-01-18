from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def do_like(post_id: int):
    return{
        "status": "success",
        "data": {
            "postId": post_id,
            "likeCount": 2
        }
    }