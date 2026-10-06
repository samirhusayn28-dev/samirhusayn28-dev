"""source-prepped.png -> portrait-ascii.svg (rows 'type' in left-to-right)."""
import html
from PIL import Image, ImageOps

SRC, OUT = "source-prepped.png", "portrait-ascii.svg"
COLS = 100
CW, LH, FS = 3.7, 6.9, 6.2          # char width, line height, font size
RAMP = " .'`^:-=+*cs#%@"            # bright (sparse) -> dark (dense)
ROW_DELAY, ROW_DUR = 0.07, 0.7

img = Image.open(SRC).convert("L")
w, h = img.size
rows = max(1, round(COLS * (h / w) * (CW / LH)))
img = ImageOps.autocontrast(img.resize((COLS, rows), Image.LANCZOS), cutoff=2)
px = img.load()

W, H = COLS * CW, rows * LH
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.1f} {H:.1f}">',
         '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;'
         f'font-size:{FS}px;fill:#57606a;white-space:pre}}'
         '.cur{fill:#57606a}'
         '@media (prefers-color-scheme:dark){text,.cur{fill:#c9d1d9}}</style><defs>']
for r in range(rows):
    parts.append(f'<clipPath id="c{r}"><rect x="0" y="{r*LH:.2f}" width="0" height="{LH:.2f}">'
                 f'<animate attributeName="width" from="0" to="{W:.1f}" begin="{r*ROW_DELAY:.2f}s" '
                 f'dur="{ROW_DUR}s" fill="freeze"/></rect></clipPath>')
parts.append('</defs>')
for r in range(rows):
    line = "".join(RAMP[min(len(RAMP) - 1, int((255 - px[c, r]) / 256 * len(RAMP)))] for c in range(COLS))
    if not line.strip():
        continue
    y = (r + 0.8) * LH
    parts.append(f'<g clip-path="url(#c{r})"><text x="0" y="{y:.2f}" xml:space="preserve" '
                 f'textLength="{W:.1f}" lengthAdjust="spacing">{html.escape(line)}</text></g>')
    parts.append(f'<rect class="cur" x="0" y="{r*LH+1:.2f}" width="{CW:.1f}" height="{LH-2:.2f}" opacity="0">'
                 f'<animate attributeName="x" from="0" to="{W-CW:.1f}" begin="{r*ROW_DELAY:.2f}s" dur="{ROW_DUR}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="1" begin="{r*ROW_DELAY:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{r*ROW_DELAY+ROW_DUR:.2f}s"/></rect>')
parts.append('</svg>')
open(OUT, "w").write("\n".join(parts))
print(f"wrote {OUT} ({COLS}x{rows})")
