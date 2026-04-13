from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
# import connect_db
from contextlib import asynccontextmanager
from connect_db import engine, Base, UserDB, SessionLocal  # our own py file



class UserFront(BaseModel):
    email: EmailStr
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



auth = FastAPI(lifespan=lifespan)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

def get_db():
    db = SessionLocal()       # ouvre le panier
    try:
        yield db              # donne le panier à la route
    finally:
        db.close()

@auth.post("/api/auth-register")
def register(data : UserFront, db: Session = Depends(get_db)):
    try :

        new_user = UserDB(email=data.email, password=data.password)

        id = db.add(new_user)

        db.commit()

        db.refresh(new_user)

        print(data.email, data.password)
        return {"message": f"connexion reussie, Bienvenue {new_user.email}, your password is {new_user.password} and your id {new_user.id}", "ValidEmail": True, "ValidPassword": True}
    except :
        db.rollback()
        return {"message": f"connexion echoue avec id = {id}"}


@auth.post("/api/auth-login")
def login(data : UserFront, db: Session = Depends(get_db)):
    try :
        user = db.query(UserDB).filter(UserDB.email == data.email).first()
        if user.password != data.password :
            raise Exception("Email ou mot de passe incorrect")
        return {"message": f"USER FOUND, Bienvenue {user.email}, your password is {user.password} and your id {user.id}", "ValidEmail": True, "ValidPassword": True}
    except :
        return {"message": f"ALMOST HAHA"}        