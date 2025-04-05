from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.user import UserCreate, UserUpdate
from models.user import User


# 사용자 생성
async def create_user(db: AsyncSession, user_create: UserCreate) -> Optional[User]:
    existing = await db.execute(select(User).where(User.email == user_create.email))
    if(existing.scalar_one_or_none()):
        raise HTTPException(status_code=404, detail=f"이미 존재하는 사용자입니다. - {user_create.email}")
        #print(f"Already exists User : {user_create.email}")
        #return None #이미 존재하는 경우 None

    # ** : Dictionary Unpacking >> {"name": "Test", "email": "test@example.com"} => name="Test", email="test@example.com로 동작
    db_user = User(**user_create.model_dump())
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Create User Error : {e}")
        raise e

# 사용자 수정
async def update_user(db: AsyncSession, user_id : int, user_update: UserUpdate) -> Optional[User]:
    try:
        #사용자 검색
        user = await get_user(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail=f"사용자를 찾을 수 없습니다. {user_id}")

        # 데이터 업데이트
        # exclude_unset=True > 값이 그대로인 필드는 제외
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        return user

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Update 실패: {e}")
        raise e


#사용자 전체 조회
async def get_all_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return list(result.scalars().all())

# 사용자 조회 0 ~ 10
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())

# 사용자 id 조회
async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
    # scalars().one_or_none하고 동일함
    # select(User)를 one_or_none로 호출 시 튜플로 감싸서 나옴

# 사용자 email 조회
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()