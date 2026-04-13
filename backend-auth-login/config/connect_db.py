from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String

DATABASE_URL = "postgresql://admin:1234@postgres:5432/auth"  # URL to connect to the postgres DB

engine = create_engine(DATABASE_URL) # Create a pool of connexions ready to use

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # session rules manager for connexion with DB (add, commit, ...) and its behavior

class Base(DeclarativeBase):
    pass

class UserDB(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

