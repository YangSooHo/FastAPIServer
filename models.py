from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
import asyncio

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    # 관계 설정 (BoardFiles -> Board)
    boardFiles = relationship("BoardFiles", back_populates="board")

class BoardFiles(Base):
    __tablename__ = "board_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    data = Column(LargeBinary)

    file_id = Column(Integer, ForeignKey("boards.id"))

    board = relationship("Board", backref="boardFiles")

