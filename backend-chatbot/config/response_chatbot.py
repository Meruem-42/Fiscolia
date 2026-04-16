from fastapi import FastAPI
from pydantic import BaseModel
from test import get_agent_answer



class UserFront(BaseModel):
    question: str

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield



app = FastAPI()

@app.post("/api/chatbot")
def response_chatbot(data : UserFront):
    try:
        answer = get_agent_answer(data.question)
        return {"message": f"{answer}"}
    except :
        return {"message": f"Error on AI backend"}