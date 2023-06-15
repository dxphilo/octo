from fastapi import status,HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import User, Entry
from schema.schema import  ResEntry, NewEntry, NewUser, ResUser, Login
from datetime import datetime
from typing import List
from config.config import settings
import httpx
from auth.auth import sign_jwt,decode_jwt

db=SessionLocal()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.get('/')
def health_check():
    return {"Message": "Server is up and running"}



@router.get('/users/', response_model=List[ResUser], status_code=200)
async def login_a_user():
    users = db.query(User).all()
    return users


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



@router.post('/user/entries/',response_model=ResEntry,status_code=status.HTTP_201_CREATED)
async def save_entries(entry: NewEntry,token:str = Depends(oauth2_scheme)):
    try:
        user_from_token = decode_jwt(token);

        if not user_from_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

        headers = {
        "Content-Type": "application/json",
        "x-app-id": settings.NUTRITIONIX_API_ID,
        "x-app-key": settings.NUTRITIONIX_API_KEY
        }
        url = settings.NUTRITIONIX_URL
        expected_calories_per_day = settings.EXPECTED_CALORIES_PER_DAY

        if entry.number_of_calories is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(url,headers=headers)
                data = response.json()
                foods = data.get("foods",[])
                if foods:
                    entry.number_of_calories =foods[0].get("nf_calories",0)
                print(response)


        new_entry = Entry(
            text= entry.text,
            number_of_calories=entry.number_of_calories,
            date=datetime.now().strftime("%Y-%m-%d"),
            time=datetime.now().strftime("%H:%M:%S"),
            is_under_calories=False
        )
        # Check the threshhold for the total nunber of calories for the day and set is_under_calories appropriately
        if entry.number_of_calories is not None and int(entry.number_of_calories) < int(expected_calories_per_day):
            new_entry.is_under_calories = True

        db.add(new_entry)
        db.commit()

        return new_entry
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/user/entries/',response_model=List[ResEntry],status_code=status.HTTP_200_OK)
async def get_entries():
    all_entries = db.query(Entry).all()
    return all_entries

@router.put('/user/entries/{entry_id}/',response_model=ResEntry,status_code=status.HTTP_200_OK)
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


@router.delete('/user/entries/{entry_id}/', response_model=ResEntry,status_code=status.HTTP_200_OK)
async def delete_an_entry(entry_id: int):
    entry_to_delete = db.query(Entry).filter(Entry.id == entry_id).first()
    # TODO: authenticate user deletion

    if entry_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Entry with the given id {entry_id} is not found")
    
    db.delete(entry_to_delete)
    db.commit()
    return entry_to_delete
