
from .. import models, schemas, utils 
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/posts")
def get_posts(db: Session = Depends(get_db), response_model=list[schemas.PostResponse]):
    posts = db.query(models.Post).all()
    return posts 

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
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

@router.get("/posts/{id}")
def get_post(id:int, response: Response, db: Session = Depends(get_db), response_model=schemas.PostResponse):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT ) 
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    post.delete(synchronize_session=False)
    db.commit()
    return {"Post Deleted!"}


@router.put("/posts/{id}")
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db)): 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post is id: {id} deosnt exist!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message":"Post Updated"}

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user