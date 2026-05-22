from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from test import get_agent_answer, OLLAMA_CHAT_MODEL, client_ollama
from contextlib import asynccontextmanager
from starlette.websockets import WebSocketDisconnect


class UserFront(BaseModel):
    question: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Vérification et ingestion des données...")
    try:
        print("test enter lifespan")
        print("Base de données vectorielle prête.")
    except:
        print(f"Erreur lors de l'ingestion")
    yield  # Le serveur tourne ici

# On passe le lifespan à l'app
app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try :
        while True:
            data = await websocket.receive_text()
            try:
                prompt = get_agent_answer(data)

                answer = client_ollama.chat(
                	model=OLLAMA_CHAT_MODEL,
                	messages=[{"role": "user", "content": prompt}],
                	keep_alive="15m",  # Garde le modèle en mémoire pendant 5 minutes
                	stream=True, 
                )

                for elem in answer:
                    chunk = elem["message"]["content"]
                    # Send character by character with a small delay
                    for char in chunk:
                        await websocket.send_text(char)
                        # Optional: small delay for more natural flow
                        # import asyncio
                        # await asyncio.sleep(0.01)  # 10ms between chars
                # await websocket.send_text("Done !")
            except :
                return {"message": f"Error on AI backend"}
    except WebSocketDisconnect:
        print("Client disconnected") 