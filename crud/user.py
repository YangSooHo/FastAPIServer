from typing import List, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from models.user import User
from schemas.user import UserCreate, UserUpdate


# 사용자 생성
async def create_user(db: AsyncSession, user_create: UserCreate) -> Optional[User]:
    existing = await db.execute(select(User).where(and_(User.email == user_create.email, User.deleted == False)))
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
        print(f"User Update 실패: {e}")
        raise HTTPException(status_code=500, detail="사용자 정보 업데이트 중 오류가 발생했습니다.")


#사용자 전체 조회
async def get_all_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return list(result.scalars().all())

# 사용자 조회 0 ~ 10 - List / total
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> Tuple[List[User], int]:
    # 사용자 목록
    result = await db.execute(select(User).where(User.deleted == False).offset(skip).limit(limit))
    boards = list(result.scalars().all())

    # 전체 개수
    total_result = await db.execute(select(func.count(User.id)))
    total = total_result.scalar()

    return boards, total

# 사용자 id 조회
async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(and_(User.id == user_id, User.deleted == False)))
    return result.scalar_one_or_none()
    # scalars().one_or_none하고 동일함
    # select(User)를 one_or_none로 호출 시 튜플로 감싸서 나옴

# 사용자 email 조회
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(and_(User.email == email, User.deleted == False)))
    return result.scalar_one_or_none()

async def delete_user(db: AsyncSession, user_id: int) -> Optional[User]:
    try:
        user = await get_user(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail=f"사용자를 찾을 수 없습니다. {user_id}")

        # 데이터 업데이트 - deleted True로 업데이트
        setattr(user, "deleted", True)

        await db.commit()
        await db.refresh(user)
        return user

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"User Delete 실패: {e}")
        raise HTTPException(status_code=500, detail="사용자 정보 업데이트 중 오류가 발생했습니다.")

