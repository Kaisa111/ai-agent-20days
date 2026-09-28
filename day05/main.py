from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from day05.agent import run_agent

# reload test
app = FastAPI(
    title="Crypto Agent API",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Crypto Agent API",
        "test": "DAY05-CURRENT-SERVER"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    print(">>> /chat 收到请求")
    print(">>> message:", request.message)

    try:
        answer = run_agent(request.message)

        return {
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )