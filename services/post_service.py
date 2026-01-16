import uuid

from models.post import Post, PostInternal
from fastapi import HTTPException
from repositories.posts_repo import get_post, save_post


def write_posts(data: Post, current_user: dict):
    posts = get_post()

    if any(u["title"] == data.title for u in posts):
        raise HTTPException(400, "이미 존재하는 게시물 타이틀")

    my_post = PostInternal(
        user_id=current_user["user_id"],
        post_id=str(uuid.uuid4()),
        title=data.title,
        content=data.content,
        media=data.media,
        created_at=data.created_at
    ).model_dump(mode="json")

    posts.append(my_post)
    save_post(my_post)

    return my_post