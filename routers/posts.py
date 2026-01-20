from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Depends

from database import demo_db, generate_post_id, find_user_by_id, find_user_by_email
from utils.auth import hash_password, verify_password, create_access_token, get_current_user, REFRESH_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.data_validator import validate_and_process_image

router = APIRouter()

# 1. 게시글 작성 메서드 시작
@router.post("/posts")
async def post_posts(
        title : Annotated[str, Form()],
        contents : Annotated[str, Form()],
        contents_image : Annotated[UploadFile | None, File()] = None,
        user: dict = Depends(get_current_user)
):
    # 게시물에 첨부할 이미지 검증
    contents_image_url = None
    if contents_image:
        contents_image_url = await validate_and_process_image(contents_image)
    # post_id 부여
    post_id = generate_post_id()
    # DB 저장 ------------------------- 지금은 임시 데모용 DB에 등록 ---------
    demo_db.append({
        "post_id" : post_id,
        "title" : title,
        "contents" : contents,
        "contents_image_url" : contents_image_url,
        "posts_created_time" : datetime.now(timezone.utc).strftime('%Y.%m.%d - %H:%M:%S'),
        "posts_modified_time" : None
    })
    return {
        "status" : "success",
        "message" : "게시글 작성이 완료되었습니다.",
        "data" : {
            "post_id": post_id,
            "title" : title,
            "contents" : contents,
            "contents_image_url": contents_image_url,
            "author" : {
                "user_id" : user["user_id"],
                "email_address" : user["email_address"],
                "nickname" : user["nickname"]
            },
            "posts_created_time": datetime.now(timezone.utc).strftime('%Y.%m.%d - %H:%M:%S'),
        }
    }