#!/usr/bin/env python3
"""Generate placeholder 'fountain pen page' images so the shelf isn't empty.
Delete these once you've uploaded real entries."""
import math, random, os
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), "..", "entries")
W, H = 1100, 1500
INK = (26, 34, 58)


def paper():
    img = Image.new("RGB", (W, H), (238, 232, 218))
    px = img.load()
    for y in range(H):
        for x in range(0, W, 2):
            n = random.randint(-7, 7)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
            px[min(W - 1, x + 1), y] = px[x, y]
    # warm blotching
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(180):
        cx, cy = random.randint(0, W), random.randint(0, H)
        r = random.randint(40, 260)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(206, 192, 164, 9))
    return img.filter(ImageFilter.GaussianBlur(0.6))


def stroke(d, pts, width, alpha):
    for i in range(len(pts) - 1):
        w = max(1, width * (0.65 + 0.55 * math.sin(i * 0.5)))
        d.line([pts[i], pts[i + 1]], fill=INK + (alpha,), width=int(round(w)))


def word(d, x, y, length, xh, scale):
    """One cursive-ish word: a wavy baseline-hugging squiggle with ascenders."""
    pts = []
    t = 0.0
    px_ = x
    phase = random.uniform(0, 6.28)
    while t < length:
        loop = math.sin(t * 0.55 + phase)
        asc = 0.0
        if random.random() < 0.004:
            asc = -xh * random.uniform(0.7, 1.4)
        py = y - xh * 0.5 * (loop + 1) + asc + math.sin(t * 0.11) * 2
        pts.append((px_, py))
        px_ += 1.5 * scale
        t += 1.5
    stroke(d, pts, 3.1 * scale, 235)
    return px_


def page(seed):
    random.seed(seed)
    img = paper()
    d = ImageDraw.Draw(img, "RGBA")
    margin = 110
    y = 210
    line_h = 74
    while y < H - 160:
        x = margin + random.randint(0, 18)
        limit = W - margin - random.randint(0, 260)
        while x < limit:
            wl = random.randint(18, 78)
            x = word(d, x, y, wl, random.uniform(20, 26), 1.0)
            x += random.randint(14, 30)
        y += line_h + random.randint(-4, 6)
    img = img.filter(ImageFilter.GaussianBlur(0.35))
    return img


if __name__ == "__main__":
    import sys, datetime
    os.makedirs(OUT, exist_ok=True)
    today = datetime.date.today()
    dates = [today, today - datetime.timedelta(days=3), today - datetime.timedelta(days=9),
             today - datetime.timedelta(days=17), today - datetime.timedelta(days=26)]
    for i, dt in enumerate(dates):
        p = os.path.join(OUT, f"{dt.isoformat()}-sample.jpg")
        page(i * 91 + 7).save(p, quality=78, optimize=True)
        print("wrote", p)
