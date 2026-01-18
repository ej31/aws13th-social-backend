import json
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename):
    """JSON 파일 읽기"""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {file_path}") from e
    except OSError:
        return []


def save_json(filename, data):
    """JSON 파일 쓰기"""
    file_path = DATA_DIR / filename

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_next_id(data, id_field="id"):
    """다음 사용할 ID 생성"""
    if not data:
        return 1

    max_id = max((item.get(id_field, 0) for item in data), default=0)
    return max_id + 1


def find_by_id(data, id_value, id_field="id"):
    """ID로 데이터 찾기"""
    for item in data:
        if item.get(id_field) == id_value:
            return item
    return None


def find_by_field(data, field, value):
    """특정 필드 값으로 데이터 찾기"""
    for item in data:
        if item.get(field) == value:
            return item
    return None


def add_item(filename, item, id_field="id"):
    """새 항목 추가"""
    data = load_json(filename)

    # ID 자동 생성
    if id_field not in item:
        item[id_field] = get_next_id(data, id_field)

    # 생성 시간 추가
    if "createdAt" not in item:
        item["createdAt"] = datetime.now(timezone.utc).isoformat()

    data.append(item)
    save_json(filename, data)

    return item


def update_item(filename, id_value, updated_data, id_field="id"):
    """항목 수정"""
    data = load_json(filename)

    for i, item in enumerate(data):
        if item.get(id_field) == id_value:
            data[i].update(updated_data)
            data[i]["updatedAt"] = datetime.now(timezone.utc).isoformat()
            save_json(filename, data)
            return data[i]

    return None


def delete_item(filename, id_value, id_field="id"):
    """항목 삭제"""
    data = load_json(filename)

    for i, item in enumerate(data):
        if item.get(id_field) == id_value:
            data.pop(i)
            save_json(filename, data)
            return True

    return False


def filter_items(data, filters):
    """여러 조건으로 필터링"""
    result = data
    for key, value in filters.items():
        result = [item for item in result if item.get(key) == value]
    return result
