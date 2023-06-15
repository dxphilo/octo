import time
import jwt
from config.config import settings
from schema.schema import SignUser

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
expiration_time = time.time() + (16 * 60 * 60)  # 16 hours (60 minutes * 60 seconds) 


def sign_jwt(user: SignUser):
    payload = {
        "user_id":user.fullname,
        "user_email": user.email,
        "role":user.role,
        "expires": expiration_time
    }

    token = jwt.encode(payload, JWT_SECRET,JWT_ALGORITHM)
    return token_responce(token=token)

def decode_jwt(token:str):
    try:
        decoded_token = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        print(decoded_token);
        return decoded_token if decoded_token['expires'] >= time.time() else {}
    except:
        return {}
    
def token_responce(token:str):
    return {
        "access_token": token
    }