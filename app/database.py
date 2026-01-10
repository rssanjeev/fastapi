import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQL_ALCHEMY_DATABASE = settings.database_url
print("Database URL:", SQL_ALCHEMY_DATABASE)

if "sqlite" in SQL_ALCHEMY_DATABASE:
    engine = create_engine(SQL_ALCHEMY_DATABASE, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQL_ALCHEMY_DATABASE)

session_local = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapi', 
#                                 user='postgres', password='sarcasm1@123', 
#                                 cursor_factory=RealDictCursor, port=5433)  
#         cursor = conn.cursor()
#         print("Successfully connected!")
#         break
#     except Exception as error:
#         print(f"Connection Failed:", error)
#         time.sleep(3)