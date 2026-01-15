from datetime import datetime
from typing import Annotated

from fastapi import HTTPException,status
from fastapi.params import Depends

from repositories.post_repository import PostRepository
from schemas.post import PostsCreateRequest, PostsUpdateRequest


class PostService:
    def __init__(self,post_repo:Annotated[PostRepository, Depends(PostRepository)]) -> None:
        self.post_repo = post_repo

    @staticmethod
    def _verify_author(post:dict, current_user_id: str):
        if post["author_id"] != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="해당 게시글에 대한 수정/삭제 권한이 없습니다.")

    async def create_post(self,req:PostsCreateRequest, author_id : str) -> dict:
        post_data = req.model_dump()

        post_data["author_id"] = author_id
        post_data["created_at"] = datetime.now()
        post_data["views"] = 0

        return self.post_repo.save(post_data)

    async def get_posts(self,page:int =1,limit:int = 10):
        all_posts = self.post_repo.find_all()

        all_posts.sort(key=lambda x: x["created_at"], reverse=True)

        start = (page - 1) * limit
        end = start+limit
        return all_posts[start:end], len(all_posts)

    async def update_posts(self,post_id:int,req:PostsUpdateRequest, author_id : str):
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")
        self._verify_author(post,author_id)

        #exclude_unset -> 요청하지 않은 필드는 가져오지 마라
        update_data = req.model.dump(exclude_unset=True)
        post.update(update_data)

        return self.post_repo.save(post)

    async def delete_posts(self,post_id:int,author_id:str) -> bool:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")
        self._verify_author(post,author_id)

        return self.post_repo.delete(post_id)
