from typing import Annotated

from fastapi import HTTPException, status
from fastapi.params import Depends

from common.security import encode_id
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from repositories.like_repository import LikeRepository
from schemas.post import PostsCreateRequest, PostsUpdateRequest, PostsInternal


class PostService:
    def __init__(self,
                 post_repo: Annotated[PostRepository, Depends(PostRepository)],
                 user_repo: Annotated[UserRepository, Depends(UserRepository)],
                 like_repo: Annotated[LikeRepository, Depends(LikeRepository)]) -> None:
        self.user_repo = user_repo
        self.post_repo = post_repo
        self.like_repo = like_repo

    @staticmethod
    def _verify_author(post: dict, current_user_id: int) -> None:
        """현재 사용자와 글쓴이가 맞는지 확인"""
        if post["author_id"] != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="해당 댓글에 대한 수정/삭제 권한이 없습니다.")

    def _assemble_post_response(self, post_data: dict, current_user_id: int | None = None) -> dict | None:
        """게시글 데이터에 author 및 실시간 좋아요 정보를 합쳐 응답 규격을 맞춤"""
        if not post_data:
            return None

        author_id = post_data.get("author_id")
        author_info = self.user_repo.find_by_id(author_id)

        if author_info:
            post_data["author"] = {
                "id": encode_id(author_info.get("id")),
                "nickname": author_info.get("nickname"),
            }
        else:
            post_data["author"] = {"id": "unknown", "nickname": "탈퇴한 사용자"}

        # 실시간 좋아요 여부 확인
        is_liked = False
        if current_user_id:
            # LikeRepository를 통해 현재 유저가 이 게시글에 좋아요를 눌렀는지 확인
            like_exists = self.like_repo.find_by_post_and_user(post_data["post_id"], current_user_id)
            is_liked = True if like_exists else False

        post_data["is_liked"] = is_liked
        return post_data

    async def create_post(self, req: PostsCreateRequest, author_id: int) -> dict:
        post_data = PostsInternal(
            post_id = self.post_repo.get_next_id(),
            author_id = author_id,
            **req.model_dump()
        )
        saved_post = self.post_repo.save(post_data.model_dump())

        # 생성 직후에는 본인이 좋아요를 누른 상태가 아니므로 author_id를 넘기지 않거나 로직에 따라 처리
        return self._assemble_post_response(saved_post, author_id)

    async def get_posts(self, page: int = 1, limit: int = 10, current_user_id: str | None = None):
        all_posts = self.post_repo.find_all()
        all_posts.sort(key=lambda x: x["created_at"], reverse=True)

        start = (page - 1) * limit
        end = start + limit
        paged_post = all_posts[start:end]

        # 각 게시글마다 현재 사용자의 좋아요 여부를 판별하여 조립
        paged_post_data = [self._assemble_post_response(post, current_user_id) for post in paged_post]
        return paged_post_data, len(all_posts)

    async def get_posts_detail(self, post_id: int, current_user_id: str | None = None) -> dict:
        self.post_repo.increment_views(post_id)
        posts_data = self.post_repo.find_by_id(post_id)
        if not posts_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")

        # 상세 조회 시에도 현재 유저 ID를 넘겨야 is_liked가 계산됨
        return self._assemble_post_response(posts_data, current_user_id)

    async def update_posts(self, post_id: int, req: PostsUpdateRequest, author_id: int):
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")

        self._verify_author(post, author_id)

        update_data = req.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            post[key] = value

        updated_post = self.post_repo.save(post)
        return self._assemble_post_response(updated_post, author_id)

    async def delete_posts(self, post_id: int, author_id: int) -> bool:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")
        self._verify_author(post, author_id)

        return self.post_repo.delete(post_id)