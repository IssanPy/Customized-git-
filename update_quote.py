from pathlib import Path
from datetime import datetime

README = Path("README.md")
QUOTES = Path("quotes.txt")

if not README.exists():
    raise SystemExit("README.md not found. Place this script at repo root.")

if not QUOTES.exists():
    raise SystemExit("quotes.txt not found. Create it at repo root with one quote per line.")

lines = [l.strip() for l in QUOTES.read_text(encoding="utf-8").splitlines() if l.strip()]
if not lines:
    raise SystemExit("quotes.txt is empty")

# cycle by weekday so it repeats weekly
weekday = datetime.utcnow().weekday()  # 0=Mon .. 6=Sun
quote = lines[weekday % len(lines)]

date = datetime.utcnow().strftime("%Y-%m-%d UTC")
block = f"<!--QUOTE-BEGIN-->\n> {quote}\n\n*Updated: {date}*\n<!--QUOTE-END-->"

text = README.read_text(encoding="utf-8")

if "<!--QUOTE-BEGIN-->" not in text or "<!--QUOTE-END-->" not in text:
    new_text = text.rstrip() + "\n\n" + block + "\n"
else:
    before, rest = text.split("<!--QUOTE-BEGIN-->", 1)
    _, after = rest.split("<!--QUOTE-END-->", 1)
    new_text = before + block + after

if new_text != text:
    README.write_text(new_text, encoding="utf-8")
    print("README updated with quote:", quote)
else:
    print("No update required.")
