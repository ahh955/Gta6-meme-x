#!/usr/bin/env python3
"""Compose the GTA 6 meme v2 for make.fun bounty gta6-meme-x-01.

Document type: BOARDING PASS -- flight GTA VI, delayed 4,811 days.
Flat vector style, drawn procedurally with PIL. Deterministic: re-running
regenerates meme.png byte-identically (fixed seed, no timestamps).

Layout (1024x1024):
  dark navy background, white boarding-pass card, magenta header band,
  LOS SANTOS -> LEONIDA route, big DELAYED 4,811 DAYS status strip,
  passenger/flight detail grid, itemised fare breakdown, a rotated
  "PAID BY MY AI AGENT ON MAKE.FUN" stamp, perforated tear-off stub
  with barcode and the make.fun ghost mark.
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "meme.png"

W = H = 1024

# --- palette (make.fun brand magenta + document inks) ---
NAVY_BG = (23, 17, 46)       # deep navy page background
WHITE = (255, 255, 255)
INK = (25, 20, 25)           # make.fun Light ink
GREY = (90, 83, 89)          # make.fun secondary
HAIRLINE = (226, 222, 225)   # make.fun hairline
MAGENTA = (196, 28, 131)     # make.fun brand magenta #C41C83
MAGENTA_DK = (188, 12, 124)  # light-mode magenta #BC0C7C
RED = (200, 16, 46)          # delay red
PINK_PALE = (253, 238, 247)  # pale pink status strip

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
F_REG = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731
F_MONO = lambda s: font("DejaVuSansMono.ttf", s)         # noqa: E731
F_MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)  # noqa: E731


def text_w(draw: ImageDraw.ImageDraw, s: str, f) -> int:
    return draw.textlength(s, font=f)


def dashed_hline(draw, x0, x1, y, color, dash=14, gap=10, width=3):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + dash, x1), y)], fill=color, width=width)
        x += dash + gap


def dashed_vline(draw, x, y0, y1, color, dash=12, gap=9, width=2):
    y = y0
    while y < y1:
        draw.line([(x, y), (x, min(y + dash, y1))], fill=color, width=width)
        y += dash + gap


def dotted_leader_row(draw, x0, x1, y, label, price, f_label, f_price,
                      label_color=INK, price_color=INK):
    """One itemised row: label .... dotted leader .... price."""
    draw.text((x0, y), label, font=f_label, fill=label_color)
    pw = text_w(draw, price, f_price)
    draw.text((x1 - pw, y), price, font=f_price, fill=price_color)
    lx = x0 + text_w(draw, label, f_label) + 12
    rx = x1 - pw - 12
    cy = y + f_label.size // 2 + 4
    x = lx
    while x < rx:
        draw.ellipse([x, cy - 2, x + 3, cy + 1], fill=GREY)
        x += 11


def draw_barcode(draw, x0, y0, height, max_w, seed=4811):
    """Deterministic pseudo-random barcode."""
    rng = random.Random(seed)
    x = x0
    while x < x0 + max_w - 6:
        w = rng.choice([2, 2, 3, 3, 4, 5])
        if rng.random() < 0.62:
            draw.rectangle([x, y0, x + w - 1, y0 + height], fill=INK)
        x += w + rng.choice([1, 2, 2, 3])


def make_stamp():
    """Rotated 'PAID BY MY AI AGENT ON MAKE.FUN' stamp, RGBA layer.

    Sized to sit over the dotted leaders of the fare block without
    covering the row labels (left) or the prices (right).
    """
    sw, sh = 440, 118
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # double border, stamp style
    d.rounded_rectangle([6, 6, sw - 7, sh - 7], radius=10,
                        outline=MAGENTA_DK + (225,), width=5)
    d.rounded_rectangle([16, 16, sw - 17, sh - 17], radius=6,
                        outline=MAGENTA_DK + (225,), width=2)
    f1 = F_BOLD(34)
    f2 = F_BOLD(24)
    l1 = "PAID BY MY AI AGENT"
    l2 = "ON MAKE.FUN"
    d.text(((sw - text_w(d, l1, f1)) / 2, 14), l1, font=f1,
           fill=MAGENTA_DK + (225,))
    d.text(((sw - text_w(d, l2, f2)) / 2, 62), l2, font=f2,
           fill=MAGENTA_DK + (225,))
    return layer.rotate(8, expand=True, resample=Image.BICUBIC,
                        fillcolor=(0, 0, 0, 0))


def main():
    img = Image.new("RGB", (W, H), NAVY_BG)
    draw = ImageDraw.Draw(img)

    # --- card ---
    CARD = (30, 30, 994, 994)
    draw.rounded_rectangle(CARD, radius=26, fill=WHITE)

    # --- header band (magenta, rounded top) ---
    draw.rounded_rectangle([30, 30, 994, 160], radius=26, fill=MAGENTA)
    draw.rectangle([30, 134, 994, 160], fill=MAGENTA)

    # ghost mark in the header (press-kit asset, used as-is, scaled only)
    ghost = Image.open(ASSETS / "mark-1024.png").convert("RGBA")
    ghost_h = ghost.resize((96, 96), Image.LANCZOS)
    img.paste(ghost_h, (52, 46), ghost_h)

    draw.text((164, 52), "LEONIDA AIR", font=F_BOLD(54), fill=WHITE)
    draw.text((164, 116), "VICE CITY  •  EST. 2013  •  FINALLY BOARDING",
              font=F_BOLD(19), fill=(255, 210, 235))
    rp = "BOARDING PASS"
    draw.text((962 - text_w(draw, rp, F_BOLD(30)), 52), rp,
              font=F_BOLD(30), fill=WHITE)
    rs = "ECONOMY OF PATIENCE"
    draw.text((962 - text_w(draw, rs, F_BOLD(19)), 116), rs,
              font=F_BOLD(19), fill=(255, 210, 235))

    # --- route ---
    draw.text((58, 188), "LOS SANTOS", font=F_BOLD(46), fill=INK)
    draw.text((58, 246), "GTA V  •  LEFT 17 SEP 2013", font=F_BOLD(20),
              fill=GREY)
    dest = "LEONIDA"
    draw.text((966 - text_w(draw, dest, F_BOLD(46)), 188), dest,
              font=F_BOLD(46), fill=MAGENTA)
    dsub = "VICE CITY  •  LANDING 19 NOV 2026"
    draw.text((966 - text_w(draw, dsub, F_BOLD(20)), 246), dsub,
              font=F_BOLD(20), fill=GREY)
    # flight path: dashes + plane + arrowhead
    dashed_hline(draw, 388, 470, 214, MAGENTA, dash=12, gap=9, width=4)
    dashed_hline(draw, 556, 652, 214, MAGENTA, dash=12, gap=9, width=4)
    plane = "\u2708"
    fp = F_BOLD(44)
    draw.text((512 - text_w(draw, plane, fp) / 2, 186), plane, font=fp,
              fill=MAGENTA)
    draw.polygon([(652, 206), (652, 222), (674, 214)], fill=MAGENTA)

    # --- status strip ---
    draw.rounded_rectangle([58, 306, 966, 396], radius=14, fill=PINK_PALE)
    draw.rounded_rectangle([58, 306, 966, 396], radius=14,
                           outline=MAGENTA, width=2)
    st = "STATUS"
    draw.text((512 - text_w(draw, st, F_BOLD(19)) / 2, 318), st,
              font=F_BOLD(19), fill=RED)
    big = "DELAYED 4,811 DAYS"
    draw.text((512 - text_w(draw, big, F_BOLD(48)) / 2, 340), big,
              font=F_BOLD(48), fill=RED)

    # --- detail grid ---
    grid = [
        ("PASSENGER", "ONE PATIENT GAMER", "FLIGHT", "GTA VI-2013",
         "DATE", "19 NOV 2026"),
        ("GATE", "13", "SEAT", "13A — WINDOW", "BOARDING",
         "13 YEARS LATE"),
    ]
    col_x = [58, 392, 700]
    row_y = [420, 500]
    for r, row in enumerate(grid):
        for c in range(3):
            label, value = row[c * 2], row[c * 2 + 1]
            x = col_x[c]
            y = row_y[r]
            draw.text((x, y), label, font=F_BOLD(18), fill=GREY)
            draw.text((x, y + 24), value, font=F_BOLD(26), fill=INK)

    # --- fare breakdown ---
    draw.line([(58, 582), (966, 582)], fill=HAIRLINE, width=2)
    draw.text((58, 598), "F A R E   B R E A K D O W N", font=F_BOLD(19),
              fill=GREY)
    fares = [
        ("BASE FARE — GTA VI, AT LAST", "$79.99"),
        ("DELAY SURCHARGE x 2", "$0.00"),
        ("TRAILER REWATCHES x 1,337", "$0.00"),
        ("BAGGAGE — 214 GB DOWNLOAD", "$0.00"),
        ("SICK DAYS — 5, DOCTOR APPROVED", "$0.00"),
    ]
    y = 632
    for label, price in fares:
        dotted_leader_row(draw, 58, 966, y, label, price,
                          F_MONO(23), F_MONO_B(23))
        y += 33
    draw.line([(58, y + 4), (966, y + 4)], fill=INK, width=2)
    draw.text((58, y + 14), "TOTAL DUE", font=F_MONO_B(28), fill=INK)
    tot = "$79.99"
    draw.text((966 - text_w(draw, tot, F_MONO_B(28)), y + 14), tot,
              font=F_MONO_B(28), fill=INK)

    # --- stamp (overlaps the fare block's dotted leaders, like the
    # top memes -- labels stay clear on the left, prices on the right)
    stamp = make_stamp()
    img.paste(stamp, (440, 688), stamp)

    # --- perforation + tear-off notches ---
    PERF_Y = 884
    dashed_hline(draw, 30, 994, PERF_Y, GREY, dash=12, gap=9, width=3)
    draw.ellipse([30 - 17, PERF_Y - 17, 30 + 17, PERF_Y + 17], fill=NAVY_BG)
    draw.ellipse([994 - 17, PERF_Y - 17, 994 + 17, PERF_Y + 17],
                 fill=NAVY_BG)

    # --- stub ---
    draw_barcode(draw, 58, 908, 56, 230)
    draw.text((58, 968), "GTAVI-2013-4811", font=F_MONO(15), fill=GREY)
    draw.text((330, 906), "ADMIT ONE", font=F_BOLD(30), fill=INK)
    draw.text((330, 944), "TRAVELLING WITH JASON & LUCIA",
              font=F_BOLD(19), fill=GREY)
    draw.text((330, 968), "THANK YOU FOR WAITING 13 YEARS.",
              font=F_REG(15), fill=GREY)
    ghost_s = ghost.resize((72, 72), Image.LANCZOS)
    img.paste(ghost_s, (894, 906), ghost_s)
    mf = "make.fun"
    draw.text((884 - text_w(draw, mf, F_BOLD(22)), 928), mf,
              font=F_BOLD(22), fill=MAGENTA)

    # Flat artwork quantizes cleanly: an adaptive 256-colour palette
    # keeps the file small (the leaderboard tie-break) with no visible
    # loss. Median-cut quantisation is deterministic for fixed input,
    # so re-runs stay byte-identical.
    img_p = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img_p.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
