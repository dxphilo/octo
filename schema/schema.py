from pydantic import BaseModel
from typing import Optional


class NewUser(BaseModel):
    fullname: str
    email: str
    password: str

    class Config:
        orm_mode = True

class ResUser(BaseModel):
    id: int
    fullname: str
    email: str
    password: str
    date: str
    time: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class NewEntry(BaseModel):
    text: str
    number_of_calories: Optional[int]

    class Config:
        orm_mode = True

class ResEntry(BaseModel):
    id: int
    date:str
    number_of_calories: str
    text: str
    time:str
    is_under_calories: bool 

    class Config:
        orm_mode = True

