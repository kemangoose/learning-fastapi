from pydantic import BaseModel, EmailStr 
from pydantic.types import conint
from datetime import datetime

class User(BaseModel):
     email:EmailStr

class UserIn(User):
     password:str

class UserOut(User):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str 

class TokenData(BaseModel):
    id:int

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Posts:Post
    votes:int

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)