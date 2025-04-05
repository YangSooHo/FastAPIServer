# from sqlalchemy import create_engine
import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

# SQLite DB
# DATABASE_URL = "sqlite:///./test.db"
#
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# # 의존성 주입 함수
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# 비동기 엔진 생성
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 세션 팩토리 생성
AsyncSessionLocal = sessionmaker(
    bind=engine, # database 연결 객체
    class_=AsyncSession, # 어떤 세션 클래스를 사용할 지 결정 (동기 Session / 비동기 AsyncSession)
    expire_on_commit=False # True면 commit() 한 후 객체의 속성이 DB에서 다시 로딩될 때까지 접근 불가. / False로 하면 commit() 후에도 기존 데이터 읽을 수 있음
)

# Base 클래스 생성
Base = declarative_base()

# DB 세션 의존성 주입 함수
async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except OperationalError as oError:
        print(f'데이터베이스 연결 실패 : {oError}')
    except Exception as e:
        print(f'기타 오류 발생 : {e}')

# 테이블 자동 생성
async def create_tables():
    try:
        print(settings.DATABASE_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f'Create Table 시도 중 오류 발생 : {e}')


if __name__ == "__main__":
    asyncio.run(create_tables()) # asyncio.run >> 비동기 함수를 메인 스레드동기처럼 실행