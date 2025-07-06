from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    name: str
    user_id: int


class FileCreate(FileBase):
    hash: str
    file_path: str


class FileUpdate(BaseModel):
    name: Optional[str] = None


class FileInDBBase(FileBase):
    id: int
    hash: str
    file_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class File(FileInDBBase):
    pass
