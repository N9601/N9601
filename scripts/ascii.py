"""One-off: turn a portrait into assets/ascii.txt for the neofetch card.

Usage: python scripts/ascii.py path/to/photo.png [cols]
Needs Pillow. The background is masked out so only the subject is drawn.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAMP = " .`'^,:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

src = Path(sys.argv[1])
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 42

img = Image.open(src).convert("L")
w, h = img.size
s = w / 442  # mask coords below are tuned on the 442px GitHub avatar

# Head + shoulders silhouette; everything outside is treated as empty space.
mask = Image.new("L", img.size, 0)
d = ImageDraw.Draw(mask)
d.ellipse([162 * s, 92 * s, 280 * s, 248 * s], fill=255)
d.polygon([(x * s, y * s) for x, y in [
    (188, 215), (256, 215), (300, 238), (360, 262), (400, 300), (432, 400),
    (442, 442), (40, 442), (66, 360), (100, 280), (140, 248)]], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(3 * s))

crop = (124 * s, 80 * s, 320 * s, 330 * s)
img, mask = img.crop(crop), mask.crop(crop)
# Equalize using only subject pixels so the face gets the full glyph range.
img = ImageOps.equalize(img, mask=mask.point(lambda v: 255 if v > 128 else 0))
img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=160))

# Characters are roughly twice as tall as they are wide.
rows = int(cols * img.height / img.width * 0.5)
img = img.resize((cols, rows), Image.LANCZOS)
mask = mask.resize((cols, rows), Image.LANCZOS)

lines = []
for y in range(rows):
    row = ""
    for x in range(cols):
        m = mask.getpixel((x, y)) / 255
        if m < 0.35:
            row += " "
            continue
        # Bright pixel -> dense glyph, so the subject glows on a dark card.
        v = (img.getpixel((x, y)) / 255) ** 0.75 * m
        row += RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))]
    lines.append(row.rstrip())

out = ROOT / "assets" / "ascii.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"\n{cols}x{rows} -> {out}")
