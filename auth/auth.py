import time
import jwt
from dataclasses import dataclass
from config.config import settings
from schema.schema import Role

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
expiration_time = time.time() + (16 * 60 * 60)  # 16 hours (60 minutes * 60 seconds)

@dataclass
class User:
    fullname: str
    email: str
    role: Role


def token_responce(token:str):
    return {
        "access_token": token
    }

def sign_jwt(user: User):
    payload = {
        "user_id":user.fullname,
        "user_email": user.email,
        "role":user.role,
        "expires": expiration_time
    }

    token = jwt.encode(payload=payload, JWT_SECRET=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_responce(token=token)

def decode_jwt(token:str) -> dict:
    try:
        decoded_token = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}