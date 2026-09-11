
from typing import List, Optional

#fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

#sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import engine, get_db

from .. import models, schemas, oauth2

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session=Depends(get_db), limit: int=5, skip: int=0, search: Optional[str]="", current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()

    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    post_query=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id)
    posts=post_query.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.get("/latest", response_model=schemas.PostOut)
async def get_latest_post(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    #latest_post=cursor.fetchone()   

    post_query=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id)
    latest_post=post_query.order_by(models.Post.id.desc()).first()
    return latest_post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    #post=cursor.fetchone()

    post_query=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id)
    post=post_query.filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return post

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    #new_post=cursor.fetchone()
    #conn.commit()

    #new_post=models.Post(title=post.title, content=post.content, published=post.published)

    # print(current_user.email)
    new_post=models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()

    post_query= db.query(models.Post).filter(models.Post.id == id)
    update_post=post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if update_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
    #return{"data": updated_post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    #return Response(status_code=status.HTTP_204_NO_CONTENT)
