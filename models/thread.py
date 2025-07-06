from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, text
from sqlalchemy.orm import relationship

from database import Base


class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('thread_id_seq')"))
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(128), nullable=False)
    summary = Column(String(512))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User")
    conversations = relationship("Conversation", back_populates="thread")
