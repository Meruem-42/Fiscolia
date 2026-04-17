from fastapi import FastAPI
from pydantic import BaseModel
from test import get_agent_answer
from create_vector_db import run_ingestion
from contextlib import asynccontextmanager


class UserFront(BaseModel):
    question: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Vérification et ingestion des données...")
    try:
        run_ingestion()
        print("Base de données vectorielle prête.")
    except:
        print(f"Erreur lors de l'ingestion")
    yield  # Le serveur tourne ici

# On passe le lifespan à l'app
app = FastAPI(lifespan=lifespan)

@app.post("/api/chatbot")
def response_chatbot(data : UserFront):
    try:
        answer = get_agent_answer(data.question)
        return {"message": f"{answer}"}
    except :
        return {"message": f"Error on AI backend"}