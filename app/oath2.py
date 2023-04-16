from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings



oath2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

#SECRET KEY
#ALGORITHM
#THE EXPIRATION TIME 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token (token:str, credentials_exceptions):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id: str = payload.get('user_id')

        print(f'id {id}')
        if id is None: 
            raise credentials_exceptions
    
        token_data = schemas.TokenData(user_id = id)

        print(f'token_data {token_data}')

    except JWTError:
        raise credentials_exceptions
    
    return token_data
    
def get_current_user (token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credentials_exceptions = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 
                                          f"Could not validate credentials", headers = {"WWW - Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exceptions)
    print(f'token {token}')
    user = db.query(models.User).filter(models.User.id == token.user_id).first()
    print(f'user {user}')
    return user






