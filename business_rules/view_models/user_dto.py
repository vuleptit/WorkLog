from typing import Union

from pydantic import BaseModel

class UserBase(BaseModel):
    user_name: str
    email: str
    phone: str
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str

class UserUpdate(BaseModel):
    id: int
    user_name: str
    email: str
    phone: str
    password: str
    is_active: bool
    
    class Config:
        orm_mode = True

    
