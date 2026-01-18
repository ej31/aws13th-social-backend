import bcrypt


# 1. 비밀번호 해싱 (문자열 -> 암호화된 문자열)
def get_password_hash(password: str) -> str:
    # 비밀번호를 바이트(bytes)로 변환
    password_bytes = password.encode('utf-8')

    # 소금(salt) 생성 및 해싱
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # DB(JSON)에 저장하기 위해 bytes를 다시 문자열(str)로 변환해서 반환
    return hashed_password.decode('utf-8')


# 2. 비밀번호 검증 (입력받은 비밀번호 vs 저장된 암호)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 둘 다 바이트(bytes)로 변환해서 비교해야 함
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # bcrypt 라이브러리가 알아서 비교해줌 (True/False)
    return bcrypt.checkpw(plain_bytes, hashed_bytes)