from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    role: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserUpdate(BaseModel):
    role: Optional[str] = None
    password: Optional[str] = None
    updated_uid: Optional[int] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
