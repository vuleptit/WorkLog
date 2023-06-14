from typing import Union
from api import user_api

from fastapi import FastAPI

app = FastAPI()

app.include_router(
    user_api.router,
    prefix="/user",
    tags=["user"]
)
