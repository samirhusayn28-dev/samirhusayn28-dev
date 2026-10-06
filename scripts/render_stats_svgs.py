"""data/stats.json -> stats-card.svg, langs.svg, projects.svg"""
import json, datetime as dt
from common import *

# repos to feature (case-insensitive); missing ones are skipped and filled with most recently pushed
FEATURED = ["patient-health-tracker", "eyespeaks", "studio-xenos", "warda-portfolio"]
LANG_COLORS = {"TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5", "HTML": "#e34c26",
               "CSS": "#563d7c", "Java": "#b07219", "C++": "#f34b7d", "C": "#555555", "Shell": "#89e051",
               "Jupyter Notebook": "#DA5B0B", "Dart": "#00B4AB", "PHP": "#4F5D95", "Vue": "#41b883",
               "SCSS": "#c6538c", "GLSL": "#5686a5", "Go": "#00ADD8", "Rust": "#dea584", "Kotlin": "#A97BFF"}
d = json.load(open("data/stats.json"))

def ago(iso):
    s = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds()
    for n, u in ((86400 * 365, "y"), (86400 * 30, "mo"), (86400, "d"), (3600, "h")):
        if s >= n:
            return f"{int(s // n)}{u} ago"
    return "just now"

# ---------- stats-card.svg
created = dt.datetime.fromisoformat(d["created_at"].replace("Z", "+00:00"))
months = int((dt.datetime.now(dt.timezone.utc) - created).days // 30.4)
member = f"{months // 12}y {months % 12}m" if months >= 12 else f"{months}m"
top = next(iter(d["langs"]), "n/a")
fields = [("repos", d["public_repos"]), ("stars", d["stars"]), ("forks", d["forks"]), ("followers", d["followers"]),
          ("following", d["following"]), ("member_for", member), ("top_lang", top)]
b = [typed(20, 66, [("$ ", "grn"), ("gh api /user | jq", "")], 0.2, 0.9), line(20, 96, "{", 1.2)]
y = 118
for i, (k, v) in enumerate(fields):
    isnum = isinstance(v, int)
    val = [(str(v), "grn")] if isnum else [(f'"{v}"', "ylw")]
    comma = [("," if i < len(fields) - 1 else "", "dim")]
    b.append(line(20, y, [(f'  "{k}":'.ljust(16), "acc")] + val + comma, 1.3 + i * 0.25))
    y += 22
b.append(line(20, y + 2, "}", 3.2))
open("stats-card.svg", "w").write(window(425, y + 28, f"gh api users/{d['user']}", "".join(b)))

# ---------- langs.svg
tot = sum(d["langs"].values()) or 1
items = list(d["langs"].items())[:6]
other = tot - sum(v for _, v in items)
if other > 0:
    items.append(("other", other))
BW, X = 385, 20
bars, x = [], X
for name, v in items:
    w = max(2.0, BW * v / tot)
    bars.append(f'<rect x="{x:.1f}" y="82" width="{w:.1f}" height="10" fill="{LANG_COLORS.get(name, "#8b949e")}"/>')
    x += w
rid, cid = uid("r"), uid("c")
b = [typed(20, 66, [("$ ", "grn"), ("cloc --by-lang ~/repos", "")], 0.2, 1.0),
     f'<clipPath id="{cid}"><rect x="{X}" y="82" width="{BW}" height="10" rx="5"/></clipPath>'
     f'<clipPath id="{rid}"><rect x="{X}" y="82" width="0" height="10"><animate attributeName="width" from="0" to="{BW}" '
     f'begin="1.3s" dur="1.2s" fill="freeze"/></rect></clipPath>'
     f'<g clip-path="url(#{cid})"><g clip-path="url(#{rid})">{"".join(bars)}</g></g>']
y = 124
for i, (name, v) in enumerate(items):
    c = LANG_COLORS.get(name, "#8b949e")
    b.append(f'<circle cx="{X + 5}" cy="{y - 4}" r="5" fill="{c}"/>')
    b.append(line(X + 18, y, [(f"{name:<18}", ""), (f"{100 * v / tot:5.1f}%", "dim")], 1.8 + i * 0.2))
    y += 22
open("langs.svg", "w").write(window(425, y + 14, "cloc", "".join(b)))

# ---------- projects.svg
byname = {r["name"].lower(): r for r in d["repos"]}
rows = [byname[n.lower()] for n in FEATURED if n.lower() in byname]
for r in sorted(d["repos"], key=lambda r: r["pushed_at"], reverse=True):
    if len(rows) >= 4:
        break
    if r not in rows:
        rows.append(r)
b = [typed(24, 66, [("$ ", "grn"), ("ls -la ~/projects", "")], 0.2, 1.0)]
y = 98
for i, r in enumerate(rows):
    desc = (r["description"] or "no description yet")
    desc = desc if len(desc) <= 72 else desc[:69] + "..."
    lang = r["language"] or "n/a"
    t = 1.3 + i * 0.5
    b.append(line(24, y, [("drwxr-xr-x  ", "dim"), (r["name"], "acc"), ("  " + desc, "dim")], t, ""))
    b.append(f'<circle cx="{24 + 6}" cy="{y + 16}" r="5" fill="{LANG_COLORS.get(lang, "#8b949e")}"/>')
    b.append(line(42, y + 20, [(f"{lang:<14}", ""), (f"stars {r['stargazers_count']:<3}", "ylw"),
                               (f"forks {r['forks_count']:<3}", "pur"), (f"updated {ago(r['pushed_at'])}", "dim")], t + 0.15))
    y += 58
open("projects.svg", "w").write(window(860, y + 6, "ls", "".join(b)))
print("wrote stats-card.svg langs.svg projects.svg")
