from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor 
from . import models, schemas, utils 
from .models import Post
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind= engine)

app = FastAPI() 
app.include_router(post.router)
app.include_router(user.router)


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

@app.get("/") 
async def root():  
    return {"message": "Hello"}


