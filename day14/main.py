from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests


app = FastAPI()


# =========================
# Pydantic Models
# =========================

class ChatRequest(BaseModel):
    message: str


# =========================
# Health API
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# Crypto API
# =========================

@app.get("/crypto/{symbol}")
def get_crypto(symbol: str):

    # 统一转换成大写
    symbol = symbol.upper()

    # 用户输入的 symbol → CoinGecko 使用的 coin id
    coin_ids = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana"
    }

    coin_id = coin_ids.get(symbol)

    # 不支持的币种
    if coin_id is None:
        raise HTTPException(
            status_code=404,
            detail="Unsupported cryptocurrency"
        )

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        # 请求 CoinGecko
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        # 如果 CoinGecko 返回 4xx / 5xx
        # 在这里抛出 requests 异常
        response.raise_for_status()

        # JSON → Python dict
        data = response.json()

        # 取出当前币种数据
        coin_data = data.get(coin_id)

        # CoinGecko 返回成功，但数据里没有这个币
        if coin_data is None:
            raise HTTPException(
                status_code=502,
                detail="Invalid response from CoinGecko"
            )

        price = coin_data.get("usd")
        change = coin_data.get("usd_24h_change")

        return {
            "symbol": symbol,
            "price": price,
            "change_24h": round(change, 2) if change is not None else None
        }

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="CoinGecko request timed out"
        )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"CoinGecko request failed: {str(e)}"
        )


# =========================
# Query Parameter Demo
# =========================

@app.get("/test-query")
def test_query(symbol: str, currency: str = "usd"):
    return {
        "symbol": symbol,
        "currency": currency
    }


# =========================
# Chat API
# =========================

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": f"You said: {request.message}"
    }