from hashids import Hashids
from passlib.context import CryptContext

from common.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

hashids = Hashids(salt=settings.HASHIDS_SALT,min_length=8)

#비밀번호 해시함수로 저장
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#비밀번호 해시함수로 검증
def verify_password(password: str,hashed_password: str ) -> bool:
    return pwd_context.verify(password, hashed_password)

#id salt 함수로 암호화
def encode_id(id: int) -> str:
    return hashids.encode(id)

#salt 함수로 암호화 된 id 복호화
def decode_id(id: str) -> int:
    decoded = hashids.decode(id)
    # 해시를 하게 되면 튜플 형식으로 저장됨 (6,)... 그렇기에 [0]번째 인수만 반환하게 함
    return decoded[0] if decoded else None


