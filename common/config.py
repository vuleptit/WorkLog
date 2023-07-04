from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME = "nguyentrungnghia.cnh@gmail.com",
    MAIL_PASSWORD = "tsnfblzbovskszqr",
    MAIL_FROM = "nguyentrungnghia.cnh@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="MAIL TITLE",
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)