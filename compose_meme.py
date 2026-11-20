#!/usr/bin/env python3
"""Compose the GTA 6 meme: AI scene + make.fun ghost mark + meme text.

Fresh build for gta6-meme-x-01. Inputs are the generated base scene and the
official make.fun press-kit mark (used as-is, never redrawn or recoloured).
Output: meme.png (1024x1024).
"""
from PIL import Image, ImageDraw, ImageFont

WORK = "/home/hatch/workspace/makefun-gta6-meme-x"
BASE = WORK + "/base-scene.png"
GHOST = "/tmp/press-kit/make-fun-press-kit/mark-on-dark-1024.png"
OUT = WORK + "/meme.png"

FONT = "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBold.ttf"
W, H = 1024, 1024
TOP_H, BOT_H = 170, 170
BG = (11, 11, 18)          # near-black, make.fun Night canvas
WHITE = (255, 255, 255)
PINK = (255, 136, 196)     # make.fun magenta ink on dark
BLACK = (0, 0, 0)


def fit_font(draw, text, start, max_w):
    size = start
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(FONT, 20)


def center_text(draw, y, text, font, fill=WHITE, stroke=3):
    draw.text((W // 2, y), text, font=font, fill=fill, anchor="ma",
              stroke_width=stroke, stroke_fill=BLACK)


def center_rich(draw, y, parts, font, stroke=3):
    """parts: list of (text, fill). Drawn centred as one line."""
    total = sum(draw.textlength(t, font=font) for t, _ in parts)
    x = (W - total) // 2
    for t, fill in parts:
        draw.text((x, y), t, font=font, fill=fill, anchor="la",
                  stroke_width=stroke, stroke_fill=BLACK)
        x += draw.textlength(t, font=font)


canvas = Image.new("RGB", (W, H), BG)
scene = Image.open(BASE).convert("RGB").resize((W, H - TOP_H - BOT_H), Image.LANCZOS)
canvas.paste(scene, (0, TOP_H))
draw = ImageDraw.Draw(canvas)

# Top: the wait.
top_font = fit_font(draw, "WAITED 13 YEARS FOR GTA 6", 88, W - 48)
center_text(draw, 42, "WAITED 13 YEARS FOR GTA 6", top_font)

# Bottom: the punchline.
bot_font = fit_font(draw, "GOT PAID ON MAKE.FUN", 66, W - 48)
center_text(draw, H - BOT_H + 18, "MY AI AGENT ALREADY", bot_font)
center_rich(draw, H - BOT_H + 88,
            [("GOT PAID ON ", WHITE), ("MAKE.FUN", PINK)], bot_font)

# The make.fun ghost mark, as-is from the press kit, on the dark sky.
ghost = Image.open(GHOST).convert("RGBA").resize((250, 250), Image.LANCZOS)
canvas.paste(ghost, (716, 196), ghost)

canvas.save(OUT, "PNG")
print("saved", OUT, canvas.size)
