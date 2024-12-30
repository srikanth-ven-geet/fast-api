from ..database import engine, app_Session, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Body
from pydantic import BaseModel
from .. import database, schemas, models, oauth2

router = APIRouter(prefix="/vote", tags=['vote'])

#A post can be voted by a user only once. IF a post is already voted by a user it can be unvoted.
@router.post("/", status_code=status.HTTP_201_CREATED)
def record_vote(vote: schemas.Vote, db: Session=Depends(get_db),
                 curr_user: schemas.UserOut= Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Post doesnt exists")
    
    vote_query = db.query(models.Vote).filter(vote.post_id == models.Vote.post_id, 
                                              curr_user.id == models.Vote.user_id)
    found_vote = vote_query.first()
    if(vote.vote_dir == 1): # to add a new vote 
        if(found_vote):
            raise HTTPException(status=status.HTTP_409_CONFLICT,
                                detail=f"User {curr_user.email} has already voted")
        new_vote = models.Vote(post_id = vote.post_id, user_id = curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Voted successfully"}
    else:                   # to delete an existing vote
        if found_vote == None:
            raise HTTPException(status = status.HTTP_404_NOT_FOUND,
                                detail="Vote doesnt exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfuly deleted the vote"}


