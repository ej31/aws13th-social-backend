import json
import os

def load_data(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, 'r', encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)