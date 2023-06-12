from fastapi import FastAPI;
from pydantic import BaseModel;

app=FastAPI()

class User(BaseModel): #serializer
    full_name: str
    email: str
    password: str

class Login(BaseModel): #serializer
    email: str
    password: str

class Calories(BaseModel): #serializer
    meal: str
    calories: int
    text: str

@app.get('/')
def greet():
    return {"Message": "Server is up and running"}


@app.post('/signup/')
async def sign_up(user: User):
    return user


@app.post('/login/')
async def log_in(login: Login):
    return login



@app.post('/calories/')
async def save_calories(login: Login):
    return login

@app.get('/user/meals/')
async def get_calories(login: Login):
    return login

@app.put('/user/meals/{user_id}')
async def update_calories(user_id: int, user: User):
    return {"user_email":f"Hello {user_id}, {user}"}


@app.delete('/user/meals/{user_id}')
async def update_calories(user_id: int):
    return {"user_email":f"Hello {user_id}"}