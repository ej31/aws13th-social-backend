from datetime import datetime, timezone
from typing import Optional
import uuid
from fastapi import HTTPException
from models.comment import Comment, CommentResponse
from repositories.comments_repo import get_all_comments, get_comment_by_id
from repositories.posts_repo import get_all_posts, get_post_by_id


def write_comments(db, post_id:str, data: Comment, current_user : dict):
    try:
        with db.cursor() as cursor:
            posts = get_post_by_id(db, post_id)
            if not any(p["post_id"] == post_id for p in posts):
                raise HTTPException(400, "Post ID not valid")
            comment_created_at = datetime.now(timezone.utc)
            user_id = current_user["user_id"]
            comment_id = str(uuid.uuid4())
            content = data.content

            insert_sql = "INSERT INTO comments (comment_id, post_id, user_id,content, created_at) VALUES (%s, %s, %s, %s, %s)"
            param = (comment_id, post_id, user_id, content, comment_created_at)
            cursor.execute(insert_sql, param)
            my_comment = CommentResponse(
                user_id = user_id,
                post_id = post_id,
                content=  content,
                comment_id= comment_id,
                created_at = comment_created_at
            ).model_dump(mode="json")
        db.commit()
        return my_comment

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print(f"Service Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_usr_comments(db, post_id:str, get_optional_user: Optional[dict] = None):
    all_data = get_all_comments(db)

    post_comments = [c for c in all_data if c["post_id"] == post_id]

    if not post_comments:
        raise HTTPException(status_code=404, detail="해당 게시물의 댓글을 찾을 수 없습니다.")

    if get_optional_user:
        user_id = get_optional_user.get("user_id")
        mine_only = [c for c in post_comments if c.get("user_id") == user_id]
        return mine_only

    return post_comments

def update_user_comments(db,comment_id:str, data: Comment, current_user : dict):
    all_data = get_comment_by_id(db, comment_id)
    user_comments = next((u for u in all_data if u["comment_id"] == comment_id), None)
    if user_comments is None:
        raise HTTPException(status_code=404, detail="해당 게시물을 찾을수 없습니다")
    if user_comments["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail=" 댓글을 수정할 권한이 없습니다.")

    index = all_data.index(user_comments)
    all_data[index]["content"] = data.content
    return all_data[index]

def delete_user_comments(db, comment_id:str, current_user : dict ):
    comments = get_comment_by_id(db, comment_id)
    target_comment = next((u for u in comments if u["comment_id"] == comment_id), None)
    if not target_comment:
        raise HTTPException(status_code=404, detail="코멘트를 찾을 수 없습니다.")

    if target_comment["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="본인의 댓글만 삭제할 수 있습니다."
        )

    updated_posts = [p for p in comments if p["comment_id"] != comment_id]

def get_my_comment(db, current_user : dict):
    all_data = get_all_comments(db)
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="인증이 필요합니다")
    return [c for c in all_data if c.get("user_id") == user_id]