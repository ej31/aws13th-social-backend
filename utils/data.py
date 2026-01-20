# utils/data.py
import json
import os

# 프로젝트 루트 기준 data 폴더 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_data(filename: str):
    """JSON 파일을 읽어오는 '가져오는 방법' 정의"""
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        return []  # 파일이 없으면 빈 데이터 반환

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data, filename: str):
    """데이터를 파일에 기록하는 '담는 방법' 정의"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)  # data 폴더가 없으면 자동 생성

    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
