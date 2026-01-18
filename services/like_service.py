import uuid
from typing import Annotated
from fastapi import Depends, HTTPException
from datetime import datetime, timezone

from repositories.like_repository import LikeRepository
from repositories.post_repository import PostRepository


class LikeService:
    def __init__(self,
                 like_repository: Annotated[LikeRepository, Depends(LikeRepository)],
                 post_repository: Annotated[PostRepository, Depends(PostRepository)]):
        self.like_repo = like_repository
        self.post_repo = post_repository

    async def toggle_like(self, post_id: int, user_id: str) -> dict:
        """좋아요 토글 (없으면 등록, 있으면 취소)"""
        # 게시글 존재 확인
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        # 이미 좋아요를 눌렀는지 확인
        existing_like = self.like_repo.find_by_post_and_user(post_id, user_id)

        if existing_like:
            # [Unlike] 이미 있다면 삭제
            self.like_repo.delete(existing_like["like_id"])
            is_liked = False
            current_like_id = ""  # 삭제되었으므로 빈 값 혹은 None
        else:
            # [Like] 없다면 생성
            new_like_data = {
                "like_id": str(uuid.uuid4()),  # 고유 식별자 생성
                "post_id": post_id,
                "user_id": user_id,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            saved_like = self.like_repo.save(new_like_data)
            is_liked = True
            current_like_id = saved_like["like_id"]

        # PostRepository를 통해 게시글의 like_count 업데이트 (정합성 유지)
        like_count = self.like_repo.count_by_post_id(post_id)
        self.post_repo.update_like_count(int(post_id), like_count)

        # 정의한 스키마 구조에 맞춰 딕셔너리 반환
        return {
            "like_id": current_like_id,
            "post_id": str(post_id),
            "is_liked": is_liked,
            "like_count": like_count
        }

    async def get_like_status(self, post_id: int, user_id: str) -> dict:
        """현재 사용자의 좋아요 여부 및 개수 확인 (조회 전용)"""
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        existing_like = self.like_repo.find_by_post_and_user(post_id, user_id)
        like_count = self.like_repo.count_by_post_id(post_id)

        return {
            "like_id": existing_like["like_id"] if existing_like else "",
            "post_id": str(post_id),
            "is_liked": True if existing_like else False,
            "like_count": like_count
        }