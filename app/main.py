from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor 


app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', 
                                user='postgres', password='sarcasm1@123', 
                                cursor_factory=RealDictCursor, port=5433)  
        cursor = conn.cursor()
        print("Successfully connected!")
        break
    except Exception as error:
        print(f"Connection Failed:", error)
        time.sleep(3)

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
    for i, p in enumerate(my_posts):
        if p['id']==id: return i

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    # print(find_post(id))
    if not find_post(id): 
        # response.status_code = status.HTTP_404_NOT_FOUND  
        # return {"message":f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    return {"post details":find_post(id)}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT ) 
def delete_post(id:int):
    # print("Deleting...")
    # i, post = find_post(id)
    if find_post(id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!") 
    else: my_posts.pop(find_post(id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_post(id)

    if index is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                          detail=f"Post is id: {id} deosnt exist!")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message":"Post Updated"}