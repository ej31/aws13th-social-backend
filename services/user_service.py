from fastapi import HTTPException
from repositories.user_repo import get_users, save_users,find_user_by_id


def get_my_profile(current_user: dict) -> dict:
    return current_user

def get_user_profile(user_id: str) -> dict:
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다")
    return user

def update_my_profile(current_user: dict, patch_data: dict) -> dict:
    users = get_users()

    index = next(
        (i for i, u in enumerate(users) if u["user_id"] == current_user["user_id"]),
        None,
    )

    if index is None:
        raise HTTPException(status_code=404, detail="해당 유저가 없습니다")

    users[index].update(patch_data)
    save_users(users)
    return users[index]

def delete_my_account(current_user: dict) -> None:
    users = get_users()
    new_users = [u for u in users if u["user_id"] != current_user["user_id"]]

    if len(users) == len(new_users):
        raise HTTPException(status_code=404, detail="삭제할 유저를 찾을 수 없습니다")

    save_users(new_users)