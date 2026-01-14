import json

def read_users():
    with open("data/users.json", "r", encoding="utf-8") as f:
        return json.load(f)

def write_users(users):
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
