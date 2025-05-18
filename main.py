from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

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
def get_posts():
    print(my_posts)
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000 )
    my_posts.append(post_dict)
    return {"New Post": post_dict}

def find_post(id):
    for p in my_posts:
        if p['id']==id: return p

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    # print(find_post(id))
    if not find_post(id): 
        # response.status_code = status.HTTP_404_NOT_FOUND  
        # return {"message":f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    return {"post details":find_post(id)}
