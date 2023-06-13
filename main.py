from fastapi import FastAPI, status
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

@app.put('/user/entries/{user_id}')
async def update_entries(user_id: int, user: NewUser):
    return {"user_email":f"Hello {user_id}, {user}"}


@app.delete('/user/entries/{user_id}')
async def delete_an_entry(user_id: int):
    return {"user_email":f"Hello {user_id}"}