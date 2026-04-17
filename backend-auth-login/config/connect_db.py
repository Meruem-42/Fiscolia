# Standart
import os
from contextlib import asynccontextmanager

#Libraries
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String
from fastapi import FastAPI, Depends

# Local files
from security import get_secret


db_user = os.getenv("DB_AUTH_USER")
db_port = os.getenv("DB_AUTH_PORT")
db_name = os.getenv("DB_AUTH_NAME")
db_password = get_secret(os.getenv("DB_AUTH_SECRETS"))

DATABASE_URL = f"postgresql://{db_user}:{db_password}@db-auth:{db_port}/{db_name}"  # URL to connect to the postgres DB

engine = create_engine(DATABASE_URL)  # Create a pool of connexions ready to use

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # session rules manager for connexion with DB (add, commit, ...) and its behavior


class Base(DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


auth = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()  # ouvre le panier
    try:
        yield db  # donne le panier à la route
    finally:
        db.close()