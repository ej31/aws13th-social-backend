"""
Base Repository
- 모든 Repository의 기본 클래스
"""
from typing import Any
from app.core.database import get_database, Database


class BaseRepository:
    """
    모든 Repository의 기본 클래스
    
    Attributes:
        db: Database 인스턴스
        table_name: 테이블 이름
    """
    
    def __init__(self, table_name: str):
        """
        Args:
            table_name: 대상 테이블 이름
        """
        self.db: Database = get_database()
        self.table_name = table_name
    
    def find_by_id(self, id_field: str, id_value: Any) -> dict[str, Any] | None:
        """
        ID로 항목 찾기
        
        Args:
            id_field: ID 필드명 (예: "user_id", "post_id")
            id_value: ID 값
            
        Returns:
            dict[str, Any] | None: 찾은 항목 또는 None
        """
        query = f"SELECT * FROM {self.table_name} WHERE {id_field} = %s"
        return self.db.execute_query(query, (id_value,), fetch_one=True)
    
    def find_all(self) -> list[dict[str, Any]]:
        """
        전체 항목 조회
        
        Returns:
            list[dict[str, Any]]: 전체 항목 리스트
        """
        query = f"SELECT * FROM {self.table_name}"
        result = self.db.execute_query(query, fetch_all=True)
        return result if result else []
    
    def exists(self, id_field: str, id_value: Any) -> bool:
        """
        항목 존재 여부 확인
        
        Args:
            id_field: ID 필드명
            id_value: ID 값
            
        Returns:
            bool: 존재 여부
        """
        query = f"SELECT COUNT(*) as cnt FROM {self.table_name} WHERE {id_field} = %s"
        result = self.db.execute_query(query, (id_value,), fetch_one=True)
        return result['cnt'] > 0 if result else False
    
    def delete(self, id_field: str, id_value: Any) -> bool:
        """
        항목 삭제
        
        Args:
            id_field: ID 필드명
            id_value: ID 값
            
        Returns:
            bool: 삭제 성공 여부
        """
        query = f"DELETE FROM {self.table_name} WHERE {id_field} = %s"
        affected = self.db.execute_query(query, (id_value,), commit=True)
        return affected > 0 if affected else False
    
    def count(self) -> int:
        """
        전체 항목 개수
        
        Returns:
            int: 항목 개수
        """
        query = f"SELECT COUNT(*) as cnt FROM {self.table_name}"
        result = self.db.execute_query(query, fetch_one=True)
        return result['cnt'] if result else 0