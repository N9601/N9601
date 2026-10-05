"""Draws the circuit-board chip art for the neofetch card.

Writes assets/ascii.txt (glyphs) and assets/ascii-colors.txt (one color key per
glyph: b=blue o=orange r=red m=muted w=bright, space=default).
Run: python scripts/chip.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 38, 25

grid = [[" "] * W for _ in range(H)]
color = [[" "] * W for _ in range(H)]
links = {}  # (x, y) -> set of directions a trace leaves the cell in

BOX = {
    frozenset("lr"): "─", frozenset("ud"): "│", frozenset("dr"): "┌", frozenset("dl"): "┐",
    frozenset("ur"): "└", frozenset("ul"): "┘", frozenset("udr"): "├", frozenset("udl"): "┤",
    frozenset("dlr"): "┬", frozenset("ulr"): "┴", frozenset("udlr"): "┼",
    frozenset("l"): "─", frozenset("r"): "─", frozenset("u"): "│", frozenset("d"): "│",
}


def put(x, y, ch, c=" "):
    grid[y][x] = ch
    color[y][x] = c


def trace(points, c, start_via=False, end_via=True):
    """Polyline through grid points; corners are resolved to box glyphs."""
    cells = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx = (x1 > x0) - (x1 < x0)
        dy = (y1 > y0) - (y1 < y0)
        x, y = x0, y0
        while (x, y) != (x1, y1):
            nx, ny = x + dx, y + dy
            d1 = "r" if dx > 0 else "l" if dx < 0 else "d" if dy > 0 else "u"
            d2 = {"r": "l", "l": "r", "u": "d", "d": "u"}[d1]
            links.setdefault((x, y), set()).add(d1)
            links.setdefault((nx, ny), set()).add(d2)
            cells.append((x, y))
            x, y = nx, ny
        cells.append((x, y))
    for x, y in cells:
        color[y][x] = c
    ends = []
    if start_via:
        ends.append(points[0])
    if end_via:
        ends.append(points[-1])
    return ends


# Chip body
cx0, cy0, cx1, cy1 = 10, 6, 27, 18
vias = []

# Traces first so the chip outline draws over their inner ends.
vias += trace([(13, cy0), (13, 3), (3, 3), (3, 0)], "b")
vias += trace([(17, cy0), (17, 1), (8, 1)], "o")
vias += trace([(21, cy0), (21, 0)], "r")
vias += trace([(25, cy0), (25, 3), (35, 3)], "b")
vias += trace([(cx0, 9), (5, 9), (5, 6), (1, 6)], "o")
vias += trace([(cx0, 12), (0, 12)], "b", end_via=False)
vias += trace([(cx0, 15), (6, 15), (6, 20), (1, 20)], "r")
vias += trace([(cx1, 9), (33, 9), (33, 7), (37, 7)], "r", end_via=False)
vias += trace([(cx1, 12), (36, 12)], "o")
vias += trace([(cx1, 15), (36, 15)], "b")
vias += trace([(15, cy1), (15, 22), (8, 22), (8, 24)], "o", end_via=False)
vias += trace([(19, cy1), (19, 23), (26, 23)], "b")
vias += trace([(23, cy1), (23, 20), (33, 20), (33, 24)], "r", end_via=False)

for (x, y), dirs in links.items():
    put(x, y, BOX[frozenset(dirs)], color[y][x])
for x, y in vias:
    put(x, y, "●", color[y][x])

# Package outline with pins
for x in range(cx0, cx1 + 1):
    for y in (cy0, cy1):
        pin = (x - cx0) % 2 == 1 and cx0 < x < cx1
        edge_link = (x, y) in links
        ch = "─"
        if pin:
            ch = ("┴" if y == cy0 else "┬") if edge_link else ("╨" if y == cy0 else "╥")
        put(x, y, ch, "m")
for y in range(cy0, cy1 + 1):
    for x in (cx0, cx1):
        pin = (y - cy0) % 3 == 0 and cy0 < y < cy1
        ch = ("┤" if x == cx0 else "├") if pin else "│"
        put(x, y, ch, "m")
put(cx0, cy0, "╭", "m"); put(cx1, cy0, "╮", "m")
put(cx0, cy1, "╰", "m"); put(cx1, cy1, "╯", "m")
for y in range(cy0 + 1, cy1):
    for x in range(cx0 + 1, cx1):
        put(x, y, " ")

# Die and labels
put(cx0 + 2, cy0 + 2, "◉", "m")
for x, ch in enumerate("╌" * 12):
    put(cx0 + 3 + x, cy0 + 4, ch, "b")
    put(cx0 + 3 + x, cy1 - 3, ch, "b")


def label(y, text, c):
    x0 = cx0 + 1 + ((cx1 - cx0 - 1) - len(text)) // 2
    for i, ch in enumerate(text):
        put(x0 + i, y, ch, c)


label(cy0 + 5, "N K R", "w")
label(cy0 + 6, "─────", "m")
label(cy0 + 7, "GO·TS·C·ASM", "o")
label(cy0 + 8, "REV 2026", "m")

(ROOT / "assets" / "ascii.txt").write_text(
    "\n".join("".join(r).rstrip() for r in grid) + "\n", encoding="utf-8")
(ROOT / "assets" / "ascii-colors.txt").write_text(
    "\n".join("".join(r) for r in color) + "\n", encoding="utf-8")
print("\n".join("".join(r) for r in grid))
