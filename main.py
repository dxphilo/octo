from fastapi import FastAPI, status
from pydantic import BaseModel;
from typing import Optional
from database import SessionLocal
import models
from datetime import datetime

app=FastAPI()

class User(BaseModel): #serializer
    fullname: str
    email: str
    password: str

    class Config:
        orm_mode=True

class ResUser(BaseModel): #serializer
    id:int
    fullname: str
    email: str
    password: str
    date:str
    time:str

    class Config:
        orm_mode=True

class Login(BaseModel): #serializer
    email: str
    password: str

    class Config:
        orm_mode=True

class Entry(BaseModel): #serializer
    text: str
    number_of_calories: int

    class Config:
        orm_mode=True

class   ResEntry(BaseModel): #serializer
    id:int
    text: str
    number_of_calories: int
    date:str
    time:str

    class Config:
        orm_mode=True

db=SessionLocal()

@app.get('/')
def greet():
    return {"Message": "Server is up and running"}


@app.get('/users/',response_model=list[ResUser],status_code=200)
async def login_a_user():
    users = db.query(models.User).all()
    return users

@app.post('/signup/',response_model=User, status_code=status.HTTP_201_CREATED)
async def create_a_user(user: User):
    new_user = models.User(
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



@app.post('/user/entries/',response_model=Entry, status_code=status.HTTP_201_CREATED)
async def save_entries(entry: Entry):

    new_entry = models.Entry(
        text= entry.text,
        number_of_calories=entry.number_of_calories,
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M:%S"),
    )

    db.add(new_entry)
    db.commit()

    return new_entry

@app.get('/user/entries/')
async def get_entries():
    all_entries = db.query(models.Entry).all()
    return all_entries

@app.put('/user/entries/{user_id}')
async def update_entries(user_id: int, user: User):
    return {"user_email":f"Hello {user_id}, {user}"}


@app.delete('/user/entries/{user_id}')
async def delete_an_entry(user_id: int):
    return {"user_email":f"Hello {user_id}"}