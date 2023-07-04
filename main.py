from api import send_mail_api, user_api, task_api, project_api, jwt_api, dailychecklist_api, worklog_api, setting_api
import time
from fastapi import FastAPI, Request
from common.middleware import permission
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

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
    tags=["project"]
)

app.include_router(
    dailychecklist_api.router,
    prefix="/checklist",
    tags=["checklist"]
)

app.include_router(
    jwt_api.router,
    prefix="/token",
    tags=["token"]
)

app.include_router(
    worklog_api.router,
    prefix="/worklog",
    tags=["worklog"]
)

app.include_router(
    setting_api.router,
    prefix="/setting",
    tags=["setting"]
)

app.include_router(
    send_mail_api.router,
    prefix="/email",
    tags=["email"]
)