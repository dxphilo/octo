from fastapi import status,HTTPException, APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import User
from schema.schema import  NewUser, ResUser, Login, Role, DeletionSuccess
from datetime import datetime
from auth.auth import sign_jwt
from typing import List
from .entry import get_user_from_token

db=SessionLocal()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


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


@router.get('/users/',response_model=List[ResUser] ,status_code=200)
async def get_users(token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']

        if role == Role.ADMIN:
            user_entries = db.query(User).all()
        elif role == Role.MANAGER:
            user_entries = db.query(User).filter(User.role == Role.USER).all()
        elif role == Role.USER:
            user_entries = db.query(User).filter(User.email == user_email).first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        return user_entries
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/users/{user_id}/', response_model=ResUser, status_code=200)
async def update_user_details(
    user_id:int,
    new_entry:NewUser,
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']

        user_entry_to_update = db.query(User).filter(User.id == user_id).first()

        if user_entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"User with the id {user_id} was not found")
        
        if (
            role == Role.ADMIN 
            or (role == Role.MANAGER and user_entry_to_update.role == Role.USER)
            or (role == Role.USER and user_entry_to_update.email == user_email)
        ):
            user_entry_to_update.fullname = new_entry.fullname
            user_entry_to_update.email = new_entry.email
            user_entry_to_update.password = new_entry.password
            user_entry_to_update.date = datetime.now().strftime("%Y-%m-%d")
            user_entry_to_update.time=datetime.now().strftime("%H:%M:%S")
            user_entry_to_update.role = new_entry.role

            db.commit()

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        return user_entry_to_update
    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/users/{user_id}/', response_model=DeletionSuccess, status_code=200)
async def delete_user_detail(
    user_id:int,
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']

        user_entry_to_delete = db.query(User).filter(User.id == user_id).first()

        if user_entry_to_delete is None:
            raise HTTPException(status_code=400, detail=f"User with the id {user_id} was not found")
        
        if (
            role == Role.ADMIN 
            or (role == Role.MANAGER and user_entry_to_delete.role == Role.USER)
            or (role == Role.USER and user_entry_to_delete.email == user_email)
        ):
            db.delete(user_entry_to_delete)
            db.commit()

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        return  DeletionSuccess()
    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User deletion was not successfull")


user_routes=router