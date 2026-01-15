from typing import Annotated

from repositories.user_repository import UserRepository


class PostService:
    def __init__(self,user_repository: UserRepository):
        self.user_repo = user_repository
