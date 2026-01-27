# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
#
# from core.db_connection import get_db_connection
#
# con = None
# try:
#     con = get_db_connection()
#
#     host = con.host
#     port = con.port
#     user = con.user
#     password = con.password
#     db = con.db
#     charset = con.charset
#
#     URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}'
#     print(URL)
#     engine = create_engine(URL, echo=True)
#
#     Base = declarative_base()
#
# finally:
#     if con:
#         con.close()

#
#
# import os
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import declarative_base, sessionmaker
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # 1. 설정값 통합 관리 (보통 .env에서 읽어옴)
# DB_USER = os.getenv("DB_USER", "root")
# DB_PW = os.getenv("DB_PASSWORD", "1234")
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "3306")
# DB_NAME = os.getenv("DB_NAME", "mydb")
#
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
#
# # 2. SQLAlchemy 엔진 생성 (애플리케이션 전체에서 하나만 생성)
# engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#
# # ---------------------------------------------------------
# # 방식 A: SQLAlchemy ORM 사용 시
# # ---------------------------------------------------------
# def use_orm():
#     db = SessionLocal()
#     try:
#         # user = db.query(User).first()
#         pass
#     finally:
#         db.close()
#
# # ---------------------------------------------------------
# # 방식 B: PyMySQL처럼 Raw Query (Native) 사용 시
# # ---------------------------------------------------------
# def use_native_query():
#     # 별도의 PyMySQL 커넥션을 맺지 않고, engine에서 바로 커넥션을 빌려옵니다.
#     # 이 방식이 성능과 커넥션 풀 관리 면에서 훨씬 유리합니다.
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT * FROM users WHERE id = :id"), {"id": 1})
#         for row in result:
#             print(row)


