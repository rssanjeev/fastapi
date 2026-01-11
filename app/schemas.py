from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    created_at: datetime

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    owner: UserOut
    owner_id: int

class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    Post: PostResponse
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int  # 1 for upvote, 0 for remove vote