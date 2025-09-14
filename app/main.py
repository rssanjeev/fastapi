from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor 
from . import models, schemas
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



my_posts=[{"title": "title of post 1", "content":"content of post 1", "id":1},
            {"title":"title of post 2", "content":"content of post 2","id":2}]

@app.get("/")
async def root():
    return {"message": "Hello"}
 
@app.get("/posts")
def get_posts(db: Session = Depends(get_db), response_model=list[schemas.PostResponse]):
    posts = db.query(models.Post).all()
    return posts 

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        model_fields = {key: value for key, value in post.model_dump().items()}
        new_post = models.Post(**model_fields)
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
def get_post(id:int, response: Response, db: Session = Depends(get_db), response_model=schemas.PostResponse):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT ) 
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    post.delete(synchronize_session=False)
    db.commit()
    return {"Post Deleted!"}


@app.put("/posts/{id}")
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db)): 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post is id: {id} deosnt exist!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message":"Post Updated"}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user. ())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  