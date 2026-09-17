#fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#sqlalchemy
from .database import engine, get_db

from . import models
from .config import settings
from .routers import post, user, auth, vote

#initialises db tables by sqlalchemy
#but we got alembic now tho dont need it

#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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



#DATABASE_HOSTNAME=localhost
#DATABASE_HOSTNAME_REMOTE=postgres
#DATABASE_PORT=5432
#DATABASE_PASSWORD=12345
#DATABASE_NAME=fastapi
#DATABASE_USERNAME=postgres

#SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
#ALGORITHM=HS256
#ACCESS_TOKEN_EXPIRE_MINUTES=30
