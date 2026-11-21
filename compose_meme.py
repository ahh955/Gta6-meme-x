#!/usr/bin/env python3
"""Procedural WANTED-poster meme for the GTA 6 meme bounty (v3).

Flat vector shapes + DejaVu text only, no network, no copied assets.
Deterministic: same input always produces the same PNG bytes.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 235, 203)
INK = (36, 20, 7)
FRAME = (46, 26, 12)
RED = (179, 32, 44)
GOLD = (233, 163, 25)
GOLD_EDGE = (138, 90, 0)
MAGENTA = (230, 0, 122)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_out, r_in, n=5, rot_deg=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot_deg + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """Four-pointed sparkle (star with concave sides)."""
    k = 0.16 * r
    return [
        (cx, cy - r), (cx + k, cy - k),
        (cx + r, cy), (cx + k, cy + k),
        (cx, cy + r), (cx - k, cy + k),
        (cx - r, cy), (cx - k, cy - k),
    ]


def draw_star(draw, cx, cy, r_out, r_in, fill, outline=None, width=1):
    draw.polygon(star_points(cx, cy, r_out, r_in), fill=fill,
                 outline=outline, width=width)


def text_center(draw, cx, y, s, fnt, fill):
    box = draw.textbbox((0, 0), s, font=fnt)
    draw.text((cx - (box[0] + box[2]) / 2, y), s, font=fnt, fill=fill)


def text_spaced_center(draw, cx, y, s, fnt, fill, tracking):
    """Draw text with extra letter spacing, centered on cx."""
    widths = []
    total = 0
    for ch in s:
        b = draw.textbbox((0, 0), ch, font=fnt)
        w = b[2] - b[0]
        widths.append((ch, b, w))
        total += w
    total += tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, b, w in widths:
        draw.text((x - b[0], y), ch, font=fnt, fill=fill)
        x += w + tracking


def ghost(draw):
    """The make.fun ghost deputy, drawn from scratch: white ghost, thick
    black outline, four-pointed sparkle eyes, round hand, magenta coin
    with a white star, gold sheriff badge on its chest."""
    cx, dome_cy, r = 200, 430, 130
    # Body outline: dome + straight sides + three rounded bottom lobes.
    pts = []
    for deg in range(180, 360, 2):  # top semicircle, left -> right
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), dome_cy + r * math.sin(a)))
    pts.append((cx + r, 600))
    # Bottom lobes, right -> left, each a downward semicircle.
    lobe_r = (2 * r) / 6.0
    for i in range(3):
        lc = cx + r - lobe_r - i * 2 * lobe_r
        for deg in range(0, 181, 6):
            a = math.radians(deg)
            pts.append((lc + lobe_r * math.cos(a), 600 + lobe_r * math.sin(a)))
    pts.append((cx - r, dome_cy))
    draw.polygon(pts, fill=WHITE, outline=BLACK, width=8)

    # Sparkle eyes.
    draw.polygon(sparkle_points(155, 400, 24), fill=BLACK)
    draw.polygon(sparkle_points(245, 400, 24), fill=BLACK)
    # Small open mouth.
    draw.ellipse((188, 448, 212, 472), fill=BLACK)
    # Gold sheriff star badge on the chest.
    draw_star(draw, 200, 545, 34, 14, fill=GOLD, outline=BLACK, width=4)
    draw.ellipse((194, 539, 206, 551), fill=WHITE, outline=BLACK, width=2)

    # Left waving hand: round white hand with black outline.
    draw.ellipse((42, 452, 80, 490), fill=WHITE, outline=BLACK, width=5)
    # Right hand holding the coin up.
    draw.ellipse((330, 436, 370, 476), fill=WHITE, outline=BLACK, width=5)
    # Magenta coin with a white star.
    draw.ellipse((342, 370, 420, 448), fill=MAGENTA, outline=BLACK, width=5)
    draw_star(draw, 381, 409, 24, 10, fill=WHITE)


def stamp(base):
    """Rotated red CAUGHT! stamp, pasted over the ghost's lower edge
    (no text anywhere near it)."""
    layer = Image.new("RGBA", (300, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((4, 4, 295, 115), outline=RED + (255,), width=5)
    d.rectangle((14, 14, 285, 105), outline=RED + (255,), width=2)
    f = font(F_SANS_B, 54)
    text_center(d, 150, 26, "CAUGHT!", f, RED + (255,))
    layer = layer.rotate(16, expand=True, resample=Image.BICUBIC)
    base.paste(layer, (110, 618), layer)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Frame: thick outer border + thin inner rule.
    d.rectangle((0, 0, W - 1, H - 1), outline=FRAME, width=18)
    d.rectangle((34, 34, W - 35, H - 35), outline=FRAME, width=3)

    # Headline.
    text_spaced_center(d, W // 2, 48, "WANTED", font(F_SERIF_B, 104), INK, 14)
    text_center(d, W // 2, 168, "GRAND THEFT AUTO VI",
                font(F_SANS_B, 40), INK)
    # Five gold stars.
    for i in range(5):
        draw_star(d, 392 + i * 60, 248, 26, 11,
                  fill=GOLD, outline=GOLD_EDGE, width=3)
    d.line((60, 292, 964, 292), fill=INK, width=3)

    # Deputy ghost, left.
    ghost(d)

    # Case file, right.
    x = 440
    f_label = font(F_SANS_B, 24)
    f_value = font(F_SANS_B, 31)
    f_big = font(F_SANS_B, 44)
    d.text((x, 308), "LAST SEEN", font=f_label, fill=RED)
    d.text((x, 336), "LOS SANTOS \u00b7 17 SEPT 2013", font=f_value, fill=INK)
    d.text((x, 384), "CAPTURED", font=f_label, fill=RED)
    d.text((x, 412), "VICE CITY \u00b7 19 NOV 2026", font=f_value, fill=INK)
    d.text((x, 460), "ON THE RUN", font=f_label, fill=RED)
    d.text((x, 488), "4,811 DAYS", font=f_big, fill=RED)
    d.line((x, 552, 964, 552), fill=INK, width=2)
    d.text((x, 564), "CHARGES", font=font(F_SANS_B, 27), fill=INK)
    charges = [
        "13 YEARS OF TOTAL SILENCE",
        "TWO TRAILERS, ZERO RELEASES",
        "BREAKING THE INTERNET \u2014 TWICE",
        "4,811 DAYS OF MAKING US WAIT",
        "LEAKING NOTHING SINCE 2013",
    ]
    f_charge = font(F_SANS_B, 24)
    for i, c in enumerate(charges):
        d.text((x, 598 + i * 27), "\u2022  " + c, font=f_charge, fill=INK)

    stamp(img)
    d = ImageDraw.Draw(img)  # refresh after paste

    # Magenta reward band: the full make.fun pitch, exact spec text
    # from the top-10 study (FINDINGS.md) + make.fun pill.
    d.rectangle((18, 740, 1005, 868), fill=MAGENTA)
    text_center(d, W // 2, 748, "REWARD: $79.99 \u2014 CLAIMED IN FULL BY MY AI AGENT.",
                font(F_SANS_B, 30), WHITE)
    text_center(d, W // 2, 788,
                "It earned real bounty cash on make.fun while the game was on the run.",
                font(F_SANS, 22), WHITE)
    # Closing line + make.fun pill, centered as one group.
    f_close = font(F_SANS_B, 24)
    close = "Your agent could too."
    f_pill = font(F_SANS_B, 22)
    pill_text = "make.fun"
    cb = d.textbbox((0, 0), close, font=f_close)
    pb = d.textbbox((0, 0), pill_text, font=f_pill)
    gap = 14
    pill_pad_x = 16
    pill_w = (pb[2] - pb[0]) + 2 * pill_pad_x
    pill_h = 30
    total = (cb[2] - cb[0]) + gap + pill_w
    x0 = W // 2 - total // 2
    y3 = 820
    d.text((x0 - cb[0], y3), close, font=f_close, fill=WHITE)
    px = x0 + (cb[2] - cb[0]) + gap
    pill_top = y3 + 2
    d.rounded_rectangle((px, pill_top, px + pill_w, pill_top + pill_h),
                        radius=pill_h // 2, fill=WHITE)
    d.text((px + pill_pad_x - pb[0],
            pill_top + (pill_h - (pb[3] - pb[1])) // 2 - pb[1]),
           pill_text, font=f_pill, fill=MAGENTA)

    # Footer verdict, two lines.
    text_center(d, W // 2, 878, "WANTED FOR 13 YEARS. CAUGHT IN ONE NIGHT.",
                font(F_SANS_B, 30), INK)
    text_center(d, W // 2, 918, "VERDICT: WORTH EVERY DAY.",
                font(F_SANS_B, 30), RED)

    # Palette-quantize: the art is flat colors, so 256 colors keeps it
    # crisp while shrinking the file well under the 60 KB target.
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(
        "meme.png", optimize=True
    )


if __name__ == "__main__":
    main()
