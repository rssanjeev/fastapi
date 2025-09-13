from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor 
from . import models
from .models import Post
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind= engine)

app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts} 




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
def get_posts(db: Session = Depends(get_db)):
    # print(my_posts)
    # cursor.execute(""" SELECT * FROM POSTS """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    try:
        # Filter only model fields
        # print({key: value for key, value in post.model_dump().items()})
        model_fields = {key: value for key, value in post.model_dump().items()}
        new_post = models.Post(**model_fields)
        print(new_post)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

def find_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id: return i

@app.get("/posts/{id}")
def get_post(id:int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    return {"post details":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT ) 
def delete_post(id:int):
    cursor.execute("DELETE FROM POSTS WHERE ID = %s RETURNING *", (str(id)))
    result = cursor.fetchall()
    if len(result) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"Post Deleted!"}


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    # index = find_post(id)

    # if index is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                                       detail=f"Post is id: {id} deosnt exist!")
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    cursor.execute("UPDATE POSTS SET TITLE = %s, CONTENT = %s, PUBLISHED = %s WHERE ID = %s RETURNING *",
                    (post.title, post.content, post.published, id))
    conn.commit()
    result = cursor.fetchall()
    if len(result)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post is id: {id} deosnt exist!")
    return {"message":"Post Updated"}