from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models, utils, database, oath2

router = APIRouter( tags = ['Authentification'])

@router.post("/login", response_model = schemas.Token)
def UserLogin (user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user: 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code =  status.HTTP_403_FORBIDDEN, detail= f"Invalid credentials")
    
    access_token = oath2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}


