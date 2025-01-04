from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr
from typing import Optional

Base = declarative_base()


class User(Base):
    """Таблица пользователя в БД"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    useremail = Column(String(50), nullable=False, unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
    user_status = Column(Integer, default=0, nullable=False)


class UserBase(BaseModel):
    useremail: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_status: Optional[int] = None


class UserInDB(UserBase):
    useremail: EmailStr
    hashed_password: str
