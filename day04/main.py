from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import (
    AsyncOpenAI,
    AuthenticationError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    APIError
)
from dotenv import load_dotenv
import os


# =========================
# 1. Environment
# =========================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env")


# =========================
# 2. OpenAI Client
# =========================

client = AsyncOpenAI(api_key=api_key)


# =========================
# 3. FastAPI
# =========================

app = FastAPI(
    title="AI Agent 20 Days - Day 04",
    description="A simple multi-turn AI chat API",
    version="1.0.0"
)


# =========================
# 4. Request Models
# =========================

class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ResetRequest(BaseModel):
    conversation_id: str


# =========================
# 5. Conversation State
# =========================

# conversation_id -> last response_id
#
# Example:
#
# {
#     "user_a": "resp_abc123",
#     "user_b": "resp_xyz789"
# }

conversations = {}


# =========================
# 6. Health API
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# 7. Chat API
# =========================

@app.post("/chat")
async def chat(request: ChatRequest):

    # 找到这个 conversation 上一轮的 response_id
    previous_response_id = conversations.get(
        request.conversation_id
    )

    try:
        response = await client.responses.create(
            model="gpt-5.6-luna",

            instructions="""
            You are an AI assistant specializing in artificial intelligence,
            cryptocurrency, blockchain, and Real-World Assets (RWA).

            When the user mentions RWA, interpret it as Real-World Assets
            unless the context clearly indicates otherwise.

            Answer clearly and concisely.
            """,

            previous_response_id=previous_response_id,

            input=request.message
        )

        # 保存最新 response_id
        conversations[request.conversation_id] = response.id

        return {
            "conversation_id": request.conversation_id,
            "answer": response.output_text,
            "response_id": response.id
        }

    except AuthenticationError:
        raise HTTPException(
            status_code=500,
            detail="LLM authentication failed"
        )

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="LLM rate limit or quota exceeded"
        )

    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="LLM request timed out"
        )

    except APIConnectionError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to LLM service"
        )

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="LLM service error"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


# =========================
# 8. Reset Conversation API
# =========================

@app.post("/chat/reset")
def reset_chat(request: ResetRequest):

    conversation_id = request.conversation_id

    if conversation_id in conversations:
        del conversations[conversation_id]

        return {
            "conversation_id": conversation_id,
            "status": "reset"
        }

    return {
        "conversation_id": conversation_id,
        "status": "not_found"
    }