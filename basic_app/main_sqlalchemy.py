from . import models
from .database import engine, app_Session
from . import database  
from sqlalchemy.orm import Session
from .schemas import Post, UserCreate, UserOut
from .utils import hash_text

from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .router import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# the below line is not required if alembic is used to manage DB table creation
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db=app_Session()
    try:
        yield db
    finally:
        db.close()
    
app.include_router(posts.rourter)
app.include_router(users.rourter)
app.include_router(auth.router)
app.include_router(vote.router)