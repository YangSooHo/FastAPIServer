from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base
from models.mixin import AuditMixin


class Board(Base, AuditMixin):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    content = Column(String(5000))
    deleted = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    # 관계 설정 (Board -> User / BoardFiles -> Board)
    user = relationship("User", back_populates="boards")
    boardFiles = relationship("BoardFiles", back_populates="board")

class BoardFiles(Base, AuditMixin):
    __tablename__ = "board_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(256), index=True)
    original_filename = Column(String(256))
    deleted = Column(Boolean, default=False)
    data = Column(LargeBinary)

    board_id = Column(Integer, ForeignKey("boards.id"))

    board = relationship("Board", back_populates="boardFiles")
