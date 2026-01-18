import json
import os
from typing import List, Dict, Any

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_file_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)

def load_data(filename: str) -> List[Dict[str, Any]]:
    path = get_file_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(filename: str, data: List[Dict[str, Any]]):
    path = get_file_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)