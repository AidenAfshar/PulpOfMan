import sys, time
from playwright.sync_api import sync_playwright

URL = "http://localhost:8899/index.html"

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in [("desk", 1280, 900), ("phone", 390, 844)]:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        errs = []
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(2500)
        pg.screenshot(path=f"shot-{name}-shelf.png")
        # open the newest scroll
        pg.locator(".slot").first.click()
        pg.wait_for_timeout(2200)
        pg.screenshot(path=f"shot-{name}-open.png")
        print(name, "errors:", errs[:6])
        pg.close()
    b.close()
