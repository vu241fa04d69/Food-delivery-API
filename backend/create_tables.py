from database.db_connection import engine, Base
from database import db_models

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")