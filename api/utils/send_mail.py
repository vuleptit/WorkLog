from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from getpass import getpass
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]

# password = getpass()
conf = ConnectionConfig(
    MAIL_USERNAME = "nguyentrungnghia.cnh@gmail.com",
    MAIL_PASSWORD = "tsnfblzbovskszqr",
    MAIL_FROM = "nguyentrungnghia.cnh@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="MAIL TITLE",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
)
app = FastAPI()



@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    # print(conf.MAIL_PASSWORD)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})