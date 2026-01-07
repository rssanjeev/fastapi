import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE='postgresql://postgres:sarcasm1%40123@localhost:5433/fastapi'

engine = create_engine(SQL_ALCHEMY_DATABASE)

session_local = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()



#dependency
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