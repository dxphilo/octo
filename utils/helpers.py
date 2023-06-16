import httpx
from fastapi import HTTPException, status
from config.config import settings
from argon2 import PasswordHasher
import argon2.exceptions
#chose argon2 for improved resitance against attacks

ph = PasswordHasher()

async def hash_password(password: str):

    hashed_password = ph.hash(password)
    print(hashed_password)
    return hashed_password

async def verify_hashed_password(password:str,hashed_password: str):
    try:
        is_password_valid = ph.verify(hashed_password, password)
        print(is_password_valid)
        return is_password_valid
    except argon2.exceptions.VerifyMismatchError:
        return False
    



async def get_calories_from_api():
    try:
        headers = {
            "Content-Type": "application/json",
            "x-app-id": settings.NUTRITIONIX_API_ID,
            "x-app-key": settings.NUTRITIONIX_API_KEY
        }
        url = settings.NUTRITIONIX_URL

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            data = response.json()
            foods = data.get("foods", [])
            if foods:
                return foods[0].get("nf_calories", 0)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve calories")
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
