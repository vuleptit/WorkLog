from pydantic import BaseModel
from typing import List, Union, Dict

class ResponseModel(BaseModel):
    message: Union[str, None] = None
    data: Union[dict, None] = None
    status: int
    exception: str = ""