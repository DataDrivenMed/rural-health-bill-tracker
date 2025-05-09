# src/fetch_bills.py – pulls rural‑health bills from GovTrack
import json, datetime as dt, pathlib, requests, urllib.parse

TODAY = dt.date.today()
DATA_DIR = pathlib.Path("data"); DATA_DIR.mkdir(exist_ok=True)

def fetch_govtrack(query="rural health OR critical access OR telehealth", congress=118):
    base = "https://www.govtrack.us/api/v2/bill"
    params = {
        "congress": congress,
        "search": query,
        "sort": "-current_status_date",
        "limit": 100
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    out = DATA_DIR / f"bills_{TODAY}.json"
    out.write_text(json.dumps(r.json(), indent=2))
    print("Saved", out)

if __name__ == "__main__":
    fetch_govtrack()
