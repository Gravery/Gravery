import os
import pathlib
OUT = str(pathlib.Path(__file__).resolve().parent.parent / "assets")
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
THEMES = {
  "dark":  dict(bg="#0d0a0b", panel="#161112", border="#2a2122", grid="#1c1617", ink="#f4f4f5", sub="#a1a1aa", quiet="#71717a", accent="#ef233c", accent_soft="#ef233c22", dim="#241b1c"),
  "light": dict(bg="#ffffff", panel="#fafafa", border="#e4e4e7", grid="#f1f1f3", ink="#18181b", sub="#52525b", quiet="#71717a", accent="#d90429", accent_soft="#d9042914", dim="#ececef"),
}

G = ["..XXXX..",
     ".X....X.",
     "X.......",
     "X..XXXX.",
     "X.....X.",
     "X.....X.",
     ".X....X.",
     "..XXXX.."]

def header(t, c):
    W, H = 1200, 300
    cell, gap = 22, 5
    gx, gy = 900, 50
    cells = []
    lit = 0
    for r, row in enumerate(G):
        for k, ch in enumerate(row):
            x = gx + k * (cell + gap); y = gy + r * (cell + gap)
            if ch == "X":
                cells.append(f'<rect class="px" style="animation-delay:{lit*0.09:.2f}s" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{c["accent"]}"/>')
                lit += 1
            else:
                cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{c["dim"]}"/>')
    side = 8 * cell + 7 * gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Guilherme Calça — backend engineer, Go, distributed systems">
