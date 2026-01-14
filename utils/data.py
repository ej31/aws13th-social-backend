import json

# 데이터 저장
def save_data(data, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 데이터 로드
def load_data(filename="data.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)