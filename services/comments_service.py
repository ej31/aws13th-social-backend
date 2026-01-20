from datetime import datetime,timezone
import uuid
from models.comment import Comment, CommentResponse
from repositories.comments_repo import get_comments, save_comments
from fastapi import HTTPException
from typing import Annotated, List, Optional

from repositories.posts_repo import get_post


def write_comments(post_id:str, data: Comment, current_user : dict):
    posts = get_post()
    comments = get_comments()

    if not any(p["post_id"] == post_id for p in posts):
        raise HTTPException(400, "Post ID not valid")

    comment_created_at = datetime.now(timezone.utc)

    my_comment = CommentResponse(
        user_id = current_user["user_id"],
        post_id = post_id,
        content=data.content,
        comment_id=str(uuid.uuid4()),
        created_at = comment_created_at
    ).model_dump(mode="json")

    comments.append(my_comment)
    save_comments(comments)
    return my_comment

def get_usr_comments(post_id:str, get_optional_user: Optional[dict] = None):
    all_data = get_comments()

    post_comments = [c for c in all_data if c["post_id"] == post_id]

    if not post_comments:
        raise HTTPException(status_code=404, detail="해당 게시물의 댓글을 찾을 수 없습니다.")

    if get_optional_user:
        user_id = get_optional_user.get("user_id")
        mine_only = [c for c in post_comments if c.get("user_id") == user_id]
        return mine_only

    return post_comments

def update_user_comments(comment_id:str, data: Comment, current_user : dict):
    all_data = get_comments()
    user_comments = next((u for u in all_data if u["comment_id"] == comment_id), None)
    if user_comments is None:
        raise HTTPException(status_code=404, detail="해당 게시물을 찾을수 없습니다")
    if user_comments["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail=" 댓글을 수정할 권한이 없습니다.")

    index = all_data.index(user_comments)
    all_data[index]["content"] = data.content
    save_comments(all_data)
    return all_data[index]

def delete_user_comments(comment_id:str, current_user : dict ):
    comments = get_comments()
    target_comment = next((u for u in comments if u["comment_id"] == comment_id), None)
    if not target_comment:
        raise HTTPException(status_code=404, detail="코멘트를 찾을 수 없습니다.")

    if target_comment["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="본인의 댓글만 삭제할 수 있습니다."
        )

    updated_posts = [p for p in comments if p["comment_id"] != comment_id]
    save_comments(updated_posts)

def get_my_comment(current_user : dict):
    all_data = get_comments()
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="인증이 필요합니다")
    return [c for c in all_data if c.get("user_id") == user_id]