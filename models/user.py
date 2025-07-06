from sqlalchemy import Column, DateTime, Integer, String, func, text

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('users_id_seq')"))
    username = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(64), nullable=False)
    role = Column(String(256))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    updated_uid = Column(Integer)
