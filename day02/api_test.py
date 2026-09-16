import requests
url = "https://this-domain-does-not-exist-123456.com"
response = requests.get(url, timeout=10)
response.raise_for_status()