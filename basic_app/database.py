from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from .config import settings

#since @ in password is spl character use the urllib.parse 
#to get the values from env, use : settings.database_hostname, etc
engine = create_engine('postgresql://postgres:%s@localhost:5432/fastapi'%quote("Geetha@1955"))
app_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db=app_Session()
    try:
        yield db
    finally:
        db.close()