"""Shared helpers: terminal-window SVG chrome, theme-aware colors, typing/fade helpers."""
import html, os

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
CW = 7.8  # char width at 13px
PREVIEW = os.environ.get("STATIC") == "1"

CSS = (
    f"text{{font-family:{FONT};font-size:13px;white-space:pre;fill:#24292f}}"
    ".bg{fill:#f6f8fa;stroke:#d0d7de}.sep{stroke:#d0d7de}"
    ".dim{fill:#57606a}.acc{fill:#0969da}.grn{fill:#1a7f37}.ylw{fill:#9a6700}.red{fill:#cf222e}.pur{fill:#8250df}.bar{fill:#d0d7de}"
    "@media (prefers-color-scheme:dark){text{fill:#c9d1d9}.bg{fill:#0d1117;stroke:#30363d}.sep{stroke:#30363d}"
    ".dim{fill:#8b949e}.acc{fill:#58a6ff}.grn{fill:#3fb950}.ylw{fill:#d29922}.red{fill:#f85149}.pur{fill:#bc8cff}.bar{fill:#21262d}}"
    + (".ln{opacity:1}" if PREVIEW else ".ln{opacity:0;animation:fi .45s ease forwards}@keyframes fi{to{opacity:1}}")
)

_n = [0]
def uid(p="x"):
    _n[0] += 1
    return f"{p}{_n[0]}"

def esc(s):
    return html.escape(str(s))

def _segs(segs):
    if isinstance(segs, str):
        segs = [(segs, "")]
    return "".join(f'<tspan class="{c}">{esc(s)}</tspan>' if c else esc(s) for s, c in segs)

def line(x, y, segs, delay=None, style=""):
    cls = ' class="ln"' if delay is not None else ""
    st = style + (f";animation-delay:{delay:.2f}s" if delay is not None else "")
    st = f' style="{st.strip(";")}"' if st.strip(";") else ""
    return f'<text{cls} x="{x}" y="{y}"{st}>{_segs(segs)}</text>'

def typed(x, y, segs, begin, dur):
    """Typewriter reveal (stepped clip) of one line."""
    if isinstance(segs, str):
        segs = [(segs, "")]
    n = sum(len(s) for s, _ in segs)
    cid = uid("t")
    vals = ";".join(f"{i * CW:.1f}" for i in range(n + 1))
    keys = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y - 15}" width="0" height="22">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{keys}" calcMode="discrete" '
            f'begin="{begin}s" dur="{dur}s" fill="freeze"/></rect></clipPath>'
            f'<g clip-path="url(#{cid})">{line(x, y, segs)}</g>')

def cursor(x, y, begin=0):
    return (f'<rect class="acc" x="{x}" y="{y - 12}" width="8" height="15" opacity="0">'
            f'<animate attributeName="opacity" values="1;0" dur="1s" begin="{begin}s" calcMode="discrete" repeatCount="indefinite"/></rect>')

def window(w, h, title, body, css=""):
    dots = "".join(f'<circle cx="{18 + i * 18}" cy="18" r="5.5" fill="{c}"/>'
                   for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{CSS}{css}</style>'
            f'<rect class="bg" x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="9"/>{dots}'
            f'<text class="dim" x="{w / 2}" y="22" text-anchor="middle" style="font-size:12px">{esc(title)}</text>'
            f'<line class="sep" x1="0" y1="36" x2="{w}" y2="36"/>{body}</svg>')
