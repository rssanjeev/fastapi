
from .. import models, schemas
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user  

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10):
    posts = db.query(models.Post).limit(limit).all()
    return posts

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        model_fields = {key: value for key, value in post.model_dump().items()}
        new_post = models.Post(owner_id=current_user.id, **model_fields)
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

@router.get("/{id}", response_model=schemas.PostResponse )
def get_post(id:int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists!")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action - This is not your post!")
    
    post.delete(synchronize_session=False)
    db.commit()
    return {"Post Deleted!"}


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)): 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action - This is not your post!")

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post is id: {id} deosnt exist!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    # Return the updated post object
    updated_post = post_query.first()
    return updated_post