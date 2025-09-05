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