from fastapi import status,HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import User
from schema.schema import  NewUser, ResUser, Login
from datetime import datetime
from typing import List
from auth.auth import sign_jwt

db=SessionLocal()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get('/users/', response_model=List[ResUser], status_code=200)
async def login_a_user():
    users = db.query(User).all()
    return users


@router.post('/signup/',response_model=ResUser, status_code=status.HTTP_201_CREATED)
async def create_a_user(user: NewUser):
    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password=user.password,
        role=user.role,
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M:%S"),
    )

    db_item=db.query(User).filter(User.email == new_user.email).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="User with the email already exists")
    
    db.add(new_user)
    db.commit()

    return new_user


@router.post('/login/')
async def login_a_user(login: Login):
    db_user = db.query(User).filter(User.email == login.email).first() 

    if db_user is not None:
        if db_user.password != login.password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You have entered a wrong password")
        token = sign_jwt(db_user)
        return token
    
    return { "msg": "User not found in the database"}

user_routes=router