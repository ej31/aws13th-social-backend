"""
입력 검증 유틸리티
"""
import re
from pydantic import ValidationError


def validate_email_format(email: str) -> str:
    """
    이메일 형식 검증
    
    Args:
        email: 검증할 이메일
    
    Returns:
        str: 검증된 이메일
        
    Raises:
        ValueError: 이메일 형식이 올바르지 않은 경우
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    return email


def validate_password_strength(password: str) -> str:
    """
    비밀번호 강도 검증
    - 최소 8자 이상
    - 영문과 숫자 조합
    
    Args:
        password: 검증할 비밀번호
    
    Returns:
        str: 검증된 비밀번호
        
    Raises:
        ValueError: 비밀번호가 요구사항을 충족하지 못한 경우
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    # 영문과 숫자 포함 확인
    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    
    if not (has_letter and has_digit):
        raise ValueError("Password must contain both letters and numbers")
    
    return password


def validate_nickname_length(nickname: str) -> str:
    """
    닉네임 길이 검증
    - 2자 이상 20자 이하
    
    Args:
        nickname: 검증할 닉네임
    
    Returns:
        str: 검증된 닉네임
        
    Raises:
        ValueError: 닉네임이 요구사항을 충족하지 못한 경우
    """
    if len(nickname) < 2:
        raise ValueError("Nickname must be at least 2 characters long")
    
    if len(nickname) > 20:
        raise ValueError("Nickname must be at most 20 characters long")
    
    return nickname


def validate_post_title(title: str) -> str:
    """
    게시글 제목 검증
    - 1자 이상 200자 이하
    
    Args:
        title: 검증할 제목
    
    Returns:
        str: 검증된 제목
        
    Raises:
        ValueError: 제목이 요구사항을 충족하지 못한 경우
    """
    if len(title) < 1:
        raise ValueError("Title cannot be empty")
    
    if len(title) > 200:
        raise ValueError("Title must be at most 200 characters long")
    
    return title


def validate_post_content(content: str) -> str:
    """
    게시글 내용 검증
    - 1자 이상 10000자 이하
    
    Args:
        content: 검증할 내용
    
    Returns:
        str: 검증된 내용
        
    Raises:
        ValueError: 내용이 요구사항을 충족하지 못한 경우
    """
    if len(content) < 1:
        raise ValueError("Content cannot be empty")
    
    if len(content) > 10000:
        raise ValueError("Content must be at most 10000 characters long")
    
    return content


def validate_comment_content(content: str) -> str:
    """
    댓글 내용 검증
    - 1자 이상 500자 이하
    
    Args:
        content: 검증할 내용
    
    Returns:
        str: 검증된 내용
        
    Raises:
        ValueError: 내용이 요구사항을 충족하지 못한 경우
    """
    if len(content) < 1:
        raise ValueError("Comment cannot be empty")
    
    if len(content) > 500:
        raise ValueError("Comment must be at most 500 characters long")
    
    return content