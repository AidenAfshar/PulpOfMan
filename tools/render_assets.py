#!/usr/bin/env python3
"""Render the physical assets for A Pulp Of Man:
   a tileable cobblestone wall, a stone shelf slab, and rolled parchment scrolls.
   Everything is procedural — run it again to reshuffle the stones.
   Output: ../assets/*.png|jpg
"""
import os, math
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
os.makedirs(OUT, exist_ok=True)

# ── helpers ───────────────────────────────────────────────────────────────
def fbm(shape, seed, octaves=5, feature=64.0, gain=0.5):
    """Tileable fractal noise, band-passed in frequency space.
    `feature` is the size of the largest detail IN PIXELS, so the result is
    isotropic no matter how oblong the array is. Output is roughly unit variance."""
    h, w = shape
    rng = np.random.default_rng(seed)
    W = np.fft.fft2(rng.normal(size=(h, w)))
    fy = np.fft.fftfreq(h)          # cycles per pixel
    fx = np.fft.fftfreq(w)
    R = np.sqrt(fy[:, None] ** 2 + fx[None, :] ** 2)
    out = np.zeros((h, w))
    amp, tot, f = 1.0, 0.0, 1.0 / max(feature, 2.0)
    for _ in range(octaves):
        if f > 0.45:
            break
        band = np.exp(-((R - f) ** 2) / (2 * (f * 0.62) ** 2))
        layer = np.real(np.fft.ifft2(W * band))
        s = layer.std()
        if s > 0:
            out += amp * layer / s
        tot += amp
        amp *= gain
        f *= 2.0
    return out / max(tot, 1e-9)


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def norm(v):
    return v / np.linalg.norm(v)


def to8(a):
    return np.clip(a, 0, 1).__pow__(1 / 1.05) * 255


def save_rgb(rgb, path, quality=92):
    img = Image.fromarray(np.clip(rgb, 0, 1).__mul__(255).astype(np.uint8), "RGB")
    if path.lower().endswith((".jpg", ".jpeg")):
        img.save(path, quality=quality, optimize=True, subsampling=0)
    else:
        img.save(path, optimize=True)
    print("  ", os.path.basename(path), img.size)


def save_rgba(rgb, alpha, path):
    a = np.clip(alpha, 0, 1)
    arr = np.dstack([np.clip(rgb, 0, 1) * 255, a * 255]).astype(np.uint8)
    img = Image.fromarray(arr, "RGBA")
    img.save(path, optimize=True)
    print("  ", os.path.basename(path), img.size)


def downsample(a, k):
    """Box-downsample a HxWx? array by integer factor k."""
    h, w = a.shape[0] // k, a.shape[1] // k
    a = a[: h * k, : w * k]
    if a.ndim == 2:
        return a.reshape(h, k, w, k).mean((1, 3))
    return a.reshape(h, k, w, k, a.shape[2]).mean((1, 3))


