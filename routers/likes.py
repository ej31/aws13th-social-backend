
from typing import Optional

from fastapi import APIRouter, HTTPException

from datetime import datetime


router = APIRouter(prefix="", tags=["likes"])

def _parse_dt(dt: Optional[str]) -> Optional[datetime]:
    # from/to가 들어오면 ISO8601(date-time)로 파싱.
    if not dt:
        return None
    try:
        return datetime.fromisoformat(dt)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date-time format (ISO8601 required)")


def _post_in_range():
    pass

# 좋아요 등록
@router.post("/posts/{post_id}/likes")
def like_post():
    pass

# 좋아요 취소
@router.delete("/posts/{post_id}/likes")
def unlike_post():
    pass


