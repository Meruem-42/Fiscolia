from fastapi import FastAPI
from pydantic import BaseModel


auth = FastAPI()

class LoginData(BaseModel):
    email: str
    password: int

@auth.post("/api/auth-login")
def read_root(data : LoginData):
    print(data.email, data.password)
    return {"message": f"connexion reussie, Bienvenue {data.email}", "test": "test de fou"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