# ═══════════════════════════════════════════════════════════════════════════
# 1. COBBLESTONE WALL  (tileable)
# ═══════════════════════════════════════════════════════════════════════════
def cobblestone(size=768, cells=10, seed=7):
    print("cobblestone…")
    rng = np.random.default_rng(seed)
    Y, X = np.mgrid[0:size, 0:size].astype(np.float64)

    # gentle warp so the cell walls aren't straight polygon edges
    wx = fbm((size, size), seed + 11, octaves=2, feature=110) * 4.5
    wy = fbm((size, size), seed + 12, octaves=2, feature=110) * 4.5
    wx += fbm((size, size), seed + 13, octaves=2, feature=26) * 1.2
    wy += fbm((size, size), seed + 14, octaves=2, feature=26) * 1.2
    Xw, Yw = X + wx, Y + wy

    step = size / cells
    sx, sy = [], []
    for j in range(cells):
        for i in range(cells):
            sx.append((i + 0.5 + (rng.random() - 0.5) * 0.72) * step)
            sy.append((j + 0.5 + (rng.random() - 0.5) * 0.72) * step)
    n = len(sx)

    F1 = np.full((size, size), 1e9)
    F2 = np.full((size, size), 1e9)
    ID = np.zeros((size, size), np.int32)
    for i in range(n):
        dx = np.abs(Xw - sx[i]); dx = np.minimum(dx, size - dx)
        dy = np.abs(Yw - sy[i]); dy = np.minimum(dy, size - dy)
        d = np.hypot(dx, dy)
        m = d < F1
        F2 = np.where(m, F1, np.minimum(F2, d))
        ID = np.where(m, i, ID)
        F1 = np.where(m, d, F1)

    edge = F2 - F1
    grout = 6.8 + fbm((size, size), seed + 21, octaves=3, feature=34) * 2.6
    t = smooth(0.0, 9.5, edge - grout)           # 0 = mortar, 1 = stone face

    # ── height field ──
    fine = fbm((size, size), seed + 31, octaves=4, feature=26)
    pits = fbm((size, size), seed + 32, octaves=3, feature=8)
    h = (t ** 0.42) * 13.0
    h += fine * 0.40 * t
    h -= np.clip(pits, 0, None) ** 2 * 0.32 * t          # chips and pits
    h += fbm((size, size), seed + 33, octaves=3, feature=9) * 0.7 * (1 - t)  # sandy mortar

    hx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5
    hy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5
    nl = np.sqrt(hx * hx + hy * hy + 1.0)
    Nx, Ny, Nz = -hx / nl, -hy / nl, 1.0 / nl

    L = norm(np.array([-0.40, -0.66, 0.64]))            # lamp above, a little left
    diff = np.clip(Nx * L[0] + Ny * L[1] + Nz * L[2], 0, 1)
    H = norm(L + np.array([0, 0, 1.0]))
    spec = np.clip(Nx * H[0] + Ny * H[1] + Nz * H[2], 0, 1) ** 30

    # ── albedo ──
    pal = np.array([
        [0.38, 0.37, 0.37], [0.34, 0.33, 0.33], [0.40, 0.38, 0.35],
        [0.32, 0.32, 0.34], [0.42, 0.40, 0.38], [0.35, 0.33, 0.31],
        [0.30, 0.29, 0.29], [0.39, 0.37, 0.34],
    ])
    idx = rng.integers(0, len(pal), n)
    val = 0.86 + rng.random(n) * 0.26
    stone_rgb = pal[idx] * val[:, None]
    A = stone_rgb[ID]                                   # (size,size,3)

    granite = fbm((size, size), seed + 41, octaves=3, feature=5.5)
    mottle = fbm((size, size), seed + 42, octaves=3, feature=30)
    A *= (1 + 0.055 * granite + 0.085 * mottle)[..., None]

    mortar = np.array([0.270, 0.254, 0.228])
    msand = fbm((size, size), seed + 51, octaves=3, feature=6.5)
    M = mortar[None, None, :] * (1 + 0.20 * msand)[..., None]

    tt = t[..., None]
    albedo = M * (1 - tt) + A * tt

    grime = smooth(-1.4, 1.4, fbm((size, size), seed + 61, octaves=3, feature=260))
    albedo *= (0.66 + 0.46 * grime)[..., None]

    # ── shade ──
    ao = 0.44 + 0.56 * t ** 0.55
    ao *= 0.80 + 0.20 * smooth(-3, 4, h - 3)
    sky = np.array([0.30, 0.33, 0.40])
    lamp = np.array([1.00, 0.94, 0.82])
    col = albedo * ((0.30 * ao)[..., None] * sky + (0.95 * diff * ao)[..., None] * lamp)
    col += (spec * 0.055 * t)[..., None] * lamp

    col *= 0.40                                          # keep the wall deep in shadow
    col = np.clip(col, 0, 1) ** (1 / 1.9)
    col += (np.random.default_rng(seed + 99).random((size, size, 1)) - 0.5) * 0.012
    save_rgb(col, os.path.join(OUT, "wall.jpg"), quality=90)


