from typing import List
from pydantic import Field

from schemas.mixin import AuditSchemaMixin


class BoardFilesBase(AuditSchemaMixin):
    filename: str = Field(..., min_length=1, max_length=256)
    original_filename: str = Field(..., min_length=1, max_length=256)

class BoardFilesCreate(BoardFilesBase):
    pass

class BoardFilesUpdate(BoardFilesBase):
    filename: str | None = Field(None, min_length=1, max_length=256)
    original_filename: str | None = Field(None, min_length=1, max_length=256)

class BoardFilesResponse(BoardFilesBase):
    id: int

    class Config:
        from_attributes = True


class BoardBase(AuditSchemaMixin):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=5000)

class BoardCreate(BoardBase):
    files: List[BoardFilesCreate] = Field(default_factory=list)

class BoardUpdate(BoardBase):
    title: str | None = Field(None, min_length=2, max_length=200)
    content: str | None = Field(None, min_length=2, max_length=5000)
    files: List[BoardFilesUpdate] | None = Field(default_factory=list)

class BoardResponse(BoardBase):
    id: int
    files: List[BoardFilesResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True