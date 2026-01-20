from fastapi import APIRouter, HTTPException, status
from schemas.user import UserCreate, UserRegistrationResponse, UserInfo
from service.user import create_user, DuplicateResourceError, UserCreateFailedError

router = APIRouter(
    prefix="/users", tags=["Users"]
)

@router.post("", response_model=UserRegistrationResponse, status_code=201)
def register_user(user: UserCreate):
    try:
        new_user = create_user(user)

        return {
            "status": "success",
            "data": {
                "id": new_user["id"],
                "email": new_user["email"],
                "nickname": new_user["nickname"],
                "profile_image_url": new_user["profile_image_url"],
                "created_at": new_user["created_at"],
            }
        }

    except DuplicateResourceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "error",
                "error": {
                    "code": "DUPLICATE_RESOURCE",
                    "message": "이미 사용 중인 이메일입니다.",
                    "details": {
                        "field": e.field
                    }
                }
            }
        )

    except UserCreateFailedError:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "회원가입 처리 중 오류가 발생했습니다."
                }
            }
        )
