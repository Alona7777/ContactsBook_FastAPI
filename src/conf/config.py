from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_port: str

    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_y_username: str
    mail_y_password: str
    mail_y_from: str
    mail_y_port: int
    mail_y_server: str
    mail_sg_username: str
    mail_sg_password: str
    mail_sg_from: str
    mail_sg_port: int
    mail_sg_server: str
    redis_host: str = 'localhost'
    redis: int = 6379

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


class Config:
    DB_URL_ASYNG = "postgresql+asyncpg://postgres:12345@localhost:5432/contacts_app"
    DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/contacts_app"


config = Config