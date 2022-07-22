from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


#Schema/Pydentic Models define the structure of a request & response
#This ensure that when an user create a post, the request will only go through if it has a "title"
# and a "content" in the body
class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode = True

class PostVote(PostBase):
    Post:PostOut 
    votes:int
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)