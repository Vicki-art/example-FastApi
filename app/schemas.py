from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config():
        orm_mode = True


####CREATE USER 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
   
    class Config():
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str



#####CREATE POST

class CreatedPost(PostBase):
    pass





#####RESPONSE MODEL

class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    owner: CreateUserResponse
    id: int

    class Config():
        orm_mode = True

class PostOut(BaseModel): 
    Post: PostResponse
    votes: int

    class Config():
        orm_mode = True


##### AUTHENTIFICATION 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None 
    # id: int




##### VOTES
class Vote(BaseModel):
    post_id: int
    dir: conint(le = 1)
           



