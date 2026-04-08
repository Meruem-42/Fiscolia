from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

auth = FastAPI()

class LoginData(BaseModel):
    email: EmailStr
    password: str

@auth.post("/api/auth-login")
def read_root(data : LoginData):
    print(data.email, data.password)
    return {"message": f"connexion reussie, Bienvenue {data.email}", "ValidEmail": True, "ValidPassword": True}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

