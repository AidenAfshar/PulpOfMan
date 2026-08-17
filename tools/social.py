"""Render the social-share card and the home-screen icons from the live page."""
from playwright.sync_api import sync_playwright
from PIL import Image

URL = "http://localhost:8899/index.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(2500)
    pg.screenshot(path="assets/og.png")
    b.close()

og = Image.open("assets/og.png").convert("RGB").resize((1200, 630), Image.LANCZOS)
og.save("assets/og.jpg", quality=86, optimize=True)

# icon: a scroll standing against the wall, square crop
wall = Image.open("assets/wall.jpg").convert("RGBA").crop((90, 90, 602, 602))
sc = Image.open("assets/scroll-1.png")
sc = sc.resize((int(sc.width * 380 / sc.height), 380), Image.LANCZOS)
wall.alpha_composite(sc, ((512 - sc.width) // 2, 70))
for n in (180, 512):
    wall.resize((n, n), Image.LANCZOS).convert("RGB").save(f"assets/icon-{n}.png", optimize=True)
