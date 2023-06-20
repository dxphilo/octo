from fastapi import status, HTTPException, APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import Entry
from schema.schema import ResEntry, NewEntry, Role
from datetime import datetime
from typing import List
from config.config import settings
from sqlalchemy.exc import SQLAlchemyError
from auth.auth import decode_jwt
from utils.helpers import get_calories_from_api

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Utility function to get user from token
async def get_user_from_token(token: str):
    user_from_token = decode_jwt(token)
    if not user_from_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user_from_token


# Endpoint for saving entries
@router.post('/user/entries/', response_model=ResEntry, status_code=status.HTTP_201_CREATED)
async def save_entries(entry: NewEntry, token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        user = user_from_token['user_id']

        if entry.number_of_calories is None:
            calories = await get_calories_from_api()
            entry.number_of_calories = calories

        new_entry = Entry(
            text=entry.text,
            number_of_calories=entry.number_of_calories,
            user=user,
            date=datetime.now().strftime("%Y-%m-%d"),
            time=datetime.now().strftime("%H:%M:%S"),
            is_under_calories=False
        )

        if entry.number_of_calories is not None and int(entry.number_of_calories) < int(settings.EXPECTED_CALORIES_PER_DAY):
            new_entry.is_under_calories = True

        db.add(new_entry)
        db.commit()

        return new_entry
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Entry was not saved to the database")



# Endpoint for retrieving entries
@router.get('/user/entries/', response_model=List[ResEntry], status_code=status.HTTP_200_OK)
async def get_entries(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        offset = (page - 1) * per_page

        if role == Role.USER:
            all_entries = db.query(Entry).filter(Entry.role == Role.USER.value).offset(offset).limit(per_page).all()
        elif role == Role.ADMIN:
            all_entries = db.query(Entry).offset(offset).limit(per_page).all()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with the role specified was not found")

        return all_entries
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error querying the database")



# Endpoint for updating an entry
@router.put('/user/entries/{entry_id}/', response_model=ResEntry, status_code=status.HTTP_200_OK)
async def update_entries(entry_id: int, entry: ResEntry, token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        entry_to_update = db.query(Entry).filter(Entry.id == entry_id).first()

        if entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"Entry with the id {entry_id} was not found")

        if role == Role.USER or role == Role.ADMIN:
            entry_to_update.text = entry.text
            entry_to_update.number_of_calories = entry.number_of_calories
            entry_to_update.date = datetime.now().strftime("%Y-%m-%d")
            entry_to_update.time = datetime.now().strftime("%H:%M:%S")

        db.commit()
        return entry_to_update
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Endpoint for deleting an entry
@router.delete('/user/entries/{entry_id}/', response_model=ResEntry, status_code=status.HTTP_200_OK)
async def delete_an_entry(entry_id: int, token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user =user_from_token['user_id']
        entry_to_delete = db.query(Entry).filter(Entry.id == entry_id).first()

        if entry_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entry with the given id {entry_id} is not found")

        if role == Role.USER and user == entry_to_delete.user or role == Role.ADMIN:
            db.delete(entry_to_delete)
            db.commit()

        return entry_to_delete
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Export the router
entry_routes = router