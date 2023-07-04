from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from business_rules.view_models.mail_dto import EmailSchema, MessageType
from fastapi import APIRouter, Depends, Response
from business_rules.task_service import *
from database_settings import get_db
from common.config import conf

router = APIRouter()

@router.post('/send/')
async def send_mail(email: EmailSchema):
    content = "This is a test email"
    subject = "TEST EMAIL SUBJECT"
    message = MessageSchema(
        subject=subject,
        recipients=email.recipients,
        body=content,
        subtype="plain"
    )
    postman = FastMail(conf)
    await postman.send_message(message)
    return CustomResponse(
        message = "Successfully",
        status = status.HTTP_201_CREATED
    )

    