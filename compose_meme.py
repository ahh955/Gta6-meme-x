#!/usr/bin/env python3
"""Compose the v7 meme for make.fun gta6-meme-x-01: a Leonida tax assessment.

Concept: LEONIDA DEPARTMENT OF REVENUE, NOTICE OF ASSESSMENT, FORM 13-VI.
The 13-year GTA 6 wait is taxed, line by line, and the total due is $1,337.00
(1,000 + 200 + 100 + 25 + 12 = 1,337 exactly). The refund is one copy of the
game itself. A large make.fun ghost pays the bill in the magenta band.

All dates and counts are real and verified:
  GTA V launched 17 Sep 2013; GTA VI launched 19 Nov 2026 -> 4,811 days.
  Rockstar confirmed the next GTA in development on 4 Feb 2022; that is
  1,749 days before the 19 Nov 2026 launch. Two delays: Fall 2025, May 2026.

Deterministic: same input -> byte-identical PNG (no timestamps, no randomness).
Run: python3 compose_meme.py  (writes meme.png next to this script)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")

W, H = 1024, 1024
MARGIN = 26          # gradient frame thickness around the paper
PAPER_R = 28         # paper corner radius

CREAM = (255, 249, 230)
NAVY = (26, 26, 46)
NAVY_SOFT = (58, 58, 86)
GREY = (122, 122, 138)
GOLD = (232, 185, 60)
GOLD_STRIP = (245, 215, 110)
MAGENTA = (216, 17, 89)
MAGENTA_DARK = (194, 24, 91)
RED = (198, 40, 40)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

FONT_DIR = "/usr/share/fonts/truetype"
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")
MONO_BOLD = os.path.join(FONT_DIR, "dejavu", "DejaVuSansMono-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, max_w, start, floor=10):
    """Largest font size at which `text` fits in `max_w` pixels."""
    size = start
    while size > floor:
        f = font(path, size)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, floor)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def draw_tracked(draw, x, y, text, f, fill, tracking=4):
    """Draw text with extra letter spacing (for the gold sub-head)."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vertical_gradient(size, stops):
    """size (w, h); stops: list of (pos 0..1, rgb). Returns an RGB image."""
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = lerp(c0, c1, f)
                break
        else:
            col = stops[-1][1]
        for x in range(w):
            px[x, y] = col
    return img


def star_points(cx, cy, r_out, r_in, rotation=-90.0):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rotation + i * 36.0)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def sparkle_points(cx, cy, r):
    """A four-pointed sparkle (the make.fun ghost's eye shape)."""
    k = 0.26
    return [
        (cx, cy - r), (cx + r * k, cy - r * k),
        (cx + r, cy), (cx + r * k, cy + r * k),
        (cx, cy + r), (cx - r * k, cy + r * k),
        (cx - r, cy), (cx - r * k, cy - r * k),
    ]


def ghost_layer(w, h, outline=7):
    """The make.fun ghost: white body, thick black outline, sparkle eyes,
    one round hand holding a magenta coin with a white star."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Body silhouette as a polygon: dome on top, straight sides, 3 scallops.
    # The body sits left of centre so the coin in its hand fits the layer.
    cx, top = w * 0.40, 8
    half = w * 0.33
    side_bottom = h * 0.86
    pts = []
    dome_cy = top + half * 0.92
    for deg in range(180, 360, 3):
        a = math.radians(deg)
        pts.append((cx + half * math.cos(a), dome_cy + half * 0.92 * math.sin(a)))
    pts.append((cx + half, side_bottom))
    # Scalloped bottom: three upward arcs, traversed right to left.
    n_scallop = 3
    seg = (2 * half) / n_scallop
    depth = seg * 0.28
    for s in range(n_scallop):
        x_right = cx + half - s * seg
        for step in range(1, 31):
            t = step / 30.0
            x = x_right - t * seg
            y = side_bottom - depth * math.sin(math.pi * t)
            pts.append((x, y))
    pts.append((cx - half, dome_cy))
    # Outline: draw the silhouette in black, then a shrunken copy in white.
    d.polygon(pts, fill=(0, 0, 0, 255))
    inner = []
    ccx, ccy = cx, (top + side_bottom) / 2
    for (x, y) in pts:
        inner.append((ccx + (x - ccx) * 0.93, ccy + (y - ccy) * 0.94))
    d.polygon(inner, fill=(255, 255, 255, 255))
    # Sparkle eyes.
    eye_y = top + half * 0.72
    eye_dx = half * 0.38
    eye_r = half * 0.20
    d.polygon(sparkle_points(cx - eye_dx, eye_y, eye_r), fill=(0, 0, 0, 255))
    d.polygon(sparkle_points(cx + eye_dx, eye_y, eye_r), fill=(0, 0, 0, 255))
    # Round hand on the right side, holding the coin.
    hand_x, hand_y, hand_r = cx + half * 0.98, dome_cy + half * 0.95, half * 0.20
    d.ellipse([hand_x - hand_r - 4, hand_y - hand_r - 4,
               hand_x + hand_r + 4, hand_y + hand_r + 4], fill=(0, 0, 0, 255))
    d.ellipse([hand_x - hand_r, hand_y - hand_r,
               hand_x + hand_r, hand_y + hand_r], fill=(255, 255, 255, 255))
    # Magenta coin with a white star, overlapping the hand.
    coin_x, coin_y, coin_r = hand_x + hand_r * 1.7, hand_y - hand_r * 0.9, half * 0.30
    d.ellipse([coin_x - coin_r - 4, coin_y - coin_r - 4,
               coin_x + coin_r + 4, coin_y + coin_r + 4], fill=(255, 255, 255, 255))
    d.ellipse([coin_x - coin_r, coin_y - coin_r,
               coin_x + coin_r, coin_y + coin_r], fill=MAGENTA + (255,))
    d.polygon(star_points(coin_x, coin_y, coin_r * 0.72, coin_r * 0.30),
              fill=(255, 255, 255, 255))
    return layer


def stamp_layer(w, h, text, size):
    """A red rubber stamp: double border, bold text, slight rotation."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=14,
                        outline=RED + (255,), width=6)
    d.rounded_rectangle([14, 14, w - 15, h - 15], radius=10,
                        outline=RED + (255,), width=2)
    f = fit(SANS_BOLD, text, w - 44, size)
    tw = d.textlength(text, font=f)
    th = f.getbbox(text)[3] - f.getbbox(text)[1]
    d.text(((w - tw) / 2, (h - th) / 2 - 4), text, font=f, fill=RED + (255,))
    return layer.rotate(-9, expand=True, resample=Image.BICUBIC)


