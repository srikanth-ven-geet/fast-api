import json
from basic_app.utils import generate_jwt, decode_jwt
from fastapi import Depends, HTTPException, status
from jose import JWTError
import hmac, hashlib, base64
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .database import engine, app_Session, get_db
from . import database , models 
from sqlalchemy.orm import Session
 
from datetime import datetime, timedelta
import datetime

SECRET_KEY="WelcomeWelcome1234"
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
outh2_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict) -> str:
    data_copy: dict = data.copy()
    expire = json.dumps(datetime.datetime.now(datetime.timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                        default=serialize_datetime)
    data_copy.update({"exp":expire})    
    #encoded_token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)    
    encoded_signature = generate_jwt(data_copy, SECRET_KEY)
    return encoded_signature

def verify_access_token(token: str, credentials_exception):
    try:
        payload: dict = decode_jwt(token, SECRET_KEY)        
        if payload["payload"]["user_email"] == None:
            raise credentials_exception
        token_data = schemas.TokenData(id = payload["payload"]["user_email"])
    except JWTError:
        raise credentials_exception
    return token_data
        
#use this method as a dependency for any of the end point that needs authentiation.
#if the token is valid, the flow will continue. If not, this method will throw exception and the 
#flow will terminate
def get_current_user(token: str = Depends(outh2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail = f"the credentials were invalid",
                                          headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    print("<---------- The user email is ---------->",token_data.id)
    curr_user = db.query(models.Users).filter(models.Users.email == token_data.id).first()
    samp: dict = {"email":curr_user.email, "id":curr_user.id, "created_at":curr_user.created_at}
    print("<---------sending the current user ------>",samp)
    return curr_user


def serialize_datetime(obj):     
    if isinstance(obj, datetime.date): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 