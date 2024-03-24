import uvicorn
from fastapi import FastAPI

from src.routes import contacts, one_contact

from src.schemas.contacts import ContactResponse
from src.database.db import SessionLocal
from src.database.models import Contact
from sqlalchemy.orm import Session

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(one_contact.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )