# from sqlalchemy import create_engine
import asyncio
import urllib.parse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


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

username = urllib.parse.quote_plus("postgres")
password = urllib.parse.quote_plus("test123!@#")

DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@localhost:5432/fast_api"

# 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 생성
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base 클래스 생성
Base = declarative_base()

# DB 세션 의존성 주입 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 테이블 자동 생성
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())