from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None 

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    
    class Config:
        orm_model=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 
    user_id: int

class TokenData(BaseModel):
    id: Optional[int]=None
    #created_at: datetime

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)