import uvicorn
from fastapi import FastAPI, Response

from src.routes import contacts

from src.schemas.schema_contacts import ContactResponse
from src.database.db import SessionLocal
from src.database.models import Contact
from sqlalchemy.orm import Session

app = FastAPI()

app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

# @app.get('/contacts',responses=ContactResponse, tags=["contacts"])
# def read_contacts(db: Session):
#     contacts = db.query(Contact).all()
#     return Response(content=contacts, media_type="application/json")
#     # return contacts
    
# @app.get("/cats", response_model=list[ContactResponse], tags=["contacts"])
# async def get_cats(db: Session):
#     contacts = db.query(Contact).all()
#     return contacts

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )