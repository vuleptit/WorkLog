from typing import Union

from pydantic import BaseModel

class TaskBase(BaseModel):
    id: int
    name: str
    project_id: Union[int, None] = None
    code_on_jira: Union[str, None] = None

    class Config:
        orm_mode = True
        
        

