import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Any, List, Dict

# 로깅 설정
logger = logging.getLogger(__name__)

# 프로젝트 루트 및 데이터 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# 허용된 파일 목록 (화이트리스트 정책)
ALLOWED_FILES = {"users.json", "posts.json", "comments.json", "likes.json"}


def safe_path(filename: str) -> Path:
    """
    보안 검증 관문: 허용된 파일인지 확인하고 Path Traversal을 차단함.
    """
    # 1. 화이트리스트 검사
    if filename not in ALLOWED_FILES:
        logger.error(f"허용되지 않은 파일 접근 시도: {filename}")
        raise ValueError("허용되지 않은 파일 접근입니다.")

    # 2. 경로 정규화 및 절대 경로 계산
    file_path = (DATA_DIR / filename).resolve()

    # 3. 상위 디렉토리 탈출 여부 검사 (보안 핵심)
    if not str(file_path).startswith(str(DATA_DIR.resolve())):
        logger.critical(f"Path Traversal 공격 감지: {filename}")
        raise ValueError("보안 위협이 감지되었습니다.")

    return file_path


def load_json(filename: str) -> List[Dict[str, Any]]:
    """
    JSON 파일을 로드함. 보안 관문(safe_path)을 반드시 통과해야 함.
    """
    # 보안 검증 적용
    file_path = safe_path(filename)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # 주의: 파일 크기가 커질수록 성능이 O(n)으로 저하됨
            return json.load(f)

    except json.JSONDecodeError as e:
        logger.critical(f"데이터 손상 감지 ({filename}): {e}")
        raise RuntimeError("데이터 파일이 손상되어 읽을 수 없습니다.")
    except Exception as e:
        logger.exception(f"파일 로드 중 알 수 없는 오류 발생: {e}")
        raise RuntimeError("데이터 로딩 실패")


def save_json(filename: str, data: List[Dict[str, Any]]) -> bool:
    """
    데이터를 안전하게 저장함. 임시 파일을 활용하여 원자성을 보장함.
    """
    # 보안 검증 적용
    file_path = safe_path(filename)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 원자적 쓰기(Atomic Write) 구현: 파일 쓰기 중 오류 시 기존 파일 보호
        with tempfile.NamedTemporaryFile('w', encoding='utf-8',
                                         dir=file_path.parent,
                                         delete=False) as tmp_file:
            json.dump(data, tmp_file, ensure_ascii=False, indent=2)
            tmp_path = tmp_file.name

        # 쓰기가 성공했을 때만 파일 교체
        shutil.move(tmp_path, file_path)
        return True
    except Exception as e:
        logger.exception(f"파일 저장 중 치명적 에러 발생: {e}")
        return False


def generate_id(prefix: str, current_data: List[Dict[str, Any]]) -> str:
    """고유 ID 생성 (Max ID + 1 방식)"""
    max_id = 0
    for item in current_data:
        item_id = item.get("id")
        if not item_id or not item_id.startswith(f"{prefix}_"):
            continue
        try:
            num_part = int(item_id.split("_")[-1])
            if num_part > max_id:
                max_id = num_part
        except (ValueError, IndexError):
            continue
    return f"{prefix}_{max_id + 1}"