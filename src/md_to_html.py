# src/md_to_html.py – turn the newest digest into docs/index.html
import glob, json, datetime as dt, pathlib, markdown

# Locate latest digest
latest_md = pathlib.Path(sorted(glob.glob("digests/rural_bill_digest_*.md"))[-1])
md_html   = markdown.markdown(latest_md.read_text(), extensions=["tables"])

# SimpleCSS for quick styling
html = f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8">
  <title>Rural‑Health Bill Tracker</title>
  <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
</head><body>
<h1>Rural‑Health Bill Tracker</h1>
<p><em>Last updated: {dt.datetime.utcnow():%Y‑%m‑%d %H:%M UTC}</em></p>
{md_html}
<p><a href="{latest_md.name}">Download raw Markdown</a></p>
</body></html>"""

out = pathlib.Path("docs/index.html")
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print("Wrote", out)
