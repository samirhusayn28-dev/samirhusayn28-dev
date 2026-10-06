"""data/contributions.json -> contrib-heatmap.svg (53x7 rounded boxes, diagonal slide-in)."""
import json, datetime as dt, math

d = json.load(open("data/contributions.json"))
days = d["days"]
CELL, GAP = 12, 3
P = CELL + GAP
X0, Y0, W = 40, 44, 860
off = (dt.date.fromisoformat(days[0]["date"]).weekday() + 1) % 7   # Sunday-first
weeks = math.ceil((off + len(days)) / 7)
H = Y0 + 7 * P + 62
peak = max(x["count"] for x in days) or 1

def lvl(x):
    return 5 if x["level"] >= 4 and x["count"] >= peak * 0.75 else x["level"]

DARK = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69ff8a"]
LIGHT = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39", "#0a3d1f"]
css = ("text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11px;fill:#57606a}"
       ".b{font-size:12px}"
       ".c{opacity:0;transform:translateY(-10px);animation:s .45s ease-out forwards}"
       "@keyframes s{to{opacity:1;transform:none}}"
       + "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(LIGHT))
       + "@media (prefers-color-scheme:dark){text{fill:#8b949e}"
       + "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(DARK)) + "}")

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}</style>']
for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    o.append(f'<text x="4" y="{Y0 + r*P + 10}">{name}</text>')
last_m = None
for i, x in enumerate(days):
    col, row = divmod(i + off, 7)
    dd = dt.date.fromisoformat(x["date"])
    if (row == 0 or i == 0) and dd.month != last_m:
        last_m = dd.month
        if col < weeks - 2:
            o.append(f'<text x="{X0 + col*P}" y="{Y0 - 10}">{dd.strftime("%b")}</text>')
    delay = (col + row) * 0.018
    o.append(f'<rect class="c l{lvl(x)}" x="{X0 + col*P}" y="{Y0 + row*P}" width="{CELL}" height="{CELL}" rx="3" '
             f'style="animation-delay:{delay:.2f}s"><title>{x["count"]} on {x["date"]}</title></rect>')
fy = Y0 + 7 * P + 26
o.append(f'<text class="b" x="{X0}" y="{fy}">{d["total"]:,} contributions in the last year</text>')
o.append(f'<text x="{X0}" y="{fy + 20}">current streak {d["current_streak"]}d · longest {d["longest_streak"]}d · '
         f'best day {d["best_day"]["count"]} ({d["best_day"]["date"]})</text>')
lx = W - 190
o.append(f'<text x="{lx - 34}" y="{fy}">Less</text>')
for i in range(6):
    o.append(f'<rect class="l{i}" x="{lx + i*(CELL+4)}" y="{fy - 10}" width="{CELL}" height="{CELL}" rx="3"/>')
o.append(f'<text x="{lx + 6*(CELL+4) + 4}" y="{fy}">More</text></svg>')
open("contrib-heatmap.svg", "w").write("\n".join(o))
print("wrote contrib-heatmap.svg")
