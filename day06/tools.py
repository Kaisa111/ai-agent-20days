import os
import requests

from dotenv import load_dotenv


load_dotenv()


def get_crypto_price(symbol):
    symbol = symbol.upper()

    coin_ids = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana"
    }

    coin_id = coin_ids.get(symbol)

    if coin_id is None:
        return {
            "error": f"Unsupported cryptocurrency: {symbol}"
        }

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        coin_data = data.get(coin_id)

        if coin_data is None:
            return {
                "error": "Cryptocurrency data not found"
            }

        return {
            "symbol": symbol,
            "price_usd": coin_data.get("usd"),
            "change_24h_percent": coin_data.get("usd_24h_change")
        }


    except requests.Timeout:
        return {
            "error": "CoinGecko request timed out"
        }

    except requests.RequestException as e:
        return {
            "error": f"CoinGecko request failed: {str(e)}"
        }


def calculate_position(investment_usd, price_usd):

    if price_usd <= 0:
        return {
            "error": "price_usd must be greater than 0"
        }

    amount = investment_usd / price_usd

    return {
        "investment_usd": investment_usd,
        "price_usd": price_usd,
        "crypto_amount": amount
    }

def search_crypto_news(query):
    url = "https://newsapi.org/v2/everything"

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        raise ValueError("NEWS_API_KEY not found in .env")

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5
    }

    headers = {
        "X-Api-Key": api_key
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return {
                "error": f"No news articles found for query: {query}"
            }

        clean_articles = []

        for article in articles:
            clean_article = {
             "source": article.get("source", {}).get("name"),
             "title": article.get("title"),
             "description": article.get("description"),
             "published_at": article.get("publishedAt"),
             "url": article.get("url")
            }

            clean_articles.append(clean_article)

        return clean_articles

    except requests.RequestException as e:
        print(f"NewsAPI request failed: {e}")
        return None

    except requests.RequestException as e:
        return {
            "error": f"NewsAPI request failed: {str(e)}"
        }
