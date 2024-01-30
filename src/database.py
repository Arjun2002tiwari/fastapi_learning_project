from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse as up

Base = declarative_base()

# Replace the connection string with your MySQL connection details
DATABASE_URL = f"mysql+mysqlconnector://root:{str(up.quote('Arjun2002'))}@localhost/zenarate_db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
