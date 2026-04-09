from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
import connect_db
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class UserFront(BaseModel):
    email: EmailStr
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"test -> {connect_db.DATABASE_URL}", flush=True)
    yield

DATABASE_URL = "postgresql://admin:1234@postgres:5432/auth"  # URL to connect to the postgres DB

engine = create_engine(DATABASE_URL) # Create a pool of connexions ready to use

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine) # session rules manager for connexion with DB (add, commit, ...) and its behavior

Base = declarative_base()

Base.metadata.create_all(bind=engine)    

class UserDB(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)    

auth = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()       # ouvre le panier
    try:
        yield db              # donne le panier à la route
    finally:
        db.close()

@auth.post("/api/auth-login")
def read_root(data : UserFront, db: Session = Depends(get_db)):
    try :

        new_user = UserDB(email=data.email, password=data.password)

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        print(data.email, data.password)
        return {"message": f"connexion reussie, Bienvenue {new_user.email}, your password is {new_user.password} and your id {new_user.id}", "ValidEmail": True, "ValidPassword": True}
    except :
        db.rollback()
        return {"message": "connexion echoue"}




# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}



