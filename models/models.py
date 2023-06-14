from sqlalchemy import String,Boolean,Integer,Column,Text
from database.database import Base

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
    is_under_calories=Column(Boolean,nullable=False)
