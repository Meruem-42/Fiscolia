from fastapi import FastAPI

auth = FastAPI()

@auth.get("/api/auth")
def read_root():
    return {"message": "connexion reussie", "test": "test de fou"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

