from typing import Union

from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    code_on_jira: Union[str, None] = None

    class Config:
        orm_mode = True
        
class ProjectUpdate(BaseModel):
    id: int
    name: str
    code_on_jira: Union[str, None] = None

    class Config:
        orm_mode = True