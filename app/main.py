#fastapi
from fastapi import FastAPI

#sqlalchemy
from .database import engine, get_db

from . import models
from .config import settings
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

#sqlalchepy test path
#@app.get("/sqlalchemy")
#def test_post(db: Session=Depends(get_db)):
#    posts=db.query(models.Post).all()
#    return{"data":posts}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



