from sqlalchemy import Column, Integer, String
from data.database import Base


# 유저 테이블 만드는 로직
class User(Base):
    __tablename__ = "User_data"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True,index=True)
    password = Column(String(255))
    nickname = Column(String(50),index=True,unique=True)
    profile_img = Column(String(255), nullable=True)

