from fastapi import APIRouter

router = APIRouter()

@router.post("/{postId}/likes")
def do_like(postId: int):
    return{
        "status": "success",
        "data": {
            "likeCount": 2
        }
    }