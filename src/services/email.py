from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="TODO Systems",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)
# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.mail_y_username,
#     MAIL_PASSWORD=settings.mail_y_password,
#     MAIL_FROM=settings.mail_y_from,
#     MAIL_PORT=settings.mail_y_port,
#     MAIL_SERVER=settings.mail_y_server,
#     MAIL_FROM_NAME="Contact Book Assistant",
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,   #certifi.where()
#     TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
# )
# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.mail_sg_username,
#     MAIL_PASSWORD=settings.mail_sg_password,
#     MAIL_FROM=settings.mail_sg_from,
#     MAIL_PORT=settings.mail_sg_port,
#     MAIL_SERVER=settings.mail_sg_server, 
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



