from typing import Union

from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str
    project_id: int = None
    code_on_jira: Union[str, None] = None

    class Config:
        orm_mode = True
        
class TaskUpdate(BaseModel):
    id: int
    name: str
    project_id: int = None
    code_on_jira: Union[str, None] = None

    class Config:
        orm_mode = True