from fastapi import FastAPI
from pydantic import BaseModel
from test.py import 



class UserFront(BaseModel):
    question: str

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield



app = FastAPI()

@app.post("/api/chatbot")
def response_chatbot(data : UserFront):
    try :
        return {"message": f"message sent : {data.question}"}
    except :
        return {"message": f"Error on AI backend"}     