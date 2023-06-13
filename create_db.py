from database import Base,engine
from models import User,Entry

print("Creating database ....")

Base.metadata.create_all(engine);