from datetime import datetime, timezone
from typing import Optional

import uuid
from fastapi import HTTPException

from core.db_connection import get_db_connection
from models.post import Post, PostQuery, PostPublic
from repositories.posts_repo import get_post, save_post, get_post_by_id


def write_posts(data: Post, current_user: dict):
    con = None
    try:
        con = get_db_connection()
        with con.cursor() as cursor:
            check_sql = "SELECT * FROM posts WHERE title = %s"
            cursor.execute(check_sql, (data.title,))
            if cursor.fetchone():
                raise HTTPException(status_code=400,detail="이미 존재하는 게시물 타이틀")

            user_id = current_user["user_id"]
            post_id = str(uuid.uuid4())
            post_created_at = datetime.now(timezone.utc)

            insert_sql = "INSERT INTO posts (user_id, post_id,title, content, media, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
            param =(user_id, post_id, data.title, data.content, post_created_at)
            cursor.execute(insert_sql, param)

            post_response= PostPublic(
                title=data.title,
                content=data.content,
                media=data.media,
            )
        con.commit()
        return post_response
    except Exception as e:
        con.rollback()
        raise e
    finally:
        if con :
            con.close()

def get_user_post(post_id: str) -> dict:
    user_post = get_post_by_id(post_id)
    if not user_post:
        raise HTTPException(status_code=404, detail="해당 게시물을 찾을수 없습니다.")

    if "view_count" not in user_post:
        user_post["view_count"] = 0

    sql = "update posts set view_count = view_count + 1 where post_id = %s"


    return user_post


def update_my_post(post_id:str, post_dict: dict, current_user: dict) -> dict:
    posts = get_post()
    user_post = next((u for u in posts if u["post_id"] == post_id), None)
    if user_post is None:
        raise HTTPException(status_code=404, detail="해당 게시물을 찾을수 없습니다")

    if user_post["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="게시물을 수정할 권한이 없습니다.")

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
        search_item = param.search.lower()
        data = [post for post in data if search_item in post.get("title","").lower()]

    if not data:
        raise HTTPException(
            status_code=404,
            detail= f"검색어 {param.search}에 해당하는 게시물을 찾을수 없습니다."
        )

    reverse = True if param.sort_order == "desc" else False
    data = sorted(data, key=lambda x: x[param.sort_by], reverse=reverse)
    paged_data = data[param.start_idx: param.end_idx]

    return {
        "total": len(data),
        "page": param.page,
        "size": param.size,
        "results": paged_data
    }
