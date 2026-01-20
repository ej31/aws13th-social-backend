import json
from pathlib import Path
from datetime import datetime, timezone
import aiofiles

DATA_DIR = Path(__file__).parent.parent / "data"

async def load_json(filename):
    """JSON 파일을 비동기로 로드합니다."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return []
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            content = content.strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {filename}: {e}")
        return []



async def save_json(filename, data):
    """JSON 파일 쓰기"""
    file_path = DATA_DIR / filename
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))


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

async def add_item(filename, item, id_field="id"):
    """새 항목 추가"""
    data = await load_json(filename)
    # ID 자동 생성
    if id_field not in item:
        item[id_field] = get_next_id(data, id_field)
    # 생성 시간 추가
    if "createdAt" not in item:
        item["createdAt"] = datetime.now(timezone.utc).isoformat()
    data.append(item)
    await save_json(filename, data)
    return item

async def update_item(filename, id_value, updated_data, id_field="id"):
    """항목 수정"""
    data = await load_json(filename)
    for i, item in enumerate(data):
        if item.get(id_field) == id_value:
            data[i].update(updated_data)
            data[i]["updatedAt"] = datetime.now(timezone.utc).isoformat()
            await save_json(filename, data)
            return data[i]
    return None


async def delete_item(filename, id_value, id_field="id"):
    """항목 삭제"""
    data = await load_json(filename)
    for i, item in enumerate(data):
        if item.get(id_field) == id_value:
            data.pop(i)
            await save_json(filename, data)
            return True
    return False


def filter_items(data, filters):
    """여러 조건으로 필터링"""
    result = data
    for key, value in filters.items():
        result = [item for item in result if item.get(key) == value]
    return result

async def delete_items_by_field(filename, field, value):
    """특정 필드 값으로 여러 아이템을 삭제합니다."""
    data = await load_json(filename)
    original_length = len(data)
    data = [item for item in data if item.get(field) !=
            value]

    if len(data) < original_length:
        await save_json(filename, data)
        return original_length - len(data)  # 삭제된 개수 반환
    return 0
