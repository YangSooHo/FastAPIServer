from pydantic import BaseModel
from sqlalchemy import LargeBinary


class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class BoardBase(BaseModel):
    title: str
    content: str
    filename: str
    file_data: LargeBinary

class BoardCreate(BoardBase):
    pass

class BoardResponse(BoardBase):
    id: int

    class Config:
        from_attributes = True