
# JSON 저장소 접근 역할
# JSON 읽기/쓰기
# 기본 CRUD 헬퍼

import json
import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

def _ensure_file(path: Path, default: Any) -> None :
    path.parent.mkdir(parents=True, exist_ok=True) # 중간 경로 빠져도 생성하고, 해당 파일이 이미 있으면 아무것도 안함
    if not path.exists():
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")

def read_json(filename: str, default: Any) -> Any:
    path = DATA_DIR / filename
    _ensure_file(path, default)
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(filename: str, data: Any):
    path = DATA_DIR / filename
    _ensure_file(path, data)
    tmp = path.with_suffix(".tmp") # 임시 파일 경로 객체 생성
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8") # 임시 파일 생성
    os.replace(tmp, path) # 기존 파일이랑 임시파일 바꿔치기 -> 쓰다 에러나도 원본 보장

def next_id(items: list[dict]) -> int:
    if not items:
        return 1
    return max(int(x["id"]) for x in items) +1