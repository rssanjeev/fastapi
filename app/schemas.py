from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass