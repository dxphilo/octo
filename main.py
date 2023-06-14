from fastapi import FastAPI, status,HTTPException
from database.database import SessionLocal
from models.models import User, ResUser, Login,Entry, ResEntry, NewEntry, NewUser
from datetime import datetime
from typing import List
from functools import lru_cache
from . import config;
import httpx

app=FastAPI()

db=SessionLocal()


@lru_cache()
def get_settings():
    return config.Settings()

settings = get_settings()

@app.get('/')
def health_check():
    return {"Message": "Server is up and running"}

@app.get('/users/', response_model=List[ResUser], status_code=200)
async def login_a_user():
    users = db.query(User).all()
    return users


@app.post('/signup/',response_model=ResUser, status_code=status.HTTP_201_CREATED)
async def create_a_user(user: NewUser):
    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password=user.password,
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M:%S"),
    )

    db_item=db.query(User).filter(user.email == new_user.email).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="User with the email already exists")
    
    db.add(new_user)
    db.commit()

    return new_user


@app.post('/login/')
async def login_a_user(login: Login):
    return login



@app.post('/user/entries/',response_model=ResEntry,status_code=status.HTTP_201_CREATED)
async def save_entries(entry: NewEntry):

    number_of_calories: int=0;

    headers = {
    "Content-Type": "application/json",
    "x-app-id": settings.NUTRITIONIX_API_ID,
    "x-app-key": settings.NUTRITIONIX_API_KEY
    }
    url = settings.NUTRITIONIX_URL

    if entry.number_of_calories is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url,headers=headers)
            print(response);


    new_entry = Entry(
        text= entry.text,
        number_of_calories=entry.number_of_calories,
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M:%S"),
    )

    db.add(new_entry)
    db.commit()

    return new_entry

@app.get('/user/entries/',response_model=List[ResEntry],status_code=status.HTTP_200_OK)
async def get_entries():
    all_entries = db.query(Entry).all()
    return all_entries

@app.put('/user/entries/{entry_id}/',response_model=ResEntry,status_code=status.HTTP_200_OK)
async def update_entries(entry_id: int, entry: ResEntry):

    entry_to_update = db.query(Entry).filter(Entry.id == entry_id).first()

    if entry_to_update is None:
        raise HTTPException(status_code=400, detail=f"Entry with the id {entry_id} is not found")

    entry_to_update.text = entry.text
    entry_to_update.number_of_calories = entry.number_of_calories
    entry_to_update.date = datetime.now().strftime("%Y-%m-%d")
    entry_to_update.time = datetime.now().strftime("%H:%M:%S")

    db.commit()

    return entry_to_update


@app.delete('/user/entries/{entry_id}/', response_model=ResEntry,status_code=status.HTTP_200_OK)
async def delete_an_entry(entry_id: int):
    entry_to_delete = db.query(Entry).filter(Entry.id == entry_id).first()
    # TODO: authenticate user deletion

    if entry_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Entry with the given id {entry_id} is not found")
    
    db.delete(entry_to_delete)
    db.commit()
    return entry_to_delete
