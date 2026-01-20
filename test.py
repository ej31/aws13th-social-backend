from utils.auth import hash_password, verify_password

plain = "P@ssw0rd!"

hashed = hash_password(plain)  # ✅ bcrypt 해시 생성

print(hashed)                  # $2b$12$...

print(verify_password(plain, hashed))
print(verify_password("wrong", hashed))
