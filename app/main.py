from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
from . import models, schemas, utils 
from .models import Post
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind= engine)

app = FastAPI() 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") 
async def root():  
    return {"message": "Hello"}
