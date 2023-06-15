from typing import Union

from pydantic import BaseModel

class ProjectBase(BaseModel):
    id: int
    name: str
    code_on_jira: Union[str, None] = None

    class Config:
        orm_mode = True

