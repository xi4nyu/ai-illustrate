from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import relationship

from database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('files_id_seq')"))
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(256), nullable=False)
    hash = Column(String(32), unique=True, index=True)
    file_path = Column(String(512), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    updated_uid = Column(Integer)

    owner = relationship("User")
