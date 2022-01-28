"""
App User model.
Define a single user inside the system if you want to have an internal auth system.
It's possible to define grant for admin with the flag: isAdmin.
The token is a different auth token that you can use if you don't want to use the user password.
"""


from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean

from app.src.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    token = Column(String)
    isAdmin = Column(Boolean, default=False)


class UserBase(BaseModel):
    username: str = None
    email: str = None
    name: Optional[str] = None
    surname: Optional[str] = None
    password: str = None
    token: Optional[str] = None
    isAdmin: bool = False


class UserRead(UserBase):
    id: Optional[int] = None


class UserCreate(UserBase):
    username: str
    email: str
    name: str
    surname: str
    password: str
    token: Optional[str]
    isAdmin: bool


class UserUpdate(UserBase):
    pass


class UserDelete(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserDataModel(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
    token: str
