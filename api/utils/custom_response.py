from pydantic import BaseModel
from typing import Union
from fastapi import status
class CustomResponse(BaseModel):
    message: Union[str, None] = ""
    data: Union[dict, list, None] = None
    status: int
    exception: Union[str, None] = ""