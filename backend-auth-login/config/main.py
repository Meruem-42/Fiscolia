# Librairies
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException

# Local Files
from connect_db import UserDB, Depends, get_db, auth
from security import verify_password, hash_password, check_password


class UserFront(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str

@auth.post("/api/auth-register")
def register(data: UserFront, db: Session = Depends(get_db)):
    try:
        error = check_password(data.password)
        if error:
            return {"status": "error", "message": error}
        hashed_pwd = hash_password(data.password)

        new_user = UserDB(email=data.email, password=hashed_pwd, firstname=data.firstname ,lastname=data.lastname)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"status": "valid", "message": f"Un email de confirmation a été envoyé a {data.email}"}
    except Exception as e:
        db.rollback()
        print(f"Error: {e}", flush=True) 
        # ICI : On renvoie une VRAIE erreur au navigateur
        raise HTTPException(status_code=400, detail=str(e))

@auth.post("/api/auth-login")
def login(data: UserFront, db: Session = Depends(get_db)):
    try:
        user = db.query(UserDB).filter(UserDB.email == data.email).first()
        if not verify_password(data.password, user.password):
            raise Exception("Email ou mot de passe incorrect")
        return {"message": f"Bienvenue {user.email}"}
    except:
        return {"message": "Email or password incorrect"}


# backend-auth/
# ├── app/
# │   ├── main.py            # Point d'entrée (FastAPI)
# │   ├── database.py        # Anciennement connect_db.py
# │   ├── schemas.py         # Modèles Pydantic (UserFront)
# │   ├── routes/
# │   │   └── auth.py        # Routes register et login
# │   └── services/
# │       ├── security.py    # Hash, verify, validation password
# │       └── auth_logic.py  # Logique métier (vérification doublons, etc.)
# └── Dockerfile