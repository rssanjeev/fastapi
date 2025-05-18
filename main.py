from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0

my_posts=[{"title": "title of post 1", "content":"content of post 1", "id":1},
            {"title":"title of post 2", "content":"content of post 2","id":2}]

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post):
    print(post)
    # return {"New Post": f"Title is {payload['title']}"}
    return {"New Post": post}