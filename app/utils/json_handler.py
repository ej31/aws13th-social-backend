"""
JSON 파일 읽기/쓰기 유틸리티
- filelock을 이용한 크로스 플랫폼 동시성 제어
"""
import json
import os
from typing import Any
from collections.abc import Callable
from filelock import FileLock, Timeout


class JsonFileHandler:
    """JSON 파일 핸들러"""
    
    def __init__(self, file_path: str) -> None:
        """
        Args(매개변수):
            file_path: JSON 파일 경로
        """
        self.file_path = file_path
        self.lock_path = f"{file_path}.lock"
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """파일이 존재하지 않으면 안전하게 생성"""
        dir_path = os.path.dirname(self.file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
            
        lock = FileLock(self.lock_path, timeout=10)
        try:
            with lock:
                if not os.path.exists(self.file_path):
                    with open(self.file_path, 'w', encoding='utf-8') as f:
                        json.dump([], f)
        except Timeout:
            print(f"로그: {self.lock_path}에 대한 락을 획득하지 못했습니다.")
            raise
    
    def read(self) -> list[dict[str, Any]]:
        """
        JSON 파일에서 데이터 읽기
        
        Returns(반환값):
            list[dict[str, Any]]: 데이터 리스트
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def write(self, data: list[dict[str, Any]]) -> None:
        """
        JSON 파일에 데이터 쓰기
        
        Args:
            data: 저장할 데이터 리스트
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def append(self, item: dict[str, Any]) -> None:
        """
        JSON 파일에 항목 추가
        
        Args:
            item: 추가할 항목
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data.append(item)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update(self, condition: Callable[[dict[str, Any]], bool], updates: dict[str, Any]) -> bool:
        """
        조건에 맞는 항목 업데이트
        
        Args:
            condition: 업데이트할 항목을 찾는 함수 (item -> bool)
            updates: 업데이트할 필드들
        
        Returns:
            bool: 업데이트 성공 여부
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            for i, item in enumerate(data):
                if condition(item):
                    data[i].update(updates)
                    updated = True
                    break
            
            if updated:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            return updated
    
    def delete(self, condition: Callable[[dict[str, Any]], bool]) -> bool:
        """
        조건에 맞는 항목 삭제
        
        Args:
            condition: 삭제할 항목을 찾는 함수 (item -> bool)
        
        Returns:
            bool: 삭제 성공 여부
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            original_length = len(data)
            data = [item for item in data if not condition(item)]
            
            if len(data) < original_length:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            
            return False
    
    def find_one(self, condition: Callable[[dict[str, Any]], bool]) -> dict[str, Any] | None:
        """
        조건에 맞는 첫 번째 항목 찾기
        
        Args:
            condition: 찾을 항목의 조건 함수 (item -> bool)
        
        Returns:
            dict[str, Any] | None: 찾은 항목 또는 None
        """
        data = self.read()
        return next((item for item in data if condition(item)), None)
    
    def find_many(self, condition: Callable[[dict[str, Any]], bool] | None = None) -> list[dict[str, Any]]:
        """
        조건에 맞는 모든 항목 찾기
        
        Args:
            condition: 찾을 항목의 조건 함수 (item -> bool), None이면 전체 반환
        
        Returns:
            list[dict[str, Any]]: 찾은 항목들
        """
        data = self.read()
        
        if condition is None:
            return data
        
        return [item for item in data if condition(item)]
    
    # 원자적 연산 메서드 - 동시성 문제 해결
    
    def atomic_increment(
        self,
        condition: Callable[[dict[str, Any]], bool],
        field: str,
        delta: int = 1
    ) -> bool:
        """
        원자적 증감 연산 (읽기-수정-쓰기를 한 번의 LOCK으로 처리)
        
        Args:
            condition: 대상 항목을 찾는 함수 (item -> bool)
            field: 증감할 필드명 (예: "views", "likes")
            delta: 증감량 (양수: 증가, 음수: 감소)
        
        Returns:
            bool: 업데이트 성공 여부
            
        Example:
            >>> handler.atomic_increment(
            ...     lambda x: x["post_id"] == 123,
            ...     "views",
            ...     1
            ... )
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            # 읽기-수정-쓰기를 한 번의 LOCK 안에서 처리
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            for i, item in enumerate(data):
                if condition(item):
                    current_value = item.get(field, 0)
                    data[i][field] = max(0, current_value + delta)  # 음수 방지
                    updated = True
                    break
            
            if updated:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            return updated
    
    def atomic_update_with_callback(
        self,
        condition: Callable[[dict[str, Any]], bool],
        update_fn: Callable[[dict[str, Any]], dict[str, Any]]
    ) -> bool:
        """
        콜백 함수를 사용한 원자적 업데이트
        
        Args:
            condition: 대상 항목을 찾는 함수 (item -> bool)
            update_fn: 업데이트 로직을 담은 함수 (item -> updates)
        
        Returns:
            bool: 업데이트 성공 여부
            
        Example:
            >>> handler.atomic_update_with_callback(
            ...     lambda x: x["post_id"] == 123,
            ...     lambda post: {
            ...         "views": post.get("views", 0) + 1,
            ...         "updated_at": datetime.now().isoformat()
            ...     }
            ... )
        """
        lock = FileLock(self.lock_path, timeout=10)
        with lock:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            for i, item in enumerate(data):
                if condition(item):
                    updates = update_fn(item)
                    data[i].update(updates)
                    updated = True
                    break
            
            if updated:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            return updated