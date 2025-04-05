from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud.board as board_crud
from schemas.board import BoardResponse, BoardCreate, BoardUpdate

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.get("/{board_id}")
async def get_board(board_id: int, db: AsyncSession = Depends(get_db)):
    board = board_crud.get_board(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@router.post("/create", response_model=BoardResponse)
async def create_board(board: BoardCreate, db: AsyncSession = Depends(get_db)):
    return await board_crud.create_board(db, board)

@router.put("/{board_id}")
async def update_board(board_id : int, board: BoardUpdate, db: AsyncSession = Depends(get_db)):
    return await board_crud.update_board(db, board_id, board)

@router.delete("/{board_id}")
async def delete_board(board_id: int, db: AsyncSession = Depends(get_db)):
    return await board_crud.delete_board(db, board_id)