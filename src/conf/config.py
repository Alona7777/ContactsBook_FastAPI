class Config:
    DB_URL_ASYNG = "postgresql+asyncpg://postgres:12345@localhost:5432/rest_api"
    DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/rest_api"


config = Config