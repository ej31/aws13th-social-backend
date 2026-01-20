import json
import os
from typing import List, Optional

from common.config import settings


class LikeRepository:
    def __init__(self):
        self.file_path = settings.likes_json_path
        # 데이터 폴더가 없으면 생성
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # 파일이 없으면 빈 리스트로 초기화
        if not os.path.exists(self.file_path):
            self._save_data([])

    def _load_data(self) -> List[dict]:
        """JSON 파일에서 좋아요 목록 로드"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[dict]):
        """JSON 파일에 데이터 저장"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def find_all(self) -> List[dict]:
        """전체 좋아요 목록 조회"""
        return self._load_data()

    def find_by_post_and_user(self, post_id: int, user_id: int) -> Optional[dict]:
        """특정 유저가 특정 게시글에 남긴 좋아요 확인 """
        likes = self._load_data()
        for like in likes:
            if like["post_id"] == post_id and str(like["user_id"]) == str(user_id):
                return like
        return None

    def count_by_post_id(self, post_id: int) -> int:
        """게시글별 총 좋아요 개수 집계 """
        likes = self._load_data()
        return len([like for like in likes if like["post_id"] == post_id])

    def save(self, like_data: dict) -> dict:
        """좋아요 정보 저장 (Insert)"""
        likes = self._load_data()
        likes.append(like_data)
        self._save_data(likes)
        return like_data

    def delete(self, like_id: str) -> bool:
        """좋아요 취소 (Delete)"""
        likes = self._load_data()
        new_likes = [like for like in likes if like["like_id"] != like_id]

        if len(likes) == len(new_likes):
            return False  # 삭제할 대상이 없음

        self._save_data(new_likes)
        return True

    def get_next_id(self):
        """다음에 부여할 게시물의 ID를 반환"""
        likes = self._load_data()
        return max([p["like_id"] for p in likes],default=0)+1