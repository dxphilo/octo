from argon2 import PasswordHasher
#chose argon2 for improvied resitance against various password attacks as opposed to bcrypt

ph = PasswordHasher()

async def hash_password(password: str):

    hashed_password = ph.hash(password)
    print(hashed_password)
    return hashed_password

async def verify_hashed_password(password:str,hashed_password: str):

    is_password_valid = ph.verify(hashed_password, password)
    print(is_password_valid)
    return is_password_valid