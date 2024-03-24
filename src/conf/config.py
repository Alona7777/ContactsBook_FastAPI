class Config:
    DB_URL_ASYNG = "postgresql+asyncpg://postgres:12345@localhost:5432/contacts_app"
    DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/contacts_app"


config = Config