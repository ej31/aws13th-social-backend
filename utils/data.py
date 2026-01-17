import json
import logging
from pathlib import Path
from typing import Any, List, Dict, Optional

# 로깅 설정 (디버깅 및 에러 추적 용도)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 프로젝트 루트 기준 data 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> List[Dict[str, Any]]:
    """
    JSON 파일을 읽어 리스트 형태로 반환.
    파일이 없거나 손상된 경우 빈 리스트 반환.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 파싱 에러 ({filename}): {e}")
        return []
    except Exception as e:
        logger.error(f"파일 로드 중 알 수 없는 에러: {e}")
        return []


def save_json(filename: str, data: List[Dict[str, Any]]) -> None:
    """
    리스트 데이터를 JSON 파일로 저장.
    디렉토리가 없으면 자동으로 생성함.
    """
    file_path = DATA_DIR / filename

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"파일 저장 중 에러 발생: {e}")


def generate_id(prefix: str, current_data: List[Dict[str, Any]]) -> str:
    """
    고유 ID 생성기 (Max ID + 1 방식).
    기존 데이터가 삭제되어도 중복되지 않는 안전한 ID 생성.
    ex) user_1, user_5 -> user_6
    """
    if not current_data:
        return f"{prefix}_1"

    try:
        # 기존 ID들에서 숫자 부분만 추출하여 최대값 탐색
        existing_ids = []
        for item in current_data:
            id_val = item.get("id", "")
            if "_" in id_val:
                num_part = id_val.split("_")[-1]
                if num_part.isdigit():
                    existing_ids.append(int(num_part))

        max_id = max(existing_ids) if existing_ids else 0
        return f"{prefix}_{max_id + 1}"
    except Exception:
        # 예외 발생 시 안전을 위해 리스트 길이를 활용하거나 임의 생성
        return f"{prefix}_{len(current_data) + 1}"