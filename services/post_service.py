from typing import Optional

import uuid

from models.post import Post, PostInternal, PostQuery
from fastapi import HTTPException
from repositories.posts_repo import get_post, save_post
from datetime import datetime

def write_posts(data: Post, current_user: dict):
    posts = get_post()

    if any(u["title"] == data.title for u in posts):
        raise HTTPException(400, "이미 존재하는 게시물 타이틀")

    post_created_at = datetime.now()

    my_post = PostInternal(
        user_id=current_user["user_id"],
        post_id=str(uuid.uuid4()),
        view_count=0,
        title=data.title,
        content=data.content,
        media=data.media,
        created_at=post_created_at
    ).model_dump(mode="json")

    posts.append(my_post)
    save_post(posts)
    return my_post

def get_user_post(post_id: str) -> dict:
    posts = get_post()
    user_post = next((u for u in posts if u["post_id"] == post_id), None)
    if user_post is None:
        raise HTTPException(status_code=404, detail="해당 게시물을 찾을수 없습니다")

    if "view_count" not in user_post:
        user_post["view_count"] = 0
    user_post["view_count"] += 1
    save_post(posts)
    return user_post

def update_my_post(post_id:str, post_dict: dict, current_user: dict) -> dict:
    posts = get_post()
    user_post = next((u for u in posts if u["post_id"] == post_id), None)
    if user_post is None:
        raise HTTPException(status_code=404, detail="해당 게시물을 찾을수 없습니다")

    if user_post["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="게시물을 수정할 권한이 없습니다.")

    # index = next(
    #     (i for i, u in enumerate(posts) if u["user_id"] == current_user["user_id"]),
    #     None,
    # )
    # if index is None:
    #     raise HTTPException(status_code=404, detail="해당 유저가 없습니다")

    index = posts.index(user_post)
    posts[index].update(post_dict)
    save_post(posts)
    return posts[index]


def delete_my_post(post_id:str,current_user: dict) -> None:
    posts = get_post()
    target_post = next((u for u in posts if u["post_id"] == post_id), None)
    if not target_post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    if target_post["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="본인의 게시물만 삭제할 수 있습니다."
        )
    updated_posts = [p for p in posts if p["post_id"] != post_id]
    save_post(updated_posts)

def query_post(param: PostQuery, get_optional_user: Optional[dict]) -> dict:
    data = get_post()

    if get_optional_user :
        return data
    else:
        pass

    if param.search:
        data = [post for post in data if param.search in data["title"]]

    reverse = True if param.sort_order == "desc" else False
    data = sorted(data, key=lambda x: x[param.sort_by], reverse=reverse)
    paged_data = data[param.start_idx: param.end_idx]

    return {
        "total": len(data),
        "page": param.page,
        "size": param.size,
        "results": paged_data
    }