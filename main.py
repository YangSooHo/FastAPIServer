from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_db, create_tables


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

# 사용자 추가 API
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# 사용자 조회 API
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user