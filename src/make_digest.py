# src/make_digest.py — Build a Markdown digest from latest rural bills

import json
import datetime as dt
import pathlib

TODAY = dt.date.today()

DATA_DIR = pathlib.Path("data")
DIGEST_DIR = pathlib.Path("digests")
DOCS_DIR = pathlib.Path("docs")

DIGEST_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)


def load_latest():
    latest = DATA_DIR / "latest.json"
    if not latest.exists():
        print("[WARN] latest.json not found; no bills to digest.")
        return []

    try:
        bills = json.loads(latest.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[WARN] Failed to read latest.json: {e}")
        return []

    print(f"[INFO] Loaded {len(bills)} rural bills from latest.json.")
    return bills


def build_markdown(bills):
    lines = []
    lines.append(f"# Rural Health Bill Digest — {TODAY.isoformat()}")
    lines.append("")

    if not bills:
        lines.append("_No rural health–related bills found in the latest scan._")
        return "\n".join(lines)

    lines.append(f"Found **{len(bills)}** bills mentioning rural-health-related terms.")
    lines.append("")
    lines.append("Showing up to the latest 20 matches:")
    lines.append("")

    for bill in bills[:20]:
        title = bill.get("title", "Untitled bill")
        summary = bill.get("summary", "")
        xml_url = bill.get("xml_url", "")

        lines.append(f"## {title}")
        if summary:
            trimmed = (summary[:400] + "...") if len(summary) > 400 else summary
            lines.append("")
            lines.append(trimmed)
            lines.append("")
        if xml_url:
            lines.append(f"[View full BILLSTATUS XML]({xml_url})")
        lines.append("")

    return "\n".join(lines)


def write_digest(markdown_text: str):
    dated = DIGEST_DIR / f"{TODAY}.md"
    latest = DIGEST_DIR / "latest.md"
    index = DOCS_DIR / "index.md"

    for path in (dated, latest, index):
        path.write_text(markdown_text, encoding="utf-8")
        print(f"[INFO] Wrote {path}")


def main():
    bills = load_latest()
    md = build_markdown(bills)
    write_digest(md)


if __name__ == "__main__":
    main()
