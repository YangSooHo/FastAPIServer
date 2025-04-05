from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base
from models.mixin import AuditMixin


class User(Base, AuditMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200), nullable=False)
    deleted = Column(Boolean, default=False)

    boards = relationship("Board", back_populates="user")
