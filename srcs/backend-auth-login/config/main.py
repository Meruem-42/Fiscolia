# Librairies
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Response, Cookie
from datetime import datetime, timedelta

# Local Files
from connect_db import UserDB, get_db, auth, UserDataDB, SessionDB
from security import verify_password, hash_password, check_password
from session_store import create_session, get_session, delete_session

from predict import predict_profile, extract_profiles_info


class UserData(BaseModel):
    etat_civil: str
    quotient_familial: str
    situation_specifique: str
    rni: str
    csp: str



class UserRegister(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@auth.post("/api/auth-register")
def register(data: UserRegister, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=400, detail="HTTP error occured")


def get_current_user(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session invalid or expired")
    user = db.query(UserDB).filter(UserDB.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@auth.post("/api/auth-login")
def login(data: UserLogin, response: Response, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    user = db.query(UserDB).filter(UserDB.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Email or password incorrect")
    # create session (7 days)
    
	# on veut verifier si l'user possede deja une session 
    existing_session = None # par defaut
    if session_id:
        existing_session = db.query(SessionDB).filter(SessionDB.id == session_id).first()
    if existing_session and existing_session.user_id == user.id:
        # Le cookie correspond au bon user
        print(f"User {user.email} already has a valid session.")
        response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax", max_age=7 * 24 * 3600)
    else:
        # Soit pas de cookie, soit le cookie appartenait a un AUTRE user (ou session expirée)
        # On doit creer une nouvelle session propre pour cet user
        session_id = create_session(db, user.id, data={"email": user.email}, ttl_seconds=7 * 24 * 3600)
        response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax", max_age=7 * 24 * 3600)
        
    return {
        "message": f"Bienvenue {user.email}",
        # "profile_complete": True,
        # "profiles_infos": profiles_info,
    }


@auth.post("/api/auth-logout")
def logout(response: Response, session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if session_id:
        delete_session(db, session_id)
    response.delete_cookie("session_id")
    return {"message": "Logged out"}


@auth.get("/api/me")
def get_me(current_user: UserDB = Depends(get_current_user), response: Response = None):
    """Get current authenticated user info"""
    # Disable cache for this endpoint
    if response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return {
        "id": current_user.id,
        "email": current_user.email,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
    }


def get_current_user_optional(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if not session_id:
        return None
    session = get_session(db, session_id)
    if not session:
        return None
    user = db.query(UserDB).filter(UserDB.id == session.user_id).first()
    return user

@auth.post("/api/edit-profile")
def edit_profile(data: UserData, current_user: Optional[UserDB] = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    user_data = {
        "etat_civil": data.etat_civil,
        "quotient_familial": data.quotient_familial,
        "situation_specifique": data.situation_specifique,
        "rni": data.rni,
        "csp": data.csp,
	}
    profile_info = predict_profile(user_data)
    new_data = UserDataDB(
        etat_civil=data.etat_civil,
        quotient_familial=data.quotient_familial,
        situation_specifique=data.situation_specifique,
        rni=data.rni,
        csp=data.csp,
        user_id=current_user.id if current_user else None,
        profile = profile_info
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"message": "Thank you, your data has been used for ML"}

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