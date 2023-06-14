from fastapi import FastAPI, status,HTTPException
from database.database import SessionLocal
from models.models import User, ResUser, Login,Entry, ResEntry, NewEntry, NewUser
from datetime import datetime


app=FastAPI()

db=SessionLocal()

@app.get('/')
def greet():
    return {"Message": "Server is up and running"}


from typing import List

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
    # TODO: ensure return approaprita error message when email is not unique;

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


@app.delete('/user/entries/{entry_id}')
async def delete_an_entry(entry_id: int):
    return {"user_email":f"Hello {entry_id}"}