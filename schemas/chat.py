from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Conversation Schemas ---


class ConversationBase(BaseModel):
    content: str


class ConversationCreate(ConversationBase):
    user_id: int
    thread_id: int


class Conversation(ConversationBase):
    id: int
    user_id: int
    thread_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# --- Thread Schemas ---


class ThreadBase(BaseModel):
    title: str
    user_id: int


class ThreadCreate(ThreadBase):
    pass


class ThreadUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None


class Thread(ThreadBase):
    id: int
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    conversations: List[Conversation] = []

    class Config:
        orm_mode = True
