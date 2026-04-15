from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String
import os

# TODO: MOVE IN utils.py

def get_secret(secret_name):
    try:
        path = f"/run/secrets/{secret_name}"
        
        with open(path, "r") as secret_file:
            return secret_file.read().strip()
            
    except FileNotFoundError:
        print(f"Error : {secret_name} file does not exist.")
        return None

db_user = os.getenv("DB_AUTH_USER")
db_port = os.getenv("DB_AUTH_PORT")
db_name = os.getenv("DB_AUTH_NAME")
db_password = get_secret(os.getenv("DB_AUTH_SECRETS"))

DATABASE_URL = f"postgresql://{db_user}:{db_password}@db-auth:{db_port}/{db_name}"  # URL to connect to the postgres DB

engine = create_engine(DATABASE_URL) # Create a pool of connexions ready to use

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # session rules manager for connexion with DB (add, commit, ...) and its behavior

class Base(DeclarativeBase):
    pass

class UserDB(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

