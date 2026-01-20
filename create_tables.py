from data.database import engine
from data.models import Base
import data.models


def init_db():
    print(" 테이블 생성을 시작합니다")

    Base.metadata.create_all(bind=engine)

    print("테이블 생성이 완료되었습니다")

if __name__ == "__main__":
    init_db()