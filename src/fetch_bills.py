# src/fetch_bills.py — Rural health bill scraper using govinfo BILLSTATUS bulk data

import json
import datetime as dt
import pathlib
import requests
import xml.etree.ElementTree as ET

TODAY = dt.date.today()
DATA_DIR = pathlib.Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Index of all BILLSTATUS files for 118th Congress
INDEX_URL = "https://www.govinfo.gov/bulkdata/BILLSTATUS/118/index.xml"

# Keywords to detect rural health–related bills
KEYWORDS = [
    "rural",
    "telehealth",
    "critical access",
    "frontier",
    "medicaid rural",
    "rural hospital",
    "maternal rural",
    "rural workforce",
]


def download_xml(url: str) -> ET.Element | None:
    """Download XML and parse. Return root Element or None on error."""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"[WARN] Failed to download {url}: {e}")
        return None

    try:
        return ET.fromstring(r.content)
    except ET.ParseError as e:
        print(f"[WARN] Failed to parse XML from {url}: {e}")
        return None


def text_matches_rural(text: str) -> bool:
    text = (text or "").lower()
    return any(k in text for k in KEYWORDS)


def fetch_bills():
    print("[INFO] Fetching BILLSTATUS index...")
    index_root = download_xml(INDEX_URL)
    if index_root is None:
        print("[WARN] Could not load index; saving empty dataset.")
        empty = []
        (DATA_DIR / f"rural_bills_{TODAY}.json").write_text(json.dumps(empty, indent=2))
        (DATA_DIR / "latest.json").write_text(json.dumps(empty, indent=2))
        return []

    # govinfo index.xml typically has <file url="/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr1.xml"/>
    files = index_root.findall(".//file")
    bill_urls = []
    for f in files:
        rel = f.get("url")
        if not rel:
            continue
        if not rel.endswith(".xml"):
            continue
        bill_urls.append("https://www.govinfo.gov" + rel)

    print(f"[INFO] Found {len(bill_urls)} bill XML entries in index.")

    # To keep it sane, only look at the last 200 (most recent) bills
    bill_urls = bill_urls[-200:]
    print(f"[INFO] Scanning the latest {len(bill_urls)} bills for rural topics...")

    rural_bills: list[dict] = []

    for url in bill_urls:
        root = download_xml(url)
        if root is None:
            continue

        title = root.findtext(".//title") or ""
        summary = root.findtext(".//summary") or ""

        combined = f"{title} {summary}"
        if text_matches_rural(combined):
            rural_bills.append(
                {
                    "title": title,
                    "summary": summary,
                    "xml_url": url,
                }
            )

    # Save results
    out_path = DATA_DIR / f"rural_bills_{TODAY}.json"
    out_path.write_text(json.dumps(rural_bills, indent=2), encoding="utf-8")
    latest_path = DATA_DIR / "latest.json"
    latest_path.write_text(json.dumps(rural_bills, indent=2), encoding="utf-8")

    print(f"[INFO] Found {len(rural_bills)} rural-related bills.")
    print(f"[INFO] Saved {out_path} and updated {latest_path}.")
    return rural_bills


if __name__ == "__main__":
    fetch_bills()
