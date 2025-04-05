from pydantic import Field

from schemas.mixin import AuditSchemaMixin


class UserBase(AuditSchemaMixin):
    name: str = Field(..., min_length=2, max_length=40) # ...는 필수 필드를 뜻함
    email: str = Field(..., min_length=8, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    name: str | None = Field(None, min_length=2, max_length=40) # None은 Optional 필드, 값이 없어도 됨
    email: str | None = Field(None, min_length=8, max_length=100)
    password: str | None = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True