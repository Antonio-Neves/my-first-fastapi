from fastapi import FastAPI, Depends
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_all(db: db_dependecy):
    return db.query(Todos).all()
