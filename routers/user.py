from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud.user as crud_user
from database import get_db
from schemas.common import PageResponse, PageInfo
from schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# 사용자 생성 : C
@router.post("/", response_model=UserResponse)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.create_user(db, user_create)
    if not user:
        raise HTTPException(status_code=400, detail="사용자 생성 실패")
    return user

# 사용자 전체 목록 : R
@router.get("/all", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await crud_user.get_all_users(db)
    return users

# 사용자 페이지 목록 : R
@router.get("/", response_model=PageResponse[UserResponse])
async def get_users(page_info: PageInfo = Depends(), db: AsyncSession = Depends(get_db)):
    users, total = await crud_user.get_users(db, skip=page_info.skip, limit=page_info.limit)

    return PageResponse[UserResponse](
        items=users,
        total=total,
        page_info=page_info
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user(db, user_id)
    return user

# 사용자 수정 : U
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user

# 사용자 삭제 : D
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"detail": "삭제되었습니다."}