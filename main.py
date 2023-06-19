from typing import Union
from api import user_api, task_api, project_api, jwt_api

from fastapi import FastAPI

app = FastAPI()

app.include_router(
    user_api.router,
    prefix="/user",
    tags=["user"]
)
app.include_router(
    task_api.router,
    prefix="/task",
    tags=["task"]
)
app.include_router(
    project_api.router,
    prefix="/project",
    tags=["project]"]
)

app.include_router(
    jwt_api.router,
    prefix="/token",
    tags=["token"]
)


