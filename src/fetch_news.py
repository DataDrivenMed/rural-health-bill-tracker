# src/fetch_news.py – pulls rural‑health headlines via NewsAPI
import os, json, datetime as dt, pathlib, requests

API_KEY = os.getenv("NEWSAPI_KEY")
TODAY = dt.date.today()
DATA_DIR = pathlib.Path("data"); DATA_DIR.mkdir(exist_ok=True)

def fetch_news(query='"rural health" AND (bill OR legislation OR congress)'):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": API_KEY
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    out = DATA_DIR / f"news_{TODAY}.json"
    out.write_text(json.dumps(r.json(), indent=2))
    print("Saved", out)

if __name__ == "__main__":
    fetch_news()
