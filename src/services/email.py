import certifi
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service

# 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

# certificate = certifi.where()
conf = ConnectionConfig(
    MAIL_USERNAME="fatsapiuser@meta.ua",
    MAIL_PASSWORD="pythonCourse2023",
    MAIL_FROM="fatsapiuser@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="TODO Systems",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)
# conf = ConnectionConfig(
#     MAIL_USERNAME="contactsbook_fastapi@yahoo.com",
#     MAIL_PASSWORD="Fast12345678api",
#     MAIL_FROM="contactsbook_fastapi@yahoo.com",
#     MAIL_PORT=465,
#     MAIL_SERVER="smtp.mail.yahoo.com",
#     MAIL_FROM_NAME="Contact Book Assistant",
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,   #certifi.where()
#     TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
# )
# conf = ConnectionConfig(
#     MAIL_USERNAME="apikey",
#     MAIL_PASSWORD="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",
#     MAIL_FROM="contactsbook_fastapi@yahoo.com",
#     MAIL_PORT=465,
#     MAIL_SERVER="smtp.sendgrid.net", 
#     MAIL_FROM_NAME="Contact Book Assistant",
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     # MAIL_TLS=True,
#     # MAIL_SSL=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
#     TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
# )


async def send_email(email: EmailStr, username: str, host: str):
    try: 
        token_verification = auth_service.create_email_token({'sub': email})
        message = MessageSchema(
            subject='Confirm your email',
            recipients=[email],
            template_body={'host': host, 'username': username, 'token': token_verification},
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name='verify_email.html')
    except ConnectionErrors as err:
        print(err)



