# src/make_digest.py – converts latest JSON into a Markdown brief
import json, datetime as dt, glob, pathlib

TODAY = dt.date.today().isoformat()
data_dir = pathlib.Path("data")
digest_dir = pathlib.Path("digests"); digest_dir.mkdir(exist_ok=True)

bills_file = max(glob.glob("data/bills_*.json"))
news_file  = max(glob.glob("data/news_*.json"))

bills = json.load(open(bills_file))
news  = json.load(open(news_file))

def link(txt, url): return f"[{txt}]({url})"

lines = [f"# Rural‑Health Bill Digest – {TODAY}\n"]

# Bills table
lines += ["## Bills in Congress", "| Bill | Title | Status | Sponsor |",
          "|------|-------|--------|---------|"]
for bill in bills["objects"]:
    num  = bill["display_number"]
    url = bill.get("congressdotgov_url") or bill.get("link") or bill["urls"]["govtrack"]
    title= (bill["title"] or "")[:80]
    status = bill["current_status"].replace("_", " ").title()
    sponsor = bill["sponsor"]["name"]
    lines.append(f"| {link(num, url)} | {title} | {status} | {sponsor} |")

# Headlines
lines += ["", "## Top Headlines"]
for art in news["articles"][:5]:
    lines.append(f"* {link(art['title'], art['url'])} — {art['source']['name']}")

outfile = digest_dir / f"rural_bill_digest_{TODAY}.md"
outfile.write_text("\n".join(lines))
print("Wrote", outfile)
