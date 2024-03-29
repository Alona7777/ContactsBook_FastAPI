import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from src.routes import contacts, one_contact, auth, full_access

from src.schemas.contacts import ContactResponse
from src.database.db import get_db
from src.database.models import Contact
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(one_contact.router, prefix='/api')
app.include_router(full_access.router, prefix='/api')


@app.get('/')
def read_root():
    return {"message": "Hello World"}

@app.get('/api/healthchecker')
async def healthchecker(db: Session = Depends(get_db)):
    try:
        result = await db.execute(text('SELECT 1'))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail='Database is not configured correctly')
        return {"message": "Welcome to FastAPI"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error connecting to the database')



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )
 