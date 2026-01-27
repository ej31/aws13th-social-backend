"""
데이터베이스 연결 관리
"""
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from typing import Generator, Any
from dbutils.pooled_db import PooledDB

from app.core.config import get_settings

settings = get_settings()


class Database:
    """
    데이터베이스 Connection Pool 관리 클래스
    
    Attributes:
        pool: DBUtils PooledDB 인스턴스
    """
    
    def __init__(self):
        """Connection Pool 초기화"""
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW,
            mincached=settings.DB_POOL_SIZE,
            maxcached=settings.DB_POOL_SIZE,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=1 if settings.DB_POOL_PRE_PING else 0,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            charset=settings.DB_CHARSET,
            cursorclass=DictCursor,  # 결과를 dict로 반환
            autocommit=False  # 명시적 commit 사용
        )
    
    def get_connection(self):
        """
        Connection Pool에서 연결 가져오기
        
        Returns:
            pymysql.Connection: 데이터베이스 연결
        """
        return self.pool.connection()
    
    @contextmanager
    def get_cursor(self, commit: bool = False) -> Generator[Any, None, None]:

        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def execute_query(
        self, 
        query: str, 
        params: tuple | dict | None = None,
        fetch_one: bool = False,
        fetch_all: bool = False,
        commit: bool = False
    ) -> dict | list[dict] | int | None:

        with self.get_cursor(commit=commit) as cursor:
            cursor.execute(query, params)
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            elif commit:
                return cursor.rowcount
            
            return None
    
    def execute_many(
        self,
        query: str,
        params_list: list[tuple | dict],
        commit: bool = True
    ) -> int:

        with self.get_cursor(commit=commit) as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def close(self):
        """Connection Pool 종료"""
        if hasattr(self, 'pool'):
            self.pool.close()


# 싱글톤 인스턴스
_database: Database | None = None


def get_database() -> Database:

    global _database
    if _database is None:
        _database = Database()
    return _database


def close_database():
    """데이터베이스 연결 종료 (애플리케이션 종료 시)"""
    global _database
    if _database is not None:
        _database.close()
        _database = None