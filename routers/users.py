from fastapi import APIRouter, HTTPException, Depends
from schemas.users import UserCreate, UserResponse, UserUpdate, UserDelete, UserPublicResponse
from utils.data import load_json, add_item, find_by_field, find_by_id, update_item, delete_item
from utils.auth import hash_password, verify_password, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", status_code=201)
async def create_user(request: UserCreate):
    """회원가입"""
    users = load_json("users.json")

    # 이메일 중복 체크
    if find_by_field(users, "email", request.email):
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "code": "DUPLICATE_RESOURCE",
                "message": "이미 사용 중인 정보(이메일/닉네임)입니다."
            }
        )

    # 닉네임 중복 체크
    if find_by_field(users, "nickname", request.nickname):
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "code": "DUPLICATE_RESOURCE",
                "message": "이미 사용 중인 정보(이메일/닉네임)입니다."
            }
        )

    # 비밀번호 해싱
    hashed_password = hash_password(request.password)

    # 사용자 저장
    new_user = add_item("users.json", {
        "email": request.email,
        "password": hashed_password,
        "nickname": request.nickname,
        "profileImage": request.profileImage
    }, id_field="userId")

    return {
        "status": "success",
        "message": "회원가입이 완료되었습니다.",
        "data": {
            "userId": new_user["userId"],
            "email": new_user["email"],
            "nickname": new_user["nickname"],
            "createdAt": new_user["createdAt"]
        }
    }


@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """내 프로필 조회"""
    users = load_json("users.json")
    user = find_by_id(users, current_user["userId"], id_field="userId")

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return {
        "status": "success",
        "data": {
            "userId": user["userId"],
            "email": user["email"],
            "nickname": user["nickname"],
            "profileImage": user.get("profileImage"),
            "createdAt": user["createdAt"]
        }
    }


@router.patch("/me")
async def update_user(user: UserUpdate, current_user: dict = Depends(get_current_user)):
    """프로필 수정"""
    users = load_json("users.json")
    current_user_data = find_by_id(users, current_user["userId"], id_field="userId")

    if not current_user_data:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 닉네임 변경 시 중복 체크
    if user.nickname and user.nickname != current_user_data["nickname"]:
        if find_by_field(users, "nickname", user.nickname):
            raise HTTPException(
                status_code=409,
                detail={
                    "status": "error",
                    "code": "DUPLICATE_RESOURCE",
                    "message": "이미 사용 중인 닉네임입니다."
                }
            )

    # 비밀번호 변경 시 currentPassword 확인
    update_data = {}
    if user.password:
        if not user.currentPassword:
            raise HTTPException(status_code=400, detail="현재 비밀번호를 입력해주세요.")

        if not verify_password(user.currentPassword, current_user_data["password"]):
            raise HTTPException(status_code=403, detail="현재 비밀번호가 일치하지 않습니다.")

        update_data["password"] = hash_password(user.password)

    if user.nickname:
        update_data["nickname"] = user.nickname
    if user.profileImage is not None:
        update_data["profileImage"] = user.profileImage

    # 업데이트
    updated_user = update_item("users.json", current_user["userId"], update_data, id_field="userId")

    return {
        "status": "success",
        "message": "프로필 정보가 성공적으로 수정되었습니다.",
        "data": {
            "userId": updated_user["userId"],
            "nickname": updated_user["nickname"],
            "profileImage": updated_user.get("profileImage"),
            "updatedAt": updated_user.get("updatedAt")
        }
    }


@router.delete("/me")
async def delete_user(user: UserDelete, current_user: dict = Depends(get_current_user)):
    """회원탈퇴"""
    users = load_json("users.json")
    current_user_data = find_by_id(users, current_user["userId"], id_field="userId")

    if not current_user_data:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 비밀번호 확인
    if not verify_password(user.password, current_user_data["password"]):
        raise HTTPException(
            status_code=403,
            detail={
                "status": "error",
                "code": "FORBIDDEN",
                "message": "비밀번호가 일치하지 않습니다."
            }
        )

    # 사용자 삭제
    delete_item("users.json", current_user["userId"], id_field="userId")

    return {
        "status": "success",
        "message": "회원 탈퇴가 성공적으로 처리되었습니다."
    }


@router.get("/{userId}")
async def get_user(userId: int):
    """특정 회원 조회"""
    users = load_json("users.json")
    user = find_by_id(users, userId, id_field="userId")

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "code": "NOT_FOUND",
                "message": "요청하신 리소스를 찾을 수 없습니다."
            }
        )

    return {
        "status": "success",
        "data": {
            "userId": user["userId"],
            "nickname": user["nickname"],
            "profileImage": user.get("profileImage"),
            "createdAt": user["createdAt"]
        }
    }
