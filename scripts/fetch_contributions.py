"""Scrape public contribution calendar (no token) -> data/contributions.json"""
import json, os, re, datetime as dt
import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER", "samirhusayn28-dev")
r = requests.get(f"https://github.com/users/{USER}/contributions",
                 headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}, timeout=30)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td[data-date]"):
    level = int(td.get("data-level", 0))
    m = re.match(r"(\d+)\s+contribution", tips.get(td.get("id"), ""))
    count = int(m.group(1)) if m else (0 if level == 0 else level)
    days.append({"date": td["data-date"], "count": count, "level": level})
days.sort(key=lambda d: d["date"])
if not days:
    raise SystemExit("no contribution cells found - GitHub markup may have changed")

total = sum(d["count"] for d in days)
longest = run = 0
for d in days:
    run = run + 1 if d["count"] > 0 else 0
    longest = max(longest, run)
cur, i = 0, len(days) - 1
if days[i]["count"] == 0:
    i -= 1  # today may not have contributions yet
while i >= 0 and days[i]["count"] > 0:
    cur += 1
    i -= 1
best = max(days, key=lambda d: d["count"])
monthly = {}
for d in days:
    monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]

os.makedirs("data", exist_ok=True)
json.dump({"user": USER, "total": total, "current_streak": cur, "longest_streak": longest,
           "best_day": best, "monthly": monthly, "days": days,
           "updated": dt.datetime.now(dt.timezone.utc).isoformat()},
          open("data/contributions.json", "w"), indent=1)
print(f"{USER}: {total} contributions, streak {cur}, longest {longest}")
