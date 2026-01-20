import json
import os

from common.config import settings


class PostRepository:
    def __init__(self) -> None:
        self.file_path = settings.posts_json_path
        if not os.path.exists(self.file_path):
            self._save_all([])

    # 내부용 함수
    def _load_all(self) -> list[dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    # 내부용 함수
    def _save_all(self, posts: list[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=4, ensure_ascii=False)

    def find_all(self) -> list[dict]:
        return self._load_all()

    def find_by_id(self, post_id: int) -> dict | None:
        posts = self._load_all()
        for p in posts:
            if p["post_id"] == post_id:
                return p
        return None

    def get_next_id(self):
        """다음에 부여할 게시물의 ID를 반환"""
        posts = self._load_all()
        return max([p["post_id"] for p in posts],default=0)+1

    def save(self, post_data: dict) -> dict:
        posts = self._load_all()
        target_id = post_data.get("post_id")

        if target_id is None:
            raise ValueError(f"게시물의 ID : {target_id}가 존재하지 않습니다.")

        index = None
        for i,p in enumerate(posts):
            if int(p["post_id"]) == target_id:
                index = i
                break

        if index is not None:
            #수정
            posts[index] = post_data
        else:
            #생성
            posts.append(post_data)

        self._save_all(posts)
        return post_data

    def delete(self, post_id: int) -> bool:
        posts = self._load_all()

        #삭제하지 않을 포스트들만 걸러낸다.
        filtered_posts = [p for p in posts if p["post_id"] != post_id]

        if len(posts) == len(filtered_posts):
            #결과적으로 지워진게 없을 시
            return False

        self._save_all(filtered_posts)
        return True

    def update_like_count(self, post_id: int, like_count: int) -> bool:
        """특정 게시글의 좋아요 숫자를 업데이트 (데이터 정합성 유지)"""
        posts = self._load_all()

        for post in posts:
            if int(post["post_id"]) == int(post_id):
                post["likes"] = like_count
                self._save_all(posts)
                return True

        return False

    def increment_views(self, post_id: int) -> bool:
        """특정 게시글의 조회수를 1 증가시킴"""
        posts = self._load_all()

        for post in posts:
            if int(post["post_id"]) == int(post_id):
                # 기존 views가 없을 경우를 대비해 get() 사용 후 +1
                post["views"] = post.get("views", 0) + 1
                self._save_all(posts)
                return True

        return False