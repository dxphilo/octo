from argon2 import PasswordHasher
from utils.helpers import hash_password, verify_hashed_password
import pytest

ph = PasswordHasher()

@pytest.mark.asyncio
async def test_hash_password():
    password = "password123"
    hashed_password = await hash_password(password)
    assert hashed_password is not None
    assert len(hashed_password) > 0

@pytest.mark.asyncio
async def test_verify_hashed_password():
    password = "password123"
    hashed_password = ph.hash(password)
    is_valid = await verify_hashed_password(password, hashed_password)
    assert is_valid is True

    incorrect_password = "incorrect"
    is_valid = await verify_hashed_password(incorrect_password, hashed_password)
    assert is_valid is False
