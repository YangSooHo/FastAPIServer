from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.board import Board, BoardFiles
from schemas.board import BoardCreate, BoardUpdate


# Board 생성
async def create_board(db: AsyncSession, board_create: BoardCreate) -> Optional[Board]:
    try:
        board = Board(**board_create.model_dump(exclude_unset=True))
        board.created_at = datetime.now(timezone.utc)
        db.add(board)
        await db.refresh(board) # board.id 확보를 위한 flush

        # 첨부파일 생성
        for file in board_create.files:
            board_file = BoardFiles(**file.model_dump(exclude_unset=True), board_id=board.id)
            db.add(board_file)

        await db.commit()
        await db.refresh(board)
        return board

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Create Board Error : {e}")
        raise HTTPException(status_code=500, detail="게시글 등록 중 오류가 발생 했습니다.")

# Board 수정
async def update_board(db: AsyncSession, board_id : int, board_update: BoardUpdate) -> Optional[Board]:
    try:
        result = await db.execute(select(Board).where(Board.id == board_id))
        board = result.scalar_one_or_none()

        if not board:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

        for field, value in board_update.model_dump(exclude_unset=True).items():
            setattr(board, field, value)

        await db.commit()
        await db.refresh(board)
        return board

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Update Board Error: {e}")
        raise HTTPException(status_code=500, detail="게시글 수정 중 오류가 발생했습니다.")

# Board 삭제
async def delete_board(db: AsyncSession, board_id: int) -> Optional[Board]:
    try:
        result = await db.execute(select(Board).where(Board.id == board_id))
        board = result.scalar_one_or_none()

        if not board:
            raise HTTPException(status_code=404, detail=f"삭제할 게시글을 찾을 수 없습니다.")

        await db.delete(board)
        await db.commit()
        await db.refresh(board)

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Delete Board Error : {e}")
        raise HTTPException(status_code=500, detail="게시글 삭제 중 오류가 발생했습니다.")


# Board 불러오기
async def get_board(db: AsyncSession, board_id: int) -> Optional[Board]:
    result = await db.execute(select(Board).where(Board.id == board_id))
    board = result.scalar_one_or_none()

    if not board:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    return board

async def get_all_boards(db: AsyncSession) -> List[BoardFiles]:
    result = await db.execute(select(BoardFiles))
    return list(result.scalars().all())

async def get_boards(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Board]:
    result = await db.execute(select(Board).offset(skip).limit(limit))
    return list(result.scalars().all())