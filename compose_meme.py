#!/usr/bin/env python3
"""Compose the GTA 6 meme v6: "BIRTH CERTIFICATE - 13 YEARS OF LABOR".

Vice City General Hospital delivers Grand Theft Auto VI after the longest
labor in hospital history: 13 years. The make.fun ghost is Dr. Ghost, the
delivering doctor, presenting the newborn (a swaddled bundle stamped VI).
The hospital bill itemizes the wait and sums to $2,013 -- the year this
all started (Sep 17, 2013).

Deterministic: no randomness, no timestamps, fixed fonts.
Run: python3 compose_meme.py  ->  meme.png (1024x1024).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette ---
PAPER = (248, 243, 228)
PAPER_DARK = (236, 228, 202)
TEAL = (18, 110, 105)
TEAL_DARK = (13, 84, 80)
TEAL_LIGHT = (178, 226, 220)
NAVY = (28, 36, 64)
GOLD = (217, 165, 33)
MAGENTA = (214, 51, 132)
RED = (178, 34, 34)
INK = (35, 35, 35)
GRAY = (110, 105, 90)
WHITE = (255, 255, 255)
BLANKET = (245, 235, 200)
PEACH = (244, 200, 170)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --- the hospital bill: prices sum to $2,013, the year it all started ---
BILL = [
    ("LABOR \u2014 13 YEARS", 1300),
    ("DELIVERY ROOM \u2014 VICE CITY GENERAL", 481),
    ("INCUBATOR \u2014 214 GB", 214),
    ("EPIDURAL \u00d72 \u2014 FALL 2025, MAY 2026", 13),
    ("SICK NOTES \u00d75 \u2014 DOCTOR APPROVED", 5),
    ("FIRST CRY \u2014 TRAILER 2, 1,337 REWATCHES", 0),
]
TOTAL_DUE = sum(p for _, p in BILL)
assert TOTAL_DUE == 2013, "bill does not total $2,013"

BAND_LINES = [
    "PAID IN FULL BY MY AI AGENT.",
    "It earned real bounty cash on make.fun while we waited in the delivery room.",
    "Your agent could too.",
]

WARNINGS = []


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, start, max_w, min_size=10, label=""):
    """Largest font size at which text fits max_w. Deterministic.
    Records a warning if even min_size does not fit."""
    size = start
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    f = font(path, min_size)
    if draw.textlength(text, font=f) > max_w:
        WARNINGS.append("TRUNCATION RISK %s: %r wider than %d px" % (label, text, max_w))
    return f


def sparkle(d, cx, cy, r, fill):
    """Four-point sparkle star (the ghost's eyes)."""
    pts = [
        (cx, cy - r),
        (cx + r * 0.28, cy - r * 0.28),
        (cx + r, cy),
        (cx + r * 0.28, cy + r * 0.28),
        (cx, cy + r),
        (cx - r * 0.28, cy + r * 0.28),
        (cx - r, cy),
        (cx - r * 0.28, cy - r * 0.28),
    ]
    d.polygon(pts, fill=fill)


def star5(d, cx, cy, r, fill):
    """Five-point star."""
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def draw_doctor_ghost(base, cx, top, width, height):
    """Dr. Ghost: the delivering doctor. White ghost in a teal surgical
    cap (white cross), sparkle eyes, a smile, holding the newborn bundle
    (swaddled, stamped VI) at chest height. The face stays visible: no
    mask, no stethoscope -- the cap and the bundle say "doctor". Own layer."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, x1 = cx - width // 2, cx + width // 2
    y0, y1 = top, top + height
    dome_r = width // 2

    # soft shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.ellipse([x0 + 6, y0 + 8, x1 + 6, y0 + 8 + width], fill=(200, 190, 160, 255))
    sd.rectangle([x0 + 6, y0 + 8 + dome_r, x1 + 6, y1 + 8], fill=(200, 190, 160, 255))
    base.alpha_composite(sh)

    # body: dome + straight sides
    d.pieslice([x0, y0, x1, y0 + width], start=180, end=360, fill=(255, 255, 255, 255))
    d.rectangle([x0, y0 + dome_r, x1, y1], fill=(255, 255, 255, 255))
    # wavy bottom: three scallop cutouts in the paper colour
    sr = width // 6
    for i in range(3):
        sx = x0 + sr + i * 2 * sr
        d.ellipse([sx - sr, y1 - sr, sx + sr, y1 + sr], fill=(*PAPER, 255))
    # outline the body so it reads on the paper
    d.arc([x0, y0, x1, y0 + width], start=180, end=360, fill=(120, 115, 100, 255), width=3)
    d.line([x0, y0 + dome_r, x0, y1 - 4], fill=(120, 115, 100, 255), width=3)
    d.line([x1, y0 + dome_r, x1, y1 - 4], fill=(120, 115, 100, 255), width=3)

    # surgical cap: teal cap over the top of the dome + forehead band
    d.pieslice([x0 + 4, y0 + 2, x1 - 4, y0 + 104], start=180, end=360,
               fill=(*TEAL, 255))
    d.rectangle([x0 + 4, y0 + 50, x1 - 4, y0 + 62], fill=(*TEAL, 255))
    # small white cross on the cap
    ccx, ccy = cx, y0 + 32
    d.rectangle([ccx - 4, ccy - 12, ccx + 4, ccy + 12], fill=(255, 255, 255, 255))
    d.rectangle([ccx - 12, ccy - 4, ccx + 12, ccy + 4], fill=(255, 255, 255, 255))

    # sparkle eyes + smile (below the cap band, above the bundle)
    eye_y = y0 + 86
    sparkle(d, cx - 30, eye_y, 13, (30, 30, 30, 255))
    sparkle(d, cx + 30, eye_y, 13, (30, 30, 30, 255))
    d.arc([cx - 18, y0 + 102, cx + 18, y0 + 128], start=15, end=165,
          fill=(30, 30, 30, 255), width=3)

    # newborn bundle held at chest height: swaddle + face + VI stamp
    bx0, bx1 = cx - 52, cx + 52
    by0, by1 = y0 + 140, y1 - 8
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18,
                        fill=(*BLANKET, 255), outline=(180, 160, 110, 255), width=2)
    # one swaddle fold line below the face
    d.line([bx0 + 10, by0 + 36, bx1 - 10, by0 + 36], fill=(180, 160, 110, 255), width=2)
    # baby face peeking out at the top
    d.ellipse([cx - 20, by0 - 14, cx + 20, by0 + 26], fill=(*PEACH, 255))
    d.ellipse([cx - 20, by0 - 14, cx + 20, by0 + 26], outline=(180, 140, 110, 255), width=2)
    # closed happy eyes + tiny smile
    d.arc([cx - 12, by0 + 2, cx - 2, by0 + 12], start=200, end=340, fill=(90, 60, 40, 255), width=2)
    d.arc([cx + 2, by0 + 2, cx + 12, by0 + 12], start=200, end=340, fill=(90, 60, 40, 255), width=2)
    d.arc([cx - 7, by0 + 10, cx + 7, by0 + 20], start=15, end=165, fill=(90, 60, 40, 255), width=2)
    # VI on the blanket
    vf = font(SERIF_BOLD, 30)
    d.text((cx, by0 + 52), "VI", font=vf, fill=NAVY, anchor="mm")

    # arms: two small white nubs cradling the bundle from the sides
    d.ellipse([bx0 - 14, by0 + 20, bx0 + 10, by0 + 52], fill=(255, 255, 255, 255),
              outline=(120, 115, 100, 255), width=2)
    d.ellipse([bx1 - 10, by0 + 20, bx1 + 14, by0 + 52], fill=(255, 255, 255, 255),
              outline=(120, 115, 100, 255), width=2)
    base.alpha_composite(layer)


def draw_paid_stamp(base, cx, cy, angle=-13):
    """Rotated red PAID IN FULL stamp, drawn on its own layer so the
    rotation never touches the rest of the image."""
    sw, sh = 260, 110
    stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(stamp)
    d.rectangle([4, 4, sw - 5, sh - 5], outline=(*RED, 255), width=5)
    d.rectangle([12, 12, sw - 13, sh - 13], outline=(*RED, 255), width=2)
    f1 = font(SANS_BOLD, 34)
    d.text((sw // 2, 34), "PAID", font=f1, fill=RED, anchor="mm")
    f2 = font(SANS_BOLD, 22)
    d.text((sw // 2, 70), "IN FULL", font=f2, fill=RED, anchor="mm")
    star5(d, 30, 34, 12, RED)
    star5(d, sw - 30, 34, 12, RED)
    rot = stamp.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(rot, (int(cx - rot.width // 2), int(cy - rot.height // 2)))


def main():
    img = Image.new("RGBA", (W, H), (*PAPER, 255))
    d = ImageDraw.Draw(img)

    # --- frame ---
    d.rectangle([14, 14, W - 15, H - 15], outline=TEAL_DARK, width=4)
    d.rectangle([24, 24, W - 25, H - 25], outline=TEAL_DARK, width=2)

    # --- header band: hospital name + maternity ward ---
    d.rectangle([24, 24, W - 25, 104], fill=TEAL_DARK)
    # white cross in a circle, left
    d.ellipse([44, 38, 90, 84], fill=WHITE)
    d.rectangle([62, 44, 72, 78], fill=TEAL_DARK)
    d.rectangle([50, 56, 84, 66], fill=TEAL_DARK)
    hf = fit(d, "VICE CITY GENERAL HOSPITAL", SANS_BOLD, 32, 800, label="hospital")
    d.text((W // 2 + 20, 52), "VICE CITY GENERAL HOSPITAL", font=hf, fill=WHITE, anchor="mm")
    sf = font(SANS_BOLD, 16)
    d.text((W // 2 + 20, 84), "MATERNITY WARD  \u00b7  EST. 2013", font=sf, fill=GOLD, anchor="mm")

    # --- title + baby name ---
    tf = fit(d, "CERTIFICATE OF LIVE BIRTH", SERIF_BOLD, 44, 940, label="title")
    d.text((W // 2, 138), "CERTIFICATE OF LIVE BIRTH", font=tf, fill=TEAL_DARK, anchor="mm")
    nf = fit(d, "GRAND THEFT AUTO VI", SERIF_BOLD, 56, 940, label="name")
    d.text((W // 2, 190), "GRAND THEFT AUTO VI", font=nf, fill=NAVY, anchor="mm")

    # --- birth facts, two lines ---
    f1 = "BORN 19 NOVEMBER 2026 \u00b7 12:01 AM  \u2014  WEIGHT 214 GB \u00b7 LENGTH 13 YEARS"
    f1f = fit(d, f1, SANS_BOLD, 20, 940, label="facts1")
    d.text((W // 2, 228), f1, font=f1f, fill=INK, anchor="mm")
    f2 = "FATHER: ROCKSTAR GAMES  \u00b7  MOTHER: ONE PATIENT GAMER"
    f2f = fit(d, f2, SANS_BOLD, 20, 940, label="facts2")
    d.text((W // 2, 254), f2, font=f2f, fill=INK, anchor="mm")
    d.line([44, 274, 980, 274], fill=GRAY, width=2)

    # --- art strip: Dr. Ghost + "IT'S A VI!" + PAID stamp ---
    draw_doctor_ghost(img, 250, 288, 190, 210)
    d = ImageDraw.Draw(img)  # refresh after compositing
    vf = fit(d, "IT\u2019S A VI!", SERIF_BOLD, 58, 280, label="itsavi")
    d.text((560, 340), "IT\u2019S A VI!", font=vf, fill=TEAL_DARK, anchor="mm")
    af = font(SANS_BOLD, 21)
    d.text((560, 392), "APGAR SCORE: 10/10", font=af, fill=INK, anchor="mm")
    d.text((560, 420), "(WORTH THE WAIT)", font=font(SANS, 19), fill=GRAY, anchor="mm")
    d.text((560, 456), "FIRST WORDS: \u201cFINALLY.\u201d", font=af, fill=INK, anchor="mm")
    draw_paid_stamp(img, 855, 380)
    d = ImageDraw.Draw(img)

    # --- the killer line ---
    lf = fit(d, "LABOR: 13 YEARS", SERIF_BOLD, 42, 940, label="labor")
    d.text((W // 2, 530), "LABOR: 13 YEARS", font=lf, fill=RED, anchor="mm")
    sub = "\u2014 THE LONGEST IN HOSPITAL HISTORY \u2014"
    subf = fit(d, sub, SANS_BOLD, 20, 940, label="laborsub")
    d.text((W // 2, 564), sub, font=subf, fill=GRAY, anchor="mm")

    # --- hospital bill box ---
    bx0, bx1 = 44, 980
    by = 586
    row_h = 25
    box_h = 36 + len(BILL) * row_h + 10 + 42
    d.rectangle([bx0, by, bx1, by + box_h], outline=TEAL_DARK, width=2)
    d.rectangle([bx0, by, bx1, by + 36], fill=TEAL_DARK)
    hf2 = font(SANS_BOLD, 23)
    d.text((bx0 + 16, by + 18), "HOSPITAL BILL", font=hf2, fill=WHITE, anchor="lm")
    d.text((bx1 - 16, by + 18), "AMOUNT", font=hf2, fill=WHITE, anchor="rm")
    y = by + 36
    for i, (label, price) in enumerate(BILL):
        ry = y + i * row_h
        if i % 2 == 1:
            d.rectangle([bx0, ry, bx1, ry + row_h], fill=PAPER_DARK)
        lab_f = fit(d, label, SANS_BOLD, 20, 640, label="bill-%d" % i)
        d.text((bx0 + 16, ry + row_h // 2), label, font=lab_f, fill=INK, anchor="lm")
        pf = font(SANS_BOLD, 21)
        d.text((bx1 - 16, ry + row_h // 2), "$%s.00" % f"{price:,}",
               font=pf, fill=INK, anchor="rm")
    ty = y + len(BILL) * row_h
    d.line([bx0 + 16, ty + 4, bx1 - 16, ty + 4], fill=TEAL_DARK, width=3)
    d.line([bx0 + 16, ty + 9, bx1 - 16, ty + 9], fill=TEAL_DARK, width=1)
    tf2 = font(SERIF_BOLD, 28)
    d.text((bx0 + 16, ty + 28), "TOTAL DUE", font=tf2, fill=TEAL_DARK, anchor="lm")
    sub2 = "THE YEAR THIS ALL STARTED."
    sub2f = font(SANS_BOLD, 18)
    d.text(((bx0 + bx1) // 2, ty + 30), sub2, font=sub2f, fill=TEAL_DARK, anchor="mm")
    vf2 = font(SERIF_BOLD, 36)
    d.text((bx1 - 16, ty + 26), "$2,013", font=vf2, fill=RED, anchor="ra")

    # --- pitch band ---
    band_y0 = by + box_h + 14
    band_y1 = band_y0 + 104
    d.rectangle([24, band_y0, W - 25, band_y1], fill=MAGENTA)
    bf1 = fit(d, BAND_LINES[0], SANS_BOLD, 29, 700, label="band1")
    d.text((44, band_y0 + 16), BAND_LINES[0], font=bf1, fill=WHITE)
    bf2 = fit(d, BAND_LINES[1], SANS_BOLD, 21, 940, label="band2")
    d.text((44, band_y0 + 48), BAND_LINES[1], font=bf2, fill=WHITE)
    bf3 = font(SANS_BOLD, 23)
    d.text((44, band_y0 + 78), BAND_LINES[2], font=bf3, fill=WHITE)
    # white pill with magenta make.fun, beside short line 1
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([W - 250, band_y0 + 8, W - 44, band_y0 + 40], radius=16,
                         fill=WHITE)
    ppf = font(SANS_BOLD, 26)
    pd.text((W - 147, band_y0 + 24), "make.fun", font=ppf, fill=MAGENTA, anchor="mm")
    img.alpha_composite(pill)
    d = ImageDraw.Draw(img)

    # --- closer ---
    closer = "MOTHER AND GAME ARE DOING FINE."
    clf = fit(d, closer, SERIF_BOLD, 30, 940, label="closer")
    d.text((W // 2, band_y1 + 30), closer, font=clf, fill=NAVY, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")
    img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
    print("bill total: $%s (target $2,013)" % f"{TOTAL_DUE:,}")
    if WARNINGS:
        print("WARNINGS:")
        for wmsg in WARNINGS:
            print(" ", wmsg)
    else:
        print("no truncation warnings")


if __name__ == "__main__":
    main()
