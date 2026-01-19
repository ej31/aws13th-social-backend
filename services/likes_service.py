import uuid
from datetime import datetime,timezone
from models.like import LikeCreate, LikeResponse
from repositories.likes_repo import get_likes, save_likes

def toggle_like_service(user_id: str , like_in: LikeCreate):
    likes = get_likes()

    existing_like = next((l for l in likes if l["user_id"] == user_id
                          and l["target_type"] == like_in.target_type
                          and l["target_id"] == like_in.target_id), None)
    if existing_like:
        likes.remove(existing_like)
        is_liked = False
        like_id = existing_like["like_id"]
    else:
        is_liked = True
        new_like_data = {
            "like_id": str(uuid.uuid4()),
            "user_id": user_id,
            "target_type": like_in.target_type,
            "target_id": like_in.target_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        likes.append(new_like_data)
        like_id = new_like_data["like_id"]

    save_likes(likes)

    current_total = len([l for l in likes if l["target_id"] == like_in.target_id
                         and l["target_type"] == like_in.target_type])

    return LikeResponse(
        target_type=like_in.target_type,
        target_id=like_in.target_id,
        like_id=like_id,
        user_id=user_id,
        is_liked=is_liked,
        total_likes=current_total
    )

#
# def write_like_post(post_id :str, current_user:dict) -> dict:
#
#     return
#
# def write_like_comment(comment_id: str, current_user: dict) -> dict:
#
#     return
#
# def get_like_post(post_id: str, current_user: dict) -> dict:
#
#     return
#
# def get_like_comment(comment_id: str, current_user: dict) -> dict:
#
#     return
#
# def delete_post_commet(post_id: str, current_user: dict) -> dict:
#     return
#
# def delete_like_comment(comment_id: str, current_user: dict) -> dict:
#     return
#
# def get_my_likes(current_user: dict) -> dict:
#     return
