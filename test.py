from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship
import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent
env_db_path = BASE_DIR / "./core/.env_DB"

# verbose=True를 넣으면 로드 과정을 상세히 출력해줍니다.
if load_dotenv(dotenv_path=env_db_path, verbose=True):
    print(f"✅ .env_DB 로드 성공! (경로: {env_db_path})")
else:
    print(f"❌ .env_DB 로드 실패! (파일이 해당 경로에 있는지 확인하세요: {env_db_path})")

host=os.getenv("MYSQL_HOST")
port=int(os.getenv("MYSQL_PORT"))
user=os.getenv("MYSQL_USER")
password=os.getenv("MYSQL_PASSWORD")
db=os.getenv("MYSQL_DB")
charset=os.getenv("MYSQL_CHARSET")

URL =   f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}'
engine = create_engine(URL, echo=True)
Base = declarative_base()


class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    member_list = relationship('Member', back_populates='belong_to_team')

    def __repr__(self):
        return f"<Team(team_id={self.team_id}, name='{self.name}')>"


class Member(Base):
    __tablename__ = 'members'

    member_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    belong_to_team = relationship('Team', back_populates='member_list')

    def __repr__(self):
        return f"<Member(member_id={self.member_id}, name='{self.name}')>"


# ============================================================
# 4. CRUD 함수들
# ============================================================
def create_data():
    with Session(engine) as session:
        dev_team = Team(team_id=10, name="개발팀")
        design_team = Team(team_id=20, name="디자인팀")

        jeff = Member(member_id=1, name="임제프",belong_to_team=dev_team)
        chulsoo = Member(member_id=2, name="김철수", belong_to_team=dev_team)
        younghee = Member(member_id=3, name="이영희", belong_to_team=design_team)

        session.add(dev_team)
        session.add(design_team)
        session.add_all([jeff, chulsoo, younghee])
        session.commit()

        print("\n=== 데이터 생성 완료 ===")


def read_data():
    with Session(engine) as session:
        print("\n=== PK로 조회 ===")
        member = session.get(Member, 1)
        print(f"멤버: {member.name}")

        print("\n=== 연관 객체 탐색 ===")
        print(f"소속팀: {member.belong_to_team.name}")

        print("\n=== 반대 방향 탐색 ===")
        team = session.get(Team, 10)
        for m in team.member_list:
            print(f"  - {m.name}")


def update_data():
    with Session(engine) as session:
        member = session.get(Member, 1)
        member.name = "임제프(수정됨)"
        session.commit()
        print(f"\n=== 수정 완료: {member} ===")


def delete_data():
    with Session(engine) as session:
        member1 = session.get(Member, 1)
        member2 = session.get(Member, 2)
        member3 = session.get(Member, 3)
        session.delete(member1)
        session.delete(member2)
        session.delete(member3)
        session.commit()
        print("\n=== 삭제 완료 ===")


def run_all():
    print("=" * 50)
    print("SQLAlchemy ORM CRUD 실습")
    print("=" * 50)
    # create_data()
    # read_data()
    # update_data()
    delete_data()
    print("\n실습 완료!")


if __name__ == "__main__":
    run_all()