import json
import logging
from pathlib import Path
from typing import Any, List, Dict, Optional

# 로깅 설정 (디버깅 및 에러 추적 용도)
logger = logging.getLogger(__name__)

# 프로젝트 루트 기준 data 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ALLOWED_FILES = {"users.json", "posts.json", "comments.json", "likes.json"}

def safe_path(filename: str) -> Path:
    if filename not in ALLOWED_FILES:
        raise ValueError("허용되지 않은 파일 접근")

    file_path = (DATA_DIR / filename).resolve()

    # DATA_DIR 밖으로 나가는지 검사
    if not str(file_path).startswith(str(DATA_DIR.resolve())):
        raise ValueError("Path Traversal 감지됨")

    return file_path
def load_json(filename: str) -> List[Dict[str, Any]]:
    """
    JSON 파일을 읽어 리스트 형태로 반환.

    - 파일이 존재하지 않으면 빈 리스트 반환 (정상 초기 상태)
    - JSON 파싱 에러 발생 시 RuntimeError 발생 (데이터 손상)
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError as e:
        logger.critical(f"JSON 파일 손상 감지 ({filename}): {e}")
        raise RuntimeError("데이터 파일이 손상되었습니다")

    except Exception as e:
        logger.exception("파일 로드 중 알 수 없는 오류")
        raise RuntimeError("데이터 파일을 읽는 중 오류 발생")


def save_json(filename: str, data: list[dict[str, Any]]) -> bool:
    """
    리스트 데이터를 JSON 파일로 저장.
    디렉토리가 없으면 자동으로 생성함.
    성공 시 True, 실패 시 False 반환.
    """
    file_path = DATA_DIR / filename

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.exception("파일 저장 중 에러 발생")
        return False


def generate_id(prefix: str, current_data: List[Dict[str, Any]]) -> str:
    """
    고유 ID 생성기 (Max ID + 1 방식).
    기존 데이터가 삭제되어도 중복되지 않는 안전한 ID 생성.
    ex) user_1, user_5 -> user_6
    """
    max_id = 0

    for item in current_data:
        item_id = item.get("id")

        # prefix가 다르면 무시
        if not item_id or not item_id.startswith(f"{prefix}_"):
            continue

        try:
            num_part = int(item_id.split("_")[-1])
            if num_part > max_id:
                max_id = num_part
        except (ValueError, IndexError):
            logger.warning(f"잘못된 형식의 ID를 발견했습니다: {item_id}")
            continue

    return f"{prefix}_{max_id + 1}"
