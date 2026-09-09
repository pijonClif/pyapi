#psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

#sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)
#engine=create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)
#SessionLocal=async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base=declarative_base()


#sqlalchemy dependency

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#async def get_db():
#    async with SessionLocal() as db:
#        yield db

#connect to postgres
#while True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='12345', cursor_factory=RealDictCursor)
#        cursor=conn.cursor()
#        print("Database connection established")
#        break
#    except Exception as error:
#        print("Connecting to database failed")
#        print("Error: ", error)
#        time.sleep(2)