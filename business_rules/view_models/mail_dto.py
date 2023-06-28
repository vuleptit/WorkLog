from typing import Union
from pydantic import BaseModel, EmailStr
from typing import List
from enum import Enum

class MessageType(Enum):
    plain = "plain"
    html = "html"

class EmailSchema(BaseModel):
    subject: str = None
    recipients: List[EmailStr]
    body: str = None
    subtype: Union[MessageType, str] = "plain"
    class Config:
        orm_mode = True
