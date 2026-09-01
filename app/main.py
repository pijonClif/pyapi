import time
from typing import Optional, List
from random import randrange

#fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

#psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

#sqlalchemy
from sqlalchemy.orm import Session
from .database import engine, get_db

from . import models, schemas, utils
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

#connect to postgres
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection established")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

#sqlalchepy test path
#@app.get("/sqlalchemy")
#def test_post(db: Session=Depends(get_db)):
#    posts=db.query(models.Post).all()
#    return{"data":posts}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



