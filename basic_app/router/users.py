from .. import models
from ..database import engine, app_Session, get_db
from .. import database  
from sqlalchemy.orm import Session
from ..schemas import Post, UserCreate, UserOut
from ..utils import hash_text
from ..oauth2 import create_access_token

from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

rourter = APIRouter(prefix="/users", tags=["users"])

@rourter.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    #hash the password before saving it to DB    
    user.password = hash_text(user.password)
    print("entering here", user.password)
    new_user = models.Users(**user.model_dump())   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@rourter.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def find_user(id:int, db:Session = Depends(get_db)):
    existing_user=db.query(models.Users).filter(models.Users.id == id).first()
    if existing_user == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")  
    
    return existing_user