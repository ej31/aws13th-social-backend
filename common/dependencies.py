from typing import Annotated

from fastapi import Depends

from repositories.user_repository import UserRepository
from services.user_service import UserService


def get_user_repo() -> UserRepository:
    return UserRepository()

def get_auth_service(
        repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> UserService:
    return UserService(user_repo = repo)