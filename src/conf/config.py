from pydantic import ConfigDict, validator
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
 
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
 
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: int = 818941732257654
    CLOUDINARY_API_SECRET: str = 'secret'
    
    model_config = ConfigDict(extra='ignore', env_file='.env', env_file_decoding='utf-8')
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"


config= Settings()


