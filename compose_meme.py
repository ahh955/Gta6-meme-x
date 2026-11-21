#!/usr/bin/env python3
"""Compose the GTA 6 meme v4: "WANTED: GRAND THEFT AUTO VI - FINES DUE".

A wanted poster whose middle is a CHARGES + FINES table. Every charge is
priced; the prices sum EXACTLY to TOTAL FINES $2,026 (the year the game
finally shows up). Deterministic: no randomness, no timestamps, fixed fonts.
Run: python3 compose_meme.py  ->  meme.png (1024x1024).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette ---
PARCHMENT = (246, 239, 219)
PARCHMENT_DARK = (232, 222, 190)
NAVY = (28, 36, 64)
NAVY_LIGHT = (52, 64, 110)
GOLD = (217, 165, 33)
GOLD_LIGHT = (240, 200, 80)
MAGENTA = (214, 51, 132)
RED = (178, 34, 34)
INK = (35, 35, 35)
GRAY = (110, 105, 90)
WHITE = (255, 255, 255)
MANILA = (233, 214, 160)
MANILA_DARK = (205, 180, 120)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --- the fines table (prices MUST sum to exactly 2026) ---
CHARGES = [
    ("GRAND THEFT OF 13 YEARS", 1300),      # $100 a year
    ("4,811 DAYS ON THE RUN", 481),         # 10c a day
    ("214 GB OF STOLEN STORAGE", 214),      # $1 a gigabyte
    ("TWO COUNTS OF DELAY", 26),            # $13 each
    ("FIVE FAKE SICK DAYS", 5),             # $1 a day
    ("1,337 REWATCHES (SELF-INFLICTED)", 0),
]
TOTAL = 2026
assert sum(p for _, p in CHARGES) == TOTAL, "fines do not sum to total"

BAND_LINES = [
    "REWARD: $79.99 \u2014 CLAIMED IN FULL BY MY AI AGENT.",
    "It earned real bounty cash on make.fun while the game was on the run.",
    "Your agent could too.",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, start, max_w, min_size=10):
    """Largest font size at which text fits max_w. Deterministic."""
    size = start
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def star_points(cx, cy, r_out, r_in, points=5, rot=-90.0):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_star(draw, cx, cy, r_out, r_in, fill, outline=None, width=2):
    pts = star_points(cx, cy, r_out, r_in)
    draw.polygon(pts, fill=fill, outline=outline, width=width)


def dotted_leader(draw, x0, x1, y, color=GRAY, gap=9, r=1.6):
    x = x0
    while x < x1:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        x += gap


def draw_ghost(base, cx, top, width, height):
    """A flat white deputy ghost with sheriff star, gold coin, and a
    manila CASE CLOSED file. Drawn on its own layer for a soft shadow."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, x1 = cx - width // 2, cx + width // 2
    y0, y1 = top, top + height
    dome_r = width // 2
    # soft shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([x0 + 8, y0 + 10, x1 + 8, y0 + 10 + width], fill=(180, 170, 140, 255))
    sd.rectangle([x0 + 8, y0 + 10 + dome_r, x1 + 8, y1 + 10], fill=(180, 170, 140, 255))
    base.alpha_composite(shadow)

    # body: dome + straight sides
    d.pieslice([x0, y0, x1, y0 + width], start=180, end=360, fill=(255, 255, 255, 255))
    d.rectangle([x0, y0 + dome_r, x1, y1], fill=(255, 255, 255, 255))
    # wavy bottom: three scallop cutouts (painted in parchment, the backdrop)
    scallop_r = width // 6
    for i in range(3):
        sx = x0 + scallop_r + i * 2 * scallop_r
        d.ellipse([sx - scallop_r, y1 - scallop_r, sx + scallop_r, y1 + scallop_r],
                  fill=(*PARCHMENT, 255))
    # eyes
    eye_w, eye_h = 16, 26
    for ex in (cx - 34, cx + 34):
        d.ellipse([ex - eye_w // 2, y0 + 78 - eye_h // 2,
                   ex + eye_w // 2, y0 + 78 + eye_h // 2], fill=(30, 30, 30, 255))
    # smile
    d.arc([cx - 22, y0 + 108, cx + 22, y0 + 140], start=15, end=165,
          fill=(30, 30, 30, 255), width=4)
    # sheriff star on the chest
    draw_star(d, cx, y0 + 185, 26, 11, fill=(*GOLD, 255), outline=(*NAVY, 255), width=2)
    base.alpha_composite(layer)

    # gold coin in the right hand
    coin = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(coin)
    ccx, ccy, cr = x1 - 6, y0 + 150, 30
    cd.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(*GOLD, 255),
               outline=(*NAVY, 255), width=3)
    cf = font(SANS_BOLD, 34)
    cd.text((ccx, ccy), "$", font=cf, fill=(*NAVY, 255), anchor="mm")
    base.alpha_composite(coin)

    # CASE CLOSED file in the left hand (slightly rotated manila folder)
    fw, fh = 150, 96
    fimg = Image.new("RGBA", (fw + 40, fh + 40), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fimg)
    fd.rounded_rectangle([20, 20, 20 + fw, 20 + fh], radius=6,
                         fill=(*MANILA, 255), outline=(*MANILA_DARK, 255), width=3)
    fd.rectangle([20, 20, 20 + 52, 20 + 16], fill=(*MANILA_DARK, 255))
    ff = font(SANS_BOLD, 19)
    fd.text((20 + fw // 2, 20 + 34), "CASE", font=ff, fill=(*RED, 255), anchor="mm")
    fd.text((20 + fw // 2, 20 + 58), "CLOSED", font=ff, fill=(*RED, 255), anchor="mm")
    fimg = fimg.rotate(-9, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(fimg, (x0 - 25, y0 + 180))


def draw_stamp(base, cx, cy, w=300, h=96, angle=-12):
    """Red CAUGHT! stamp, fully clear of every other element."""
    layer = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([30, 30, 30 + w, 30 + h], radius=10,
                        outline=(*RED, 255), width=5)
    d.rounded_rectangle([38, 38, 30 + w - 8, 30 + h - 8], radius=7,
                        outline=(*RED, 255), width=2)
    sf = font(SANS_BOLD, 52)
    d.text((30 + w // 2, 30 + h // 2), "CAUGHT!", font=sf, fill=(*RED, 255),
           anchor="mm")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(layer, (cx - layer.width // 2, cy - layer.height // 2))


def main():
    img = Image.new("RGBA", (W, H), (*PARCHMENT, 255))
    d = ImageDraw.Draw(img)

    # --- frame ---
    d.rectangle([14, 14, W - 15, H - 15], outline=NAVY, width=4)
    d.rectangle([24, 24, W - 25, H - 25], outline=NAVY, width=2)

    # --- header band: WANTED + 5 gold stars ---
    d.rectangle([24, 24, W - 25, 148], fill=NAVY)
    wf = fit(d, "WANTED", SERIF_BOLD, 96, 420)
    d.text((W // 2, 84), "WANTED", font=wf, fill=GOLD_LIGHT, anchor="mm")
    cf = font(SANS_BOLD, 17)
    d.text((W - 44, 44), "CASE No. 001337", font=cf, fill=GOLD, anchor="rm")
    d.text((44, 44), "LEONIDA COUNTY", font=cf, fill=GOLD, anchor="lm")
    for i in range(5):
        draw_star(d, W // 2 - 120 + i * 60, 132, 13, 5.5, fill=GOLD)

    # --- name + format-mined sublines ---
    nf = fit(d, "GRAND THEFT AUTO VI", SERIF_BOLD, 52, 940)
    d.text((W // 2, 186), "GRAND THEFT AUTO VI", font=nf, fill=NAVY, anchor="mm")
    s1 = "ARMED (WITH TRAILERS) AND DANGEROUS (TO PRODUCTIVITY)"
    f1 = fit(d, s1, SANS_BOLD, 26, 940)
    d.text((W // 2, 226), s1, font=f1, fill=RED, anchor="mm")
    s2 = "DO NOT APPROACH \u2014 IT WILL DELAY AGAIN"
    f2 = fit(d, s2, SANS_BOLD, 24, 940)
    d.text((W // 2, 254), s2, font=f2, fill=NAVY, anchor="mm")

    # --- CHARGES & FINES table (left) ---
    tx0, tx1 = 44, 640
    ty = 282
    d.rectangle([tx0, ty, tx1, ty + 44], fill=NAVY)
    hf = font(SANS_BOLD, 27)
    d.text((tx0 + 16, ty + 22), "CHARGES & FINES", font=hf, fill=WHITE, anchor="lm")
    d.text((tx1 - 16, ty + 22), "FINE", font=hf, fill=GOLD_LIGHT, anchor="rm")

    row_h = 40
    rf = font(SANS_BOLD, 23)
    pf = font(SANS_BOLD, 25)
    y = ty + 44
    for i, (charge, price) in enumerate(CHARGES):
        ry = y + i * row_h
        if i % 2 == 1:
            d.rectangle([tx0, ry, tx1, ry + row_h], fill=PARCHMENT_DARK)
        d.text((tx0 + 16, ry + row_h // 2), charge, font=rf, fill=INK, anchor="lm")
        price_txt = "$%s" % ("0.00" if price == 0 else f"{price:,}")
        d.text((tx1 - 16, ry + row_h // 2), price_txt, font=pf, fill=NAVY, anchor="rm")
        # dotted leader between charge text and price
        cx_end = tx0 + 16 + text_w(d, charge, rf) + 10
        px_start = tx1 - 16 - text_w(d, price_txt, pf) - 10
        if px_start - cx_end > 20:
            dotted_leader(d, cx_end, px_start, ry + row_h // 2)
        d.line([tx0, ry + row_h, tx1, ry + row_h], fill=GRAY, width=1)

    ty_total = y + len(CHARGES) * row_h + 8
    d.line([tx0, ty_total, tx1, ty_total], fill=NAVY, width=3)
    d.line([tx0, ty_total + 5, tx1, ty_total + 5], fill=NAVY, width=1)
    tf = font(SERIF_BOLD, 33)
    d.text((tx0 + 16, ty_total + 34), "TOTAL FINES", font=tf, fill=NAVY, anchor="lm")
    vf = font(SERIF_BOLD, 44)
    d.text((tx1 - 16, ty_total + 34), "$2,026", font=vf, fill=RED, anchor="rm")
    sf2 = font(SANS_BOLD, 21)
    d.text(((tx0 + tx1) // 2, ty_total + 76), "THE YEAR IT FINALLY SHOWED UP.",
           font=sf2, fill=NAVY, anchor="mm")

    # --- ghost deputy (right) ---
    draw_ghost(img, 822, 282, 250, 285)

    # --- CAUGHT! stamp: own clear space under the ghost ---
    draw_stamp(img, 822, 616, w=285)

    # --- file facts strip ---
    fy = 700
    d.line([44, fy - 12, W - 45, fy - 12], fill=NAVY, width=2)
    ff1 = fit(d, "LAST SEEN: LOS SANTOS, 2013  \u2022  CAPTURED: VICE CITY  \u2022  ON THE RUN: 4,811 DAYS",
              SANS_BOLD, 21, 940)
    d.text((W // 2, fy + 8), "LAST SEEN: LOS SANTOS, 2013  \u2022  CAPTURED: VICE CITY  \u2022  ON THE RUN: 4,811 DAYS",
           font=ff1, fill=NAVY, anchor="mm")
    ff2 = fit(d, "ACCOMPLICES: JASON & LUCIA (IN CUSTODY)  \u2022  GETAWAY DRIVER: ONE ALLIGATOR (STILL AT LARGE)",
              SANS_BOLD, 21, 940)
    d.text((W // 2, fy + 36), "ACCOMPLICES: JASON & LUCIA (IN CUSTODY)  \u2022  GETAWAY DRIVER: ONE ALLIGATOR (STILL AT LARGE)",
           font=ff2, fill=NAVY, anchor="mm")

    # --- reward band (verbatim v3 text) ---
    band_y0, band_y1 = 762, 878
    d.rectangle([24, band_y0, W - 25, band_y1], fill=MAGENTA)
    bf1 = fit(d, BAND_LINES[0], SANS_BOLD, 31, 940)
    d.text((44, band_y0 + 24), BAND_LINES[0], font=bf1, fill=WHITE, anchor="lm")
    bf2 = fit(d, BAND_LINES[1], SANS_BOLD, 24, 940)
    d.text((44, band_y0 + 62), BAND_LINES[1], font=bf2, fill=WHITE, anchor="lm")
    bf3 = font(SANS_BOLD, 24)
    d.text((44, band_y0 + 94), BAND_LINES[2], font=bf3, fill=WHITE, anchor="lm")
    # white pill with magenta make.fun, beside short line 3 (no overlap)
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([W - 250, band_y0 + 80, W - 44, band_y0 + 112], radius=16,
                         fill=WHITE)
    pf2 = font(SANS_BOLD, 26)
    pd.text((W - 147, band_y0 + 96), "make.fun", font=pf2, fill=MAGENTA, anchor="mm")
    img.alpha_composite(pill)

    # --- closer ---
    c1 = "VERDICT: GUILTY."
    c2 = "SENTENCE: 13 MORE YEARS \u2014 PLAYING IT."
    cf1 = fit(d, c1, SERIF_BOLD, 36, 940)
    d.text((W // 2, 912), c1, font=cf1, fill=NAVY, anchor="mm")
    cf2 = fit(d, c2, SERIF_BOLD, 34, 940)
    d.text((W // 2, 954), c2, font=cf2, fill=NAVY, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")
    # Quantize to a 256-color palette: flat vector art compresses far better
    # with no visible change (deterministic median-cut).
    img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
    print("fines sum: $%s (target $%s)" % (f"{sum(p for _, p in CHARGES):,}", f"{TOTAL:,}"))


if __name__ == "__main__":
    main()
