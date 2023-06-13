from sqlalchemy import String,Boolean,Integer,Column,Text
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    fullname=Column(String(255),nullable=False)
    email=Column(Text,nullable=False,unique=True)
    password=Column(String(255),nullable=False)
    date=Column(String(255),nullable=False)
    time=Column(String(244),nullable=False)

class Entry(Base):
    __tablename__='entries'
    id=Column(Integer,primary_key=True)
    text=Column(String(255),nullable=False)
    number_of_calories=Column(Text,nullable=False)
    date=Column(String(255),nullable=False)
    time=Column(String(244),nullable=False)


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
    number_of_calories: int

    class Config:
        orm_mode = True

class ResEntry(BaseModel):
    id: int
    date:str
    number_of_calories: str
    text: str
    time:str

    class Config:
        orm_mode = True

