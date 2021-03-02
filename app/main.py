from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import json
import datetime

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/records/", response_model=List[schemas.Record])
def show_records(db: Session = Depends(get_db)):
    records = db.query(models.Record).all()
    return records

@app.post("/records/")
def add_records(items: List[schemas.Record],db: Session = Depends(get_db)):
    models.Base.metadata.create_all(bind=engine)
    for item in items:
        items = item.dict()
        db_record = models.Record(
                id = None,
                date=items['date'],
                loc=items['loc'],
                temperature=items['temperature']
            )
        db.add(db_record)

        db.commit()


    records = db.query(models.Record).all()

    return records
    

@app.get("/records/{loc}")
def get_id(loc: str, maxi: Optional[bool] = None, mini: Optional[bool] = None, dt: Optional[int] = 24, db: Session = Depends(get_db)):
    if maxi:
        return db.query(models.Record).filter(models.Record.loc == loc).filter(models.Record.date >= (datetime.datetime.today() - datetime.timedelta(hours=dt))).order_by(models.Record.temperature.desc()).first()
    if mini:
        return db.query(models.Record).filter(models.Record.loc == loc).filter(models.Record.date >= (datetime.datetime.today() - datetime.timedelta(hours=dt))).order_by(models.Record.temperature).first()
    if loc == 'all':
        return db.query(models.Record).filter(models.Record.date >= (datetime.datetime.today() - datetime.timedelta(hours=dt))).all()
    return db.query(models.Record).filter(models.Record.loc == loc).filter(models.Record.date >= (datetime.datetime.today() - datetime.timedelta(hours=dt))).all()