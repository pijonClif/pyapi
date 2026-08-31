from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import schemas

import time
from typing import Optional, List
from random import randrange

#psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

#sqlalchemy
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()

    posts=db.query(models.Post).all()
    return posts

@app.get("/posts/latest")
def get_latest_post(db: Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    #latest_post=cursor.fetchone()   

    latest_post=db.query(models.Post).order_by(models.Post.id.desc()).first()
    return{"detail": latest_post}

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    #post=cursor.fetchone()

    post=db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return {"detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    #new_post=cursor.fetchone()
    #conn.commit()

    #new_post=models.Post(title=post.title, content=post.content, published=post.published)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()

    post_query= db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
    #return{"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post_query.delete(synchronize_session=False)
    db.commit()
    #return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user