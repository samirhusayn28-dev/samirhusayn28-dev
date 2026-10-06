"""Neofetch-style info card -> info-card.svg. Edit CONFIG below. STATIC=1 for a frozen frame."""
import html, os

STATIC = os.environ.get("STATIC") == "1"
OUT = "info-card.svg"
W, LH, PAD, KEYW = 490, 22, 24, 110
USER, HOST = "samir", "github"

CONFIG = [
    ("Role", ["Full Stack Developer"]),
    ("Location", ["Islamabad, Pakistan"]),
    ("Now", ["Patient Health Tracking System"]),
    ("Prev", ["eyespeaks (eye-tracking assistive tech)", "studio-xenos (agency + WebGL)"]),
    ("Stack", ["React · Next.js · Node.js · Express", "Python · TensorFlow · PyTorch · OpenCV"]),
    ("Highlights", ["Open to React & Python projects", "I debug faster at 2am"]),
]

rows = [("title", f"{USER}@{HOST}", None), ("rule", "", None)]
for k, vals in CONFIG:
    for i, v in enumerate(vals):
        rows.append(("kv", k if i == 0 else "", v))
H = PAD * 2 + (len(rows) + 1) * LH

if STATIC:
    anim = ".l{opacity:1}"
else:
    anim = (".l{opacity:0;animation:f .5s ease forwards}"
            "@keyframes f{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}")
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13px;white-space:pre}'
       '.t,.k{fill:#0969da;font-weight:700}.v{fill:#24292f}.r{fill:#8c959f}.p{fill:#1a7f37}'
       '@media (prefers-color-scheme:dark){.t,.k{fill:#58a6ff}.v{fill:#c9d1d9}.r{fill:#6e7681}.p{fill:#3fb950}}'
       + anim + '</style>']
y = PAD + LH
out.append(f'<text class="l p" x="{PAD}" y="{y}">$ neofetch</text>')
for n, (kind, k, v) in enumerate(rows, start=1):
    y += LH
    st = "" if STATIC else f' style="animation-delay:{0.25 + n * 0.18:.2f}s"'
    if kind == "title":
        out.append(f'<text class="l t" x="{PAD}" y="{y}"{st}>{html.escape(k)}</text>')
    elif kind == "rule":
        out.append(f'<text class="l r" x="{PAD}" y="{y}"{st}>{"─" * 30}</text>')
    else:
        out.append(f'<text class="l k" x="{PAD}" y="{y}"{st}>{html.escape(k)}</text>'
                   f'<text class="l v" x="{PAD + KEYW}" y="{y}"{st}>{html.escape(v)}</text>')
out.append('</svg>')
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
