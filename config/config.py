from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(".env")

class Settings(BaseSettings):
    app_name: str = "octo API"
    NUTRITIONIX_API_ID: str
    NUTRITIONIX_API_KEY: str
    NUTRITIONIX_URL: str
    EXPECTED_CALORIES_PER_DAY: str
    
    class Config:
        env_file = ".env"