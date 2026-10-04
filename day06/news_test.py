from day06.tools import search_crypto_news


news = search_crypto_news("Bitcoin")

if news is None:
    print("Failed to fetch news.")

else:
    for index, article in enumerate(news, start=1):
        print(f"\n===== Article {index} =====")
        print(f"Source: {article['source']}")
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"Published At: {article['published_at']}")
        print(f"URL: {article['url']}")