from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users", 
    tags = ["users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.CreateUserResponse)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash password = user.password 
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password

    created_user = models.User(**new_user.dict())
    #ADDING NEW POST TO THE DB 
    db.add(created_user)
    #COMMITTING NEW POST 
    db.commit()
    #SHOWING NEW POST TO THE USER AFTER CREATION 
    db.refresh(created_user)

    return created_user

@router.get("/{id}", response_model = schemas.CreateUserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "The user with id: {id} does not exist")
    
    return user