def dotted_leader(draw, x0, x1, y, color, gap=10, dot=3):
    x = x0
    while x < x1:
        draw.ellipse([x, y - dot // 2, x + dot, y + dot // 2], fill=color)
        x += gap


def main():
    # --- background: full-bleed purple -> magenta -> orange gradient ---
    img = vertical_gradient((W, H), [
        (0.0, (91, 42, 134)),
        (0.45, (194, 24, 91)),
        (1.0, (245, 124, 0)),
    ])
    d = ImageDraw.Draw(img)

    # --- cream paper ---
    d.rounded_rectangle([MARGIN, MARGIN, W - MARGIN - 1, H - MARGIN - 1],
                        radius=PAPER_R, fill=CREAM)
    px0, px1 = MARGIN, W - MARGIN  # paper x range

    # --- header band (dark navy, rounded top corners like the paper) ---
    band_h = 138
    d.rounded_rectangle([px0, MARGIN, px1 - 1, MARGIN + band_h],
                        radius=PAPER_R, fill=NAVY)
    d.rectangle([px0, MARGIN + band_h - PAPER_R, px1 - 1, MARGIN + band_h],
                fill=NAVY)
    f_title = fit(SANS_BOLD, "LEONIDA DEPARTMENT OF REVENUE", 640, 40)
    d.text((px0 + 30, MARGIN + 22), "LEONIDA DEPARTMENT OF REVENUE",
           font=f_title, fill=WHITE)
    f_sub = font(SANS_BOLD, 27)
    draw_tracked(d, px0 + 30, MARGIN + 76, "NOTICE OF ASSESSMENT", f_sub,
                 GOLD, tracking=5)
    f_form = font(SANS_BOLD, 29)
    f_year = font(MONO_BOLD, 21)
    t = "FORM 13-VI"
    d.text((px1 - 30 - text_w(d, t, f_form), MARGIN + 26), t,
           font=f_form, fill=WHITE)
    t2 = "TAX YEAR 2013-2026"
    d.text((px1 - 30 - text_w(d, t2, f_year), MARGIN + 66), t2,
           font=f_year, fill=(176, 176, 196))
    t3 = "VICE CITY  ·  LEONIDA"
    d.text((px1 - 30 - text_w(d, t3, f_year), MARGIN + 94), t3,
           font=f_year, fill=(176, 176, 196))

    # --- info block (left) + PAID IN FULL stamp (right) ---
    info_y = MARGIN + band_h + 22
    f_label = font(MONO_BOLD, 19)
    f_value = font(SANS_BOLD, 26)
    rows = [
        ("TAXPAYER", "PLAYER ONE"),
        ("FILED", "SEP 17, 2013"),
        ("ASSESSED", "NOV 19, 2026"),
        ("DAYS WAITING", "4,811"),
        ("DEPENDENTS", "JASON & LUCIA"),
    ]
    # Two pairs per row on the left; the stamp owns the right ~300 px.
    col_x = [px0 + 30, px0 + 330]
    row_h = 42
    for i, (label, value) in enumerate(rows):
        col = i % 2
        row = i // 2
        x = col_x[col]
        y = info_y + row * row_h
        if i == 4:  # dependents spans the second row's right side alone
            x = col_x[0]
            y = info_y + 2 * row_h
        d.text((x, y), label, font=f_label, fill=GREY)
        lw = text_w(d, label, f_label)
        d.text((x + lw + 12, y - 3), value, font=f_value, fill=NAVY)
    # Filling status line under the pairs.
    fy = info_y + 3 * row_h + 2
    f_status = font(SANS_BOLD, 22)
    d.text((px0 + 30, fy), "FILING STATUS:", font=f_label, fill=GREY)
    sw = text_w(d, "FILING STATUS:", f_label)
    d.text((px0 + 30 + sw + 12, fy - 2), "STILL WAITING",
           font=f_status, fill=RED)
    # Stamp, top-right, in clear space.
    stamp = stamp_layer(300, 132, "PAID IN FULL", 46)
    img.paste(stamp, (px1 - 30 - stamp.width + 18, info_y - 6), stamp)
    d = ImageDraw.Draw(img)

    # --- divider + itemised assessment ---
    table_top = fy + 44
    d.line([px0 + 30, table_top, px1 - 30, table_top], fill=NAVY, width=3)
    f_item = font(SANS, 27)
    f_price = font(SANS_BOLD, 27)
    items = [
        ("Patience, 13 years", "$1,000.00"),
        ('Delays x 2 ("Fall 2025", "May 2026")', "$200.00"),
        ("Download, 214 GB", "$100.00"),
        ("Sick days x 5", "$25.00"),
        ("Alligator removal", "$12.00"),
    ]
    y = table_top + 18
    for label, price in items:
        f_lab = fit(SANS, label, 640, 27)
        d.text((px0 + 30, y), label, font=f_lab, fill=NAVY)
        pw = text_w(d, price, f_price)
        d.text((px1 - 30 - pw, y), price, font=f_price, fill=NAVY)
        leader_x0 = px0 + 30 + text_w(d, label, f_lab) + 14
        leader_x1 = px1 - 30 - pw - 14
        dotted_leader(d, leader_x0, leader_x1, y + 16, (170, 170, 180))
        y += 48
    # Total row.
    d.line([px0 + 30, y + 2, px1 - 30, y + 2], fill=NAVY, width=3)
    f_total = font(SANS_BOLD, 40)
    f_amount = font(SANS_BOLD, 58)
    d.text((px0 + 30, y + 18), "TOTAL DUE", font=f_total, fill=NAVY)
    amt = "$1,337.00"
    d.text((px1 - 30 - text_w(d, amt, f_amount), y + 6), amt,
           font=f_amount, fill=NAVY)

    # --- refund strip (gold): the game itself is the refund ---
    strip_y = y + 84
    strip_h = 52
    d.rounded_rectangle([px0 + 30, strip_y, px1 - 30, strip_y + strip_h],
                        radius=12, fill=GOLD_STRIP)
    refund = "REFUND ISSUED: ONE (1) COPY OF GRAND THEFT AUTO VI."
    f_ref = fit(SANS_BOLD, refund, px1 - px0 - 100, 28)
    rw = text_w(d, refund, f_ref)
    d.text(((W - rw) / 2, strip_y + 12), refund, font=f_ref, fill=NAVY)

    # --- footer micro-line (announcement date, verified) ---
    foot_y = strip_y + strip_h + 14
    f_foot = font(MONO_BOLD, 15)
    foot = "GTA VI ANNOUNCED FEB 4, 2022  ·  1,749 DAYS BEFORE LAUNCH  ·  FORM 13-VI  ·  PAGE 1 OF 1"
    fw = text_w(d, foot, f_foot)
    d.text(((W - fw) / 2, foot_y), foot, font=f_foot, fill=GREY)

    # --- magenta band: LARGE ghost + the make.fun pitch ---
    band_y = foot_y + 24
    band_bottom = H - MARGIN
    d.rounded_rectangle([px0, band_y, px1 - 1, band_bottom],
                        radius=PAPER_R, fill=MAGENTA)
    d.rectangle([px0, band_y, px1 - 1, band_y + PAPER_R], fill=MAGENTA)
    band_h2 = band_bottom - band_y
    ghost = ghost_layer(250, 190)
    gy = band_y + (band_h2 - ghost.height) // 2 + 4
    img.paste(ghost, (px0 + 30, gy), ghost)
    d = ImageDraw.Draw(img)
    tx = px0 + 310
    f_paid = fit(SANS_BOLD, "PAID BY MY AI AGENT", px1 - tx - 30, 46)
    d.text((tx, band_y + 16), "PAID BY MY AI AGENT", font=f_paid, fill=WHITE)
    f_earn = font(SANS, 28)
    d.text((tx + 2, band_y + 70), "with real money it earned on",
           font=f_earn, fill=WHITE)
    # make.fun pill.
    pill_y = band_y + 108
    pill_w, pill_h = 248, 50
    d.rounded_rectangle([tx, pill_y, tx + pill_w, pill_y + pill_h],
                        radius=25, fill=WHITE)
    f_pill = font(SANS_BOLD, 34)
    pill_t = "make.fun"
    pw2 = text_w(d, pill_t, f_pill)
    d.text((tx + (pill_w - pw2) / 2, pill_y + 7), pill_t,
           font=f_pill, fill=MAGENTA_DARK)

    # Save as a 256-colour palette PNG: flat vector art compresses to the
    # 29-60 KB range the winners sit in (the RGB render is ~138 KB, mostly
    # the smooth gradient frame). Palette conversion is deterministic.
    img.convert("P", palette=Image.ADAPTIVE, colors=256).save(
        OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
