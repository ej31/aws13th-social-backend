from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#데이터 베이스 창구...? 여는법이라는데
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:kst500132*@localhost:3306/fastapi_assignment"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 실제 디비 실행어
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()