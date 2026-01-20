from fastapi import HTTPException

from core.db_connection import get_db_connection
from repositories.user_repo import get_users, save_users, get_all_users_db, get_user_by_id
from services.auth_service import get_password_hash


def get_my_profile(current_user: dict) -> dict:
    return current_user

def get_user_profile(user_id: str) -> dict:
    users = get_user_by_id(user_id)
    if not users:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다")
    return users

def update_my_profile(current_user: dict, patch_data: dict) -> dict:
    if not patch_data:
        raise HTTPException(status_code=400, detail="수정할 데이터가 없습니다.")

    if "password" in patch_data:
        patch_data["password"] = get_password_hash(patch_data["password"])

    con = None
    try:
        con = get_db_connection()
        with con.cursor() as cursor:
            filed = [f"{key} = %s" for key in patch_data.keys()]
            update_sql = f"UPDATE users SET {','.join(filed)} WHERE user_id = %s"

            param = list(patch_data.values())+[current_user["user_id"]]
            cursor.execute(update_sql, tuple(param))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="해당 유저가 없습니다")
        con.commit()

        with con.cursor() as cursor:
            cursor.execute("SELECT email,nickname,profile_image_url FROM users WHERE user_id = %s", (current_user["user_id"],))
            update_user = cursor.fetchone()

        return update_user

    except Exception:
        con.rollback()
        raise
    finally:
        if con:
            con.close()

def delete_my_account(current_user: dict) -> None:
    users = get_all_users_db()
    list_users = list(users)
    user = next((u for u in list_users if u["user_id"] == current_user["user_id"]), None)
    if user is None:
        raise HTTPException(status_code=404, detail="해당 유저가 없습니다")
    con = None
    try:
        con = get_db_connection()
        with con.cursor() as cursor:
            delete_sql = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(delete_sql, (current_user["user_id"],))
        con.commit()
    except Exception:
        con.rollback()
        raise

