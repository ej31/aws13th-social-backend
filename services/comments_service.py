from datetime import datetime
from models.comment import Comment, CommentInternal, CommentResponse
from models.post import Post
from repositories.comments_repo import get_comments, save_comments
from fastapi import HTTPException

from repositories.posts_repo import get_post


def write_comments(post_id:str,data: Comment, current_user : dict):
    posts = get_post()
    comments = get_comments()

    if any(p["post_id"] != post_id for p in posts):
        raise HTTPException(400, "Post ID not valid")
    #
    # if any(u["comment_id"] ==  for data. u in comments):
    #     raise HTTPException(400, "이미 존재하는 코멘트 입니다.")

    comment_created_at = datetime.now()

    my_comment = CommentResponse(
        user_id = current_user["user_id"],
        post_id = post_id,
        content=data.content,
        comment_id=data.comment_id,
        created_at = comment_created_at
    ).model_dump("json")

    save_comments(my_comment)

    return my_comment


