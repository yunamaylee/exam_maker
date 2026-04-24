from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import DATABASE_URL

# engine과 SessionLocal을 함수로 감싸서 import 시점에 DB 연결 방지
# 테스트 환경에서 DATABASE_URL이 없어도 import 가능
def get_engine():
    return create_engine(DATABASE_URL)


def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()