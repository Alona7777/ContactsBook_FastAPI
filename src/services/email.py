from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import config


conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME="Contact Book Assistant",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to verify their account.
        The function takes in three parameters:
            - email: the user's email address, as a string.
            - username: the user's username, as a string.  This is used for personalization of the message body and subject line.
            - host: this is used for personalization of the message body and subject line.
    
    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username to the template
    :param host: str: Pass the host url to the email template
    :return: A coroutine, which is an object that can be executed by the asyncio event loop
    :doc-author: Trelent
    """
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



