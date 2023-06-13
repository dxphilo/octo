from database.database import Base,engine
from models.models import User,Entry

print("Creating database ....")

Base.metadata.create_all(engine);