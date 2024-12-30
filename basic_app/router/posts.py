from sqlalchemy import func
from .. import models
from ..database import engine, app_Session, get_db
from .. import database, schemas
from sqlalchemy.orm import Session
from ..schemas import Post, UserCreate, UserOut, PostOut
from ..utils import hash_text
from .. import oauth2


from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

rourter = APIRouter(tags=["Posts"])

@rourter.get("/posts", response_model=List[PostOut])
def test_app(db: Session=Depends(get_db), limit:int =10, page:int = 1):    
    posts = db.query(models.Post).offset((page-1)*limit).limit(limit).all()
    #the below uses left join and group by. default join is left inner join
    #query to get the votes for all posts
    #                  Posts table   get the count of votes along with other columns     join with vote table   on post_id and vote id                      group by Post id count    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return results

@rourter.post("/posts",status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post:Post, db: Session=Depends(get_db), 
                curr_user: UserOut= Depends(oauth2.get_current_user)):
    #new_post = models.Post(title=post.title, content=post.content)  
    print(f"<--------Entering the create post ------->")    
    new_post = models.Post(owner_id = curr_user.id, **post.model_dump())    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@rourter.get("/post/{id}", response_model=PostOut)
def get_post(id: int, db: Session=Depends(get_db)):
    #post=db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    if not post:       
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {id} not found")
    return post

@rourter.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session=Depends(get_db), 
                curr_user: UserOut= Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == id)
    #delete the post only if the user token details match with the id of the user who created it
    if(curr_user.id == post.first().owner_id):
        if not post.first():       
         raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {id} not found")
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"You are not authorized to delete this post")


@rourter.put("/post/{id}")
def update_post(id:int, post:Post, db: Session=Depends(get_db), 
                curr_user: UserOut= Depends(oauth2.get_current_user)):
    existing_post=db.query(models.Post).filter(models.Post.id == id)
    new_post = existing_post.first()
    if  new_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {id} not found")    
    if (new_post.owner_id == curr_user.id):
        existing_post.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return {"data":'record updated'}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Not authorized to delete this post")    