from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    user_name: str
    email: str
    phone: str
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str