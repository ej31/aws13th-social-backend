from typing import Annotated, List, Tuple
from fastapi import HTTPException, status, Depends

from common.security import encode_id
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from repositories.like_repository import LikeRepository
from models.base import Post as PostTable
from schemas.post import PostsCreateRequest, PostsUpdateRequest


class PostService:
    def __init__(self,
                 post_repo: Annotated[PostRepository, Depends(PostRepository)],
                 user_repo: Annotated[UserRepository, Depends(UserRepository)],
                 like_repo: Annotated[LikeRepository, Depends(LikeRepository)]) -> None:
        self.user_repo = user_repo
        self.post_repo = post_repo
        self.like_repo = like_repo

    @staticmethod
    def _post_verify_author(post: PostTable, current_user_id: int) -> None:
        """현재 사용자와 글쓴이가 맞는지 확인 (객체 속성 접근)"""
        if post.author_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="해당 게시글에 대한 수정/삭제 권한이 없습니다.")

    async def _assemble_post_response(self, post: PostTable, current_user_id: int | None = None) -> dict:
        """게시글 객체에 관계 데이터를 합쳐 응답 규격으로 변환"""
        # 1. 작성자 정보 가져오기 (관계 설정을 했다면 post.author로 바로 접근 가능하지만, 명시적 로직 유지)
        author_info = await self.user_repo.find_by_id(post.author_id)

        author_data = {
            "id": encode_id(author_info.id) if author_info else "unknown",
            "nickname": author_info.nickname if author_info else "탈퇴한 사용자"
        }

        # 2. 실시간 좋아요 여부 확인
        is_liked = False
        if current_user_id:
            like_exists = await self.like_repo.find_by_post_and_user(post.id, current_user_id)
            is_liked = True if like_exists else False

        # 3. 데이터 조립
        return {
            "post_id": post.id,
            "title": post.title,
            "content": post.content,
            "author": author_data,
            "like_count": post.like_count,
            "views": post.views,
            "is_liked": is_liked,
            "created_at": post.created_at
        }

    async def create_post(self, req: PostsCreateRequest, author_id: int) -> dict:
        # PostsCreateInternal 없이 바로 모델 객체 생성
        new_post = PostTable(
            author_id=author_id,
            title=req.title,
            content=req.content
        )
        saved_post = await self.post_repo.add(new_post)
        return await self._assemble_post_response(saved_post, author_id)

    async def get_post(self, page: int = 1, limit: int = 10, current_user_id: int | None = None) -> Tuple[
        List[dict], int]:
        all_posts = await self.post_repo.find_all()

        start = (page - 1) * limit
        end = start + limit
        paged_posts = all_posts[start:end]

        paged_post_data = [
            await self._assemble_post_response(post, current_user_id)
            for post in paged_posts
        ]
        return paged_post_data, len(all_posts)

    async def get_post_detail(self, post_id: int, current_user_id: int | None = None) -> dict:
        await self.post_repo.increment_views(post_id)

        post = await self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글이 존재하지 않습니다.")

        return await self._assemble_post_response(post, current_user_id)

    async def update_post(self, post_id: int, req: PostsUpdateRequest, author_id: int):
        post = await self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글이 존재하지 않습니다.")

        self._post_verify_author(post, author_id)

        update_data = req.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)

        updated_post = await self.post_repo.update(post)
        return await self._assemble_post_response(updated_post, author_id)

    async def delete_post(self, post_id: int, author_id: int) -> bool:
        post = await self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글이 존재하지 않습니다.")

        self._post_verify_author(post, author_id)

        return await self.post_repo.delete(post_id)