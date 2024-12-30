from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    email:EmailStr
    id: int
    created_at: datetime
    class Config:
        from_attributes=True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value will be true if user doesnt populate this in req
    owner_id: int
    owner: UserOut
    #the below is required to convert ORM model to pydantic dict model before sending the response
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post:Post
    votes: int
    class Config:
        from_attributes:True

class UserCreate(BaseModel):
    email:EmailStr
    password:str    
    


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id:int
    vote_dir:int