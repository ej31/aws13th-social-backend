"""
Base Repository
- JSON 파일 기반 공통 CRUD 로직
- 모든 Repository의 기본 클래스
"""
from typing import Any, Callable
from app.utils.json_handler import JsonFileHandler


class BaseRepository:
    """
    모든 Repository의 기본 클래스
    
    Attributes:
        handler: JSON 파일 핸들러
    """
    
    def __init__(self, file_path: str):
        """
        Args:
            file_path: JSON 파일 경로
        """
        self.handler = JsonFileHandler(file_path)
    
    def find_by_id(self, id_field: str, id_value: Any) -> dict[str, Any] | None:
        """
        ID로 항목 찾기
        
        Args:
            id_field: ID 필드명 (예: "user_id", "post_id")
            id_value: ID 값
            
        Returns:
            dict[str, Any] | None: 찾은 항목 또는 None
        """
        return self.handler.find_one(lambda x: x.get(id_field) == id_value)
    
    def find_all(self) -> list[dict[str, Any]]:
        """
        전체 항목 조회
        
        Returns:
            list[dict[str, Any]]: 전체 항목 리스트
        """
        return self.handler.read()
    
    def find_many(
        self, 
        condition: Callable[[dict[str, Any]], bool] | None = None
    ) -> list[dict[str, Any]]:
        """
        조건에 맞는 항목들 찾기
        
        Args:
            condition: 필터 조건 함수, None이면 전체 반환
            
        Returns:
            list[dict[str, Any]]: 조건에 맞는 항목 리스트
        """
        return self.handler.find_many(condition)
    
    def create(self, item: dict[str, Any]) -> dict[str, Any]:
        """
        항목 생성
        
        Args:
            item: 생성할 항목 데이터
            
        Returns:
            dict[str, Any]: 생성된 항목
        """
        self.handler.append(item)
        return item
    
    def update(
        self, 
        id_field: str, 
        id_value: Any, 
        updates: dict[str, Any]
    ) -> bool:
        """
        항목 수정
        
        Args:
            id_field: ID 필드명
            id_value: ID 값
            updates: 수정할 필드들
            
        Returns:
            bool: 수정 성공 여부
        """
        return self.handler.update(
            lambda x: x.get(id_field) == id_value,
            updates
        )
    
    def delete(self, id_field: str, id_value: Any) -> bool:
        """
        항목 삭제
        
        Args:
            id_field: ID 필드명
            id_value: ID 값
            
        Returns:
            bool: 삭제 성공 여부
        """
        return self.handler.delete(lambda x: x.get(id_field) == id_value)
    
    def exists(self, id_field: str, id_value: Any) -> bool:
        """
        항목 존재 여부 확인
        
        Args:
            id_field: ID 필드명
            id_value: ID 값
            
        Returns:
            bool: 존재 여부
        """
        return self.find_by_id(id_field, id_value) is not None