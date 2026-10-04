from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from day06.agent import run_agent


app = FastAPI(
    title="Crypto Research Agent API",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Crypto Research Agent API"
    }


@app.post(
    "/research",
    response_model=ResearchResponse
)
def research(request: ResearchRequest):

    try:
        answer = run_agent(request.question)

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )