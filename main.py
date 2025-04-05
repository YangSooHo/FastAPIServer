from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables
from routers import user, board


# 비동기 설정
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버 시작!")  # 여기에 DB 연결 같은 초기화 코드 추가 가능

    # 테이블 생성
    await create_tables()
    print("Database Table Created !")

    yield  # 여기가 API 실행되는 동안 유지됨
    print("서버 종료!")  # 여기에 정리(clean-up) 코드 추가 가능

app = FastAPI(lifespan=lifespan)

#User Router
app.include_router(user.router)

#board Router
app.include_router(board.router)