# ═══════════════════════════════════════════════════════════════════════════
# 2. STONE SHELF  (tileable across x, transparent below)
# ═══════════════════════════════════════════════════════════════════════════
def shelf(width=2048, top=40, face=78, drop=70, seed=3):
    print("shelf…")
    H = top + face + drop
    Y, X = np.mgrid[0:H, 0:width].astype(np.float64)
    grain = fbm((H, width), seed + 1, octaves=3, feature=3.2)     # granular stone
    pit = fbm((H, width), seed + 2, octaves=3, feature=11)
    broad = fbm((H, width), seed + 3, octaves=3, feature=170)     # slab-scale variation
    chip = fbm((H, width), seed + 4, octaves=2, feature=26)

    col = np.zeros((H, width, 3))
    alpha = np.zeros((H, width))
    warm = np.array([1.00, 0.962, 0.895])

    tex = 1 + 0.26 * grain + 0.15 * pit + 0.12 * broad

    # ── top surface: receding plane, brightest at the near edge ──
    m_top = Y < top
    depth = np.clip(Y / max(top, 1), 0, 1)                        # 0 back → 1 front
    ttop = (0.105 + 0.085 * depth ** 1.4) * tex
    ttop *= 0.60 + 0.40 * smooth(0.0, 0.5, depth)                 # back edge in shadow
    col[m_top] = np.clip(ttop[..., None] * warm, 0, None)[m_top]
    alpha[m_top] = 1.0

    # ── the worn chamfer where the top meets the front ──
    band = np.exp(-((Y - (top - 1.6)) ** 2) / (2 * 2.6 ** 2))
    col += (band * 0.055 * (1 + 0.7 * grain + 0.5 * chip))[..., None] * warm

    # ── front face ──
    m_face = (Y >= top) & (Y < top + face)
    fy = np.clip((Y - top) / max(face, 1), 0, 1)
    fbase = (0.072 - 0.050 * fy ** 0.75) * (1 + 0.30 * grain + 0.19 * pit + 0.14 * broad)
    fbase *= 1 - 0.13 * np.exp(-((Y - (top + face * 0.30)) ** 2) / (2 * 3.0 ** 2))
    col[m_face] = np.clip(fbase, 0, None)[..., None][m_face] * warm
    alpha[m_face] = 1.0

    # ── shadow thrown down the wall ──
    m_drop = Y >= top + face
    dy = (Y - (top + face)) / max(drop, 1)
    sh = (1 - dy) ** 2.0 * 0.86 * (1 + 0.08 * broad)
    col[m_drop] = 0.0
    alpha[m_drop] = np.clip(sh, 0, 1)[m_drop]

    col = np.clip(col, 0, 1) ** (1 / 1.9)
    save_rgba(col, alpha, os.path.join(OUT, "shelf.png"))
    return top, face, drop


# ═══════════════════════════════════════════════════════════════════════════
# 3. ROLLED SCROLLS
# ═══════════════════════════════════════════════════════════════════════════
PARCH = [
    (0.845, 0.790, 0.664), (0.872, 0.818, 0.690), (0.818, 0.760, 0.632),
    (0.858, 0.798, 0.658), (0.832, 0.782, 0.672), (0.884, 0.832, 0.712),
]
LS = norm(np.array([-0.46, -0.30, 0.83]))


def parchment_texture(h, w, seed, tint):
    """Flat parchment albedo — kept deliberately quiet: fibre, faint blotching,
    and a little age at the edges. Anything louder reads as marble, not paper."""
    fine = fbm((h, w), seed + 2, octaves=3, feature=7) * 0.013
    blot = fbm((h, w), seed + 3, octaves=3, feature=120) * 0.026
    # fibres running along the roll's axis
    fib = fbm((h, w), seed + 1, octaves=2, feature=2.6) * 0.014
    fib += np.repeat(fbm((h, 1), seed + 5, octaves=2, feature=90), w, axis=1) * 0.012
    v = 1 + fine + blot + fib
    rgb = np.array(tint)[None, None, :] * v[..., None]
    fox = np.clip(fbm((h, w), seed + 4, octaves=2, feature=26), 0, 1) ** 3
    rgb *= (1 - 0.055 * fox)[..., None]
    rgb[..., 2] *= 1 - 0.04 * fox
    return np.clip(rgb, 0, 1)


def scroll(path, r_css=26, h_css=176, seed=1, tint=0, ss=3, dpr=2):
    R = r_css * dpr * ss
    b = R * 0.33                       # how much of the top face we see
    Hb = h_css * dpr * ss              # body height
    W = int(round(2 * R))
    Ht = int(round(2 * b + Hb))
    Y, X = np.mgrid[0:Ht, 0:W].astype(np.float64)
    cx = W / 2.0
    rng = np.random.default_rng(seed)

    # slow silhouette wobble — hand-rolled paper isn't a true cylinder
    wob = fbm((Ht, 1), seed + 5, octaves=3, feature=Ht/3)[:, 0]
    Ry = R * (1 + 0.016 * wob)[:, None]

    nx = np.clip((X - cx) / Ry, -1, 1)
    inside = np.abs(X - cx) <= Ry
    nz = np.sqrt(np.clip(1 - nx * nx, 0, 1))
    theta = np.arcsin(nx)

    y_front_top = b + b * nz           # where the top face ends and the body begins
    y_back_top = b - b * nz
    Y0 = b + Hb
    y_bottom = Y0 + b * nz

    m_body = inside & (Y >= y_front_top) & (Y <= y_bottom)
    m_top = inside & (Y >= y_back_top) & (Y < y_front_top)

    # ── parchment albedo, mapped by arc length so it foreshortens correctly ──
    tw = int(R * 3.2)
    tex = parchment_texture(Ht, tw, seed * 31 + 3, PARCH[tint % len(PARCH)])
    u = np.clip(((theta / (math.pi / 2)) * 0.5 + 0.5) * (tw - 1), 0, tw - 1).astype(np.int32)
    vv = np.clip(Y, 0, Ht - 1).astype(np.int32)
    albedo = tex[vv, u]

    # ── creases from rolling: near-vertical, so noise varies with θ not with y ──
    cr = np.repeat(fbm((1, tw), seed + 7, octaves=3, feature=tw / 16.0), Ht, axis=0)
    cr = cr * 0.017 + fbm((Ht, tw), seed + 8, octaves=2, feature=tw / 5.0) * 0.004
    crease = cr[vv, u]
    nxc = np.clip(nx + crease, -1, 1)
    nzc = np.sqrt(np.clip(1 - nxc * nxc, 0, 1))
    diff = np.clip(nxc * LS[0] + nzc * LS[2], 0, 1)
    rim = (1 - nz) ** 3 * 0.13
    shade = 0.27 + 0.76 * diff + rim

    # ── the free edge of the sheet: a hairline, a lit lip, a cast shadow ──
    th_e = -0.62 + 0.012 * fbm((Ht, 1), seed + 9, octaves=2, feature=Ht / 3)[:, 0]
    x_e = cx + Ry[:, 0][:, None] * np.sin(th_e)[:, None]
    d = X - x_e
    thick = max(R * 0.013, 1.4)
    shade *= 1 - 0.26 * np.exp(-np.clip(d - thick, 0, None) / (R * 0.075))   # shadow
    shade *= 1 - 0.42 * np.exp(-(d ** 2) / (2 * (thick * 0.5) ** 2))          # hairline
    shade += 0.24 * np.exp(-((d + thick * 1.4) ** 2) / (2 * (thick * 0.6) ** 2))  # lit lip

    # a couple of fainter layer edges further round
    for k, off in enumerate((0.62, 1.15)):
        dk = X - (cx + Ry[:, 0][:, None] * np.sin(th_e + off)[:, None])
        shade *= 1 - 0.07 / (k + 1) * np.exp(-(dk ** 2) / (2 * (thick * 0.7) ** 2))

    # less light reaches the foot of the scroll
    shade *= 1 - 0.34 * smooth(Y0 - R * 2.4, Y0 + b, Y)
    shade *= 1 - 0.14 * smooth(b * 2 + R * 1.1, b * 2, Y)   # shade just under the rim

    body = albedo * shade[..., None] * np.array([1.0, 0.972, 0.918])

    # ── the top face: a spiral of paper edges ──
    Xc = (X - cx) / Ry
    Yc = (Y - b) / b
    rr_out = np.sqrt(np.clip(Xc * Xc + Yc * Yc, 0, None))     # 1.0 at the rim
    # the roll is wound off-centre and never perfectly round
    ex, ey = (rng.random() - 0.5) * 0.22, (rng.random() - 0.5) * 0.22
    Xs, Ys = Xc - ex, Yc - ey
    rr = np.sqrt(np.clip(Xs * Xs + Ys * Ys, 0, None))
    ang = np.arctan2(Ys, Xs)
    rr = rr * (1 + 0.05 * np.sin(2 * ang + seed) + 0.03 * np.sin(5 * ang - 1.1))
    turns = 9.0 + (seed % 4)
    # the outer end of the spiral is the sheet's free edge, on the body below
    phase = th_e[0] / (2 * math.pi)
    lam = (rr * turns - ang / (2 * math.pi) + phase) % 1.0
    lam_edge = np.minimum(lam, 1 - lam)
    groove = np.exp(-(lam_edge ** 2) / (2 * 0.055 ** 2))
    lip = np.exp(-((lam - 0.10) ** 2) / (2 * 0.055 ** 2))
    ramp = 0.88 + 0.20 * lam
    ao = 0.46 + 0.54 * np.clip(rr, 0, 1) ** 0.5
    core = smooth(0.0, 0.22, rr)
    tshade = 0.82 * ramp * ao * (1 - 0.42 * groove + 0.12 * lip) * (0.12 + 0.88 * core)
    tshade *= 1 + 0.09 * fbm((Ht, tw), seed + 13, octaves=3, feature=9)[vv, u]
    tshade *= 1 - 0.26 * smooth(0.55, 1.0, rr_out)         # rim rolls away from the light
    topcol = albedo * tshade[..., None] * np.array([1.0, 0.982, 0.944])

    col = np.where(m_body[..., None], body, 0.0)
    col = np.where(m_top[..., None], topcol, col)
    alpha = (m_body | m_top).astype(np.float64)

    col = np.clip(col, 0, 1) ** (1 / 1.9)
    col = downsample(col, ss)
    alpha = downsample(alpha, ss)
    save_rgba(col, alpha, path)


def rod(seed=5, tint=1, r_css=11.5, ss=3, dpr=2, strip_css=28):
    """A horizontal roll for the head and foot of an opened scroll."""
    R = r_css * dpr * ss
    H = int(round(2 * R))
    Wb = int(round(strip_css * dpr * ss))
    Y, X = np.mgrid[0:H, 0:Wb].astype(np.float64)
    cy = H / 2.0
    ny = np.clip((Y - cy) / R, -1, 1)
    nz = np.sqrt(np.clip(1 - ny * ny, 0, 1))
    Lr = norm(np.array([-0.22, -0.58, 0.78]))
    tw = int(R * 3.2)
    tex = parchment_texture(tw, Wb, seed * 17 + 1, PARCH[tint % len(PARCH)])
    v = np.clip(((np.arcsin(ny) / (math.pi / 2)) * 0.5 + 0.5) * (tw - 1), 0, tw - 1).astype(np.int32)
    uu = np.clip(X, 0, Wb - 1).astype(np.int32)
    albedo = tex[v, uu]
    crease = fbm((tw, Wb), seed + 3, octaves=3, feature=14)[v, uu] * 0.05
    nyc = np.clip(ny + crease, -1, 1)
    nzc = np.sqrt(np.clip(1 - nyc * nyc, 0, 1))
    diff = np.clip(nyc * Lr[1] + nzc * Lr[2], 0, 1)
    shade = 0.28 + 0.90 * diff + (1 - nz) ** 3 * 0.14
    col = np.clip(albedo * shade[..., None], 0, 1) ** (1 / 1.9)
    save_rgba(downsample(col, ss), downsample(np.ones((H, Wb)), ss),
              os.path.join(OUT, "rod-body.png"))

    # end sliver: a thin ellipse of the spiral, seen almost edge-on
    Wc = int(round(9 * dpr * ss))
    Y, X = np.mgrid[0:H, 0:Wc].astype(np.float64)
    a = Wc - 1.0
    Xc = (X - (Wc - a)) / a
    Yc = (Y - cy) / R
    rr = np.sqrt(np.clip(Xc * Xc + Yc * Yc, 0, None))
    m = rr <= 1
    ang = np.arctan2(Yc, np.clip(Xc, -1, 1))
    lam = (rr * 7.5 - ang / (2 * math.pi)) % 1.0
    groove = np.exp(-(np.minimum(lam, 1 - lam) ** 2) / (2 * 0.09 ** 2))
    sh = 0.92 * (0.86 + 0.26 * lam) * (0.50 + 0.50 * rr ** 0.5) * (1 - 0.45 * groove)
    sh *= 0.20 + 0.80 * smooth(0.0, 0.2, rr)
    base = np.array(PARCH[tint % len(PARCH)])
    col = np.clip(base[None, None, :] * sh[..., None], 0, 1) ** (1 / 1.9)
    save_rgba(downsample(col, ss), downsample(m.astype(float), ss),
              os.path.join(OUT, "rod-end.png"))


def sheet_paper(size=512, seed=77):
    """Tileable writing-surface texture for the unrolled sheet."""
    print("paper…")
    rgb = parchment_texture(size, size, seed, (0.955, 0.930, 0.862))
    fib = fbm((size, size), seed + 31, octaves=3, feature=3.0)
    rgb *= (1 + 0.035 * fib)[..., None]
    save_rgb(np.clip(rgb, 0, 1) ** (1 / 1.9), os.path.join(OUT, "paper.jpg"), quality=88)


if __name__ == "__main__":
    cobblestone()
    shelf()
    print("scrolls…")
    specs = [(24, 168), (27, 186), (25, 158), (28, 176), (23, 196), (26, 150),
             (27, 164), (24, 190)]
    for i, (r, h) in enumerate(specs):
        scroll(os.path.join(OUT, f"scroll-{i}.png"), r_css=r, h_css=h, seed=i * 13 + 3, tint=i)
    print("rods…")
    rod()
    sheet_paper()
    print("done.")
