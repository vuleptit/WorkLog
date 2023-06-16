from pydantic import BaseModel
from typing import List, Union, Dict

class ResponseModel(BaseModel):
    message: Union[str, None] = ""
    data: Union[dict, None] = None
    status: int
    exception: Union[str, None] = ""