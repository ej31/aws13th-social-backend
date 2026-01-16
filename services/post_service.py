from datetime import datetime,timezone
from typing import Annotated

from fastapi import HTTPException,status
from fastapi.params import Depends

from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from schemas.post import PostsCreateRequest, PostsUpdateRequest


class PostService:
    def __init__(self,post_repo:Annotated[PostRepository, Depends(PostRepository)],
                      user_repo:Annotated[UserRepository,Depends()]) -> None:
        self.post_repo = post_repo

    @staticmethod
    def _verify_author(post:dict, current_user_id: str):
        if post["author_id"] != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="해당 게시글에 대한 수정/삭제 권한이 없습니다.")

    async def create_post(self,req:PostsCreateRequest, author_id : str) -> dict:
        post_data = req.model_dump()

        post_data["author_id"] = author_id
        post_data["created_at"] = datetime.now(timezone.utc).isoformat()
        post_data["views"] = 0
        post_data["likes"] = 0
        post_data["comment_count"]=0
        saved_post = self.post_repo.save(post_data)

        author_info = self.user_repo.find_by_id(author_id)
        return self.post_repo.save(post_data)

    async def get_posts(self,page:int =1,limit:int = 10):
        all_posts = self.post_repo.find_all()

        all_posts.sort(key=lambda x: x["created_at"], reverse=True)

        start = (page - 1) * limit
        #start가 0부터 시작하는 이유는 리스트의 인덱스는 0부터 시작하므로
        #즉 1페이지 보여줘 하면 0번 인덱스부터 보여줘야 하므로
        end = start + limit
        #end는 끝까지 보여줄 페이지 즉 0+10 =10 10페이지가 마지막
        return all_posts[start:end], len(all_posts)

    async def get_posts_detail(self,post_id:int,user_id:str | None = None) -> dict:
        posts_data = self.post_repo.find_by_id(post_id)
        if not posts_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")
        posts_data["views"] += 1
        self.post_repo.save(posts_data)

        is_liked= False
        #좋아요 검증 로직 (아직 좋아요 서비스 개발중이 아니라서 주석처리
        #if user_id:
        #    is_liked= self.liked_repo.exists(post_id,user_id)

        posts_data["is_liked"] = is_liked
        return posts_data


    async def update_posts(self,post_id:int,req:PostsUpdateRequest, author_id : str):
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")
        self._verify_author(post,author_id)

        #exclude_unset -> 요청하지 않은 필드는 가져오지 마라
        update_data = req.model_dump(exclude_unset=True)
        post.update(update_data)

        return self.post_repo.save(post)

    async def delete_posts(self,post_id:int,author_id:str) -> bool:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="게시글이 존재하지 않습니다.")
        self._verify_author(post,author_id)

        return self.post_repo.delete(post_id)
