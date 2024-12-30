from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, utils, schemas, database, oauth2


router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
#@router.post("/login", )
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db),):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(database.get_db),):
    #the OAuth2PAsswordRequestForm will convert the data in dictionary format containing 
    #username and password fields
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    #print(user)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email doesnt exists")
    if not utils.verify_password(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed")
    access_token = oauth2.create_access_token(data = {"user_email":user_credentials.username})
    return {"token":access_token, "type":"bearer"}

    #remember, the request will be sent in form data format and not as JSON with Oauth2PAsswordRe...

    