from pydantic import BaseModel, EmailStr
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

class PostResponse(PostBase): 
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None