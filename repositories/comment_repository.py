import os
import json
from typing import Optional

from common.config import settings

class CommentRepository:
    def __init__(self) -> None:
        self.file_path = settings.comments_json_path
        if not os.path.exists(self.file_path):
            self._save_all([])

    def _load_all(self) -> list[dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _save_all(self,comments) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(comments, f, indent=4, ensure_ascii=False)

    def find_all_by_post_id(self,post_id: int) -> list[dict]:
        """특정 게시글에 속한 모든 댓글 가져오기"""
        comments = self._load_all()
        return [c for c in comments if int(c["post_id"]) == int(post_id)]

    def find_by_id(self, comment_id: int) -> Optional[dict]:
        comments = self._load_all()
        for comment in comments:
            if int(comment["comment_id"]) == int(comment_id):
                return comment
        return None

    def save(self,comment_data:dict) -> dict:
        """코멘트 id가 없을 시 새로 게시물 생성 만약 있을 시 수정된 데이터만 저장"""
        comments = self._load_all()

        if "comment_id" not in comment_data or comment_data["comment_id"] is None:
            max_id = max((int(c["comment_id"]) for c in comments), default=0)
            comment_data["comment_id"] = max_id + 1
            comments.append(comment_data)

        else:
            for i,c in enumerate(comments):
                if int(c["comment_id"]) == int(comment_data["comment_id"]):
                    comments[i] = comment_data
                    break
            else:
                raise ValueError(f"댓글 ID {comment_data['comment_id']}를 찾을 수 없습니다.")
        self._save_all(comments)
        return comment_data

    def delete(self,comment_id: int) -> bool:
        """해당 코멘트 id와 다른 id만 저장"""
        comments = self._load_all()
        filtered_data = [c for c in comments if c["comment_id"] != comment_id]

        if len(comments) == len(filtered_data):
            return False

        self._save_all(filtered_data)
        return True
