"""Static art (edit text below, run once): banner.svg, status.svg, skills.svg"""
from common import *

W = 860

def banner():
    b, y = [], 70
    b.append(typed(24, y, [("$ ", "grn"), ("./boot.sh --user samir", "")], 0.3, 1.2))
    b.append(line(24, 118, [("Samir Husayn", "acc")], 1.7, "font-size:38px;font-weight:700"))
    b.append(line(24, 144, [("Full Stack Developer · AI Explorer · Islamabad, Pakistan", "dim")], 2.0))
    rows = [("OK", "identity", "Full Stack Developer"),
            ("OK", "stack", "React · Next.js · Node.js · Python"),
            ("OK", "ai-lab", "TensorFlow · PyTorch · OpenCV"),
            ("..", "building", "Patient Health Tracking System"),
            ("OK", "network", "open to React & Python collaborations")]
    y = 184
    for i, (st, name, val) in enumerate(rows):
        dots = "." * (16 - len(name))
        c = "grn" if st == "OK" else "ylw"
        b.append(line(24, y, [("[ ", "dim"), (st, c), (" ] ", "dim"), (name + " " + dots + " ", "dim"), (val, "")], 2.4 + i * 0.4))
        y += 22
    b.append(line(24, y + 6, [("$ ", "grn"), ("echo $FUN_FACT", "")], 4.6))
    b.append(line(24, y + 28, [("I debug faster at 2am", "ylw")], 4.9))
    b.append(line(24, y + 56, [("$ ", "grn")], 5.2))
    b.append(cursor(24 + 2 * CW, y + 56, 5.2))
    return window(W, y + 80, "samir@islamabad: ~", "".join(b))

def status():
    units = [
        ("●", "grn", "patient-health-tracker.service", "Patient Health Tracking System", "active (running)", "grn"),
        ("●", "grn", "studio-xenos.service", "Agency brand · portfolio · WebGL", "active (running)", "grn"),
        ("●", "grn", "learning.service", "Next.js · Express.js · TensorFlow", "active (running)", "grn"),
        ("●", "acc", "collab.socket", "Open to React & Python projects", "listening on :react :python", "acc"),
        ("○", "ylw", "system-design.service", "System Design & Cloud Architecture", "waiting (need help here)", "ylw"),
    ]
    b = [typed(24, 66, [("$ ", "grn"), ("systemctl status --user samir.target", "")], 0.2, 1.3)]
    y = 98
    for i, (dot, dc, name, desc, act, ac) in enumerate(units):
        d = 1.7 + i * 0.5
        b.append(line(24, y, [(dot + " ", dc), (name, "acc"), (" - " + desc, "dim")], d))
        b.append(line(24, y + 20, [("     Active: ", "dim"), (act, ac)], d + 0.15))
        y += 52
    return window(W, y + 6, "systemctl", "".join(b))

def skills():
    tree = [("frontend/", "React · Next.js · TypeScript · JavaScript · Tailwind · Three.js · Vite · HTML5 · CSS3"),
            ("backend/", "Node.js · Express.js · Flask · MongoDB · MySQL · Firebase"),
            ("ai-ml/", "Python · TensorFlow · PyTorch · OpenCV · NumPy · Pandas"),
            ("cloud/", "AWS · Google Cloud · Vercel · Netlify"),
            ("tools/", "Git · GitHub · Figma · Arduino · Linux")]
    b = [typed(24, 66, [("$ ", "grn"), ("tree ~/stack", "")], 0.2, 0.8),
         line(24, 94, [("~/stack", "acc")], 1.1)]
    y = 94 + 24
    for i, (d, items) in enumerate(tree):
        br = "└── " if i == len(tree) - 1 else "├── "
        b.append(line(24, y, [(br, "dim"), (f"{d:<10}", "pur"), (items, "")], 1.3 + i * 0.35))
        y += 24
    b.append(line(24, y + 14, [("5 directories, 33 tools", "dim")], 3.2))
    return window(W, y + 40, "tree", "".join(b))

for name, fn in (("banner.svg", banner), ("status.svg", status), ("skills.svg", skills)):
    open(name, "w").write(fn())
    print("wrote", name)