<style>
.px {{ opacity:.12; animation: lit 9s ease-in-out infinite; }}
@keyframes lit {{ 0%{{opacity:.12}} 8%{{opacity:1}} 80%{{opacity:1}} 92%,100%{{opacity:.12}} }}
.cursor {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50%{{opacity:0}} }}
@media (prefers-reduced-motion: reduce) {{ .px{{animation:none;opacity:1}} .cursor{{animation:none}} }}
</style>
<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern></defs>
<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{c["border"]}"/>
<text x="56" y="78" font-family="{MONO}" font-size="16" fill="{c["accent"]}" letter-spacing="2">~/gravery</text>
<text x="56" y="138" font-family="{SANS}" font-size="56" font-weight="800" fill="{c["ink"]}">Guilherme Calça</text>
<text x="58" y="176" font-family="{MONO}" font-size="20" fill="{c["sub"]}">backend engineer · go · distributed systems</text>
<text x="58" y="234" font-family="{MONO}" font-size="17" fill="{c["quiet"]}">$ <tspan fill="{c["ink"]}">go run ./cmd/hello --tz=UTC-3</tspan><tspan class="cursor" fill="{c["accent"]}"> ▍</tspan></text>
<text x="58" y="262" font-family="{MONO}" font-size="17" fill="{c["accent"]}">› open to remote · US / EU</text>
<text x="{gx}" y="{gy+side+28}" font-family="{MONO}" font-size="13" fill="{c["quiet"]}">chunk(0,0) · 64×64 · sync.RWMutex</text>
{"".join(cells)}
</svg>'''

def arch(t, c):
    W, H = 1200, 500
    bw, bh, y0 = 196, 104, 170
    xs = [40, 286, 532, 778, 964+0]
    xs = [40, 281, 522, 763, 1004 - 40]
    xs = [36 + i * (bw + 41) for i in range(5)]
    boxes = [
        ("Browser client", "Canvas 2D engine", "viewport culling"),
        ("WebSocket hub", "Area-of-Interest", "deltas to viewers only"),
        ("Chunk map", "64×64 px per chunk", "one RWMutex each"),
        ("Write-behind", "dirty chunks queued", "flushed every 2 s"),
        ("SQLite", "WAL mode", "batched writes"),
    ]
    edges = ["place pixel", "validate + apply", "mark dirty", "batch flush"]
    out = []
    for i, (name, l1, l2) in enumerate(boxes):
        x = xs[i]; hot = i == 2
        stroke = c["accent"] if hot else c["border"]
        fill = c["accent_soft"] if hot else c["panel"]
        sw = 2 if hot else 1.25
        cx = x + bw / 2
        out.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        out.append(f'<text x="{cx}" y="{y0+36}" text-anchor="middle" font-family="{SANS}" font-size="18" font-weight="700" fill="{c["ink"]}">{name}</text>')
        out.append(f'<text x="{cx}" y="{y0+64}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c["sub"]}">{l1}</text>')
        out.append(f'<text x="{cx}" y="{y0+84}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c["sub"]}">{l2}</text>')
    for i, lab in enumerate(edges):
        x1 = xs[i] + bw + 3; x2 = xs[i+1] - 5; y = y0 + bh / 2
        out.append(f'<path d="M{x1} {y}H{x2}" stroke="{c["quiet"]}" stroke-width="1.5" marker-end="url(#a)"/>')
    # edge labels above the row, centred on the gap
    for i, lab in enumerate(edges):
        gc = xs[i] + bw + 41 / 2
        out.append(f'<text x="{gc}" y="{y0-14}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c["quiet"]}">{lab}</text>')
    # return path hub -> client, below
    yb = y0 + bh
    hx = xs[1] + bw / 2; cx0 = xs[0] + bw / 2
    out.append(f'<path d="M{hx} {yb+4}V{yb+40}H{cx0}V{yb+8}" fill="none" stroke="{c["accent"]}" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
    out.append(f'<text x="{(hx+cx0)/2}" y="{yb+62}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c["accent"]}">broadcast only to intersecting viewports</text>')
    # brackets: hot path (boxes 0-2) / async (3-4)
    by = 122
    def bracket(xa, xb, label, col):
        return (f'<path d="M{xa} {by+10}V{by}H{xb}V{by+10}" fill="none" stroke="{col}" stroke-width="1.5"/>'
                f'<text x="{(xa+xb)/2}" y="{by-10}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="600" fill="{col}" letter-spacing="1">{label}</text>')
    out.append(bracket(xs[0], xs[2] + bw, "HOT PATH · IN MEMORY", c["accent"]))
    out.append(bracket(xs[3], xs[4] + bw, "ASYNC · OFF THE HOT PATH", c["quiet"]))
    # stat tiles
    tiles = [("64×64", "pixels per lock, no global mutex"), ("2 s", "write-behind flush interval"), ("−95%", "payload via AoI filtering"), ("0", "disk writes on the hot path")]
    tw, th, ty, tg = 270, 100, 364, 20
    tx0 = (W - (4 * tw + 3 * tg)) / 2
    for i, (v, l) in enumerate(tiles):
        x = tx0 + i * (tw + tg)
        out.append(f'<rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}"/>')
        out.append(f'<text x="{x+22}" y="{ty+50}" font-family="{SANS}" font-size="34" font-weight="800" fill="{c["accent"]}">{v}</text>')
        out.append(f'<text x="{x+22}" y="{ty+80}" font-family="{MONO}" font-size="12.5" fill="{c["sub"]}">{l}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="PixelPlace architecture: a pixel goes from the browser through a WebSocket hub to an in-memory chunk map, then asynchronously to SQLite">
<defs>
<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c["quiet"]}"/></marker>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c["accent"]}"/></marker>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{c["border"]}"/>
<text x="36" y="52" font-family="{SANS}" font-size="24" font-weight="800" fill="{c["ink"]}">PixelPlace: how one pixel travels</text>
<text x="36" y="80" font-family="{MONO}" font-size="14" fill="{c["quiet"]}">real-time r/place-style canvas · Go · WebSockets · SQLite WAL · private repo, walkthrough on request</text>
{"".join(out)}
</svg>'''

for t, c in THEMES.items():
    open(f"{OUT}/header-{t}.svg", "w").write(header(t, c))
    open(f"{OUT}/pixelplace-{t}.svg", "w").write(arch(t, c))
print(os.listdir(OUT))
