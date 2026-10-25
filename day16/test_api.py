
import requests

URL = "https://api.llama.fi/protocols"

def main():
    print("[Day16] Testing DefiLlama API...")

    try:
        response = requests.get(
            URL,
            timeout=20,
        )
        response.raise_for_status()

        data = response.json()

        print("HTTP status:", response.status_code)
        print("Response type:", type(data).__name__)
        print("Total protocols:", len(data))

        if data:
            item = data[0]
            print("\nFirst protocol:")
            print("Name:", item.get("name"))
            print("Category:", item.get("category"))
            print("TVL:", item.get("tvl"))

    except requests.RequestException as exc:
        print("API request failed:", exc)

if __name__ == "__main__":
    main()
