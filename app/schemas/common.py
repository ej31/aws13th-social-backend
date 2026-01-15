"""
공통 스키마 정의
"""
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """
    API 공통 응답 포맷

    Attributes:
        status: 응답 상태 (success/error)
        data: 응답 데이터
    """
    status: str = Field(default="success", description="응답 상태")
    data: T = Field(description="응답 데이터")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "data": {"message": "처리 완료"}
                }
            ]
        }
    }

class PaginationResponse(BaseModel):
    """
    페이지네이션 정보

    Attributes:
        page: 현재 페이지 번호
        limit: 페이지당 항목 수
        total: 전체 항목 수
        total_pages: 전체 페이지 수
    """
    page: int = Field(ge=1, description="현재 페이지 번호")
    limit: int = Field(ge=1, le=100, description="페이지당 항목 수")
    total: int = Field(ge=0, description="전체 항목 수")
    total_pages: int = Field(ge=0, description="전체 페이지 수")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "page": 1,
                    "limit": 20,
                    "total": 150,
                    "total_pages": 8
                }
            ]
        }
    }

class PaginationParams(BaseModel):
    """
    페이지네이션 쿼리 파라미터

    Attributes:
        page: 페이지 번호 (기본값: 1)
        limit: 페이지당 항목 수 (기본값: 20, 최대: 100)
    """
    page: int = Field(default=1, ge=1, description="페이지 번호")
    limit: int = Field(default=20, ge=1, le=100, description="페이지당 항목 수")