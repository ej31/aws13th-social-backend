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
            except (FileNotFoundError, json.JSONDecodeError):
                return []

    # 내부용 함수
    def _save_all(self, users: list[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def find_all(self) -> list:
        return self._load_all()

    def find_by_id(self, post_id: int) -> dict | None:
        posts = self._load_all()
        for p in posts:
            if (p["post_id"]) == post_id:
                return p
        return None

    def save(self, post_data: dict) -> dict:
        posts = self._load_all()
        #새 게시글인지 확인한다.
        if "post_id" not in post_data or post_data["post_id"] is None:
            # 현재 게시글의 id 중 최대값을 찾는다. (기본값이 없을 시 default=0으로 해둠)
            max_id = max([p["post_id"] for p in posts],default=0)
            #새 ID 부여 (최대값 + 1)
            post_data["post_id"] = max_id + 1
            #리스트에 새 데이터 추가
            posts.append(post_data)
        else:
            #p에는 posts, post_data의 id와 비교해서 같은 값을 찾음
            for i,p in enumerate(posts):
                if p["post_id"] == post_data["post_id"]:
                    #찾게되면 현재 저장되어 있는 posts[i]번째를 현재 저장할려는 post_data로 변경함
                    posts[i] = post_data
                    break
        self._save_all(posts)
        return post_data

    def delete(self, post_id: int) -> bool:
        posts = self._load_all()
        filtered_posts = [p for p in posts if p["post_id"] != post_id]

        if len(posts) == len(filtered_posts):
            #결과적으로 지워진게 없을 시
            return False

        self._save_all(filtered_posts)
        return True
