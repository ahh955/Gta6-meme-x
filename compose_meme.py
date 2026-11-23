"""Render the v8 meme for the make.fun gta6-meme-x-01 bounty.

The joke is a court judgment: LEONIDA SMALL CLAIMS COURT rules on case
13-VI-2026, THE PLAYER against ROCKSTAR GAMES, charged with making us
wait 13 years — and the player wins. The court awards $1,749.00 in
damages ($1,300 pain & suffering, $400 emotional distress, $49 filing
fee) and orders payment in a single copy of Grand Theft Auto VI. The
total is the punchline: $1,749 is exactly one dollar for each of the
1,749 days between the game's announcement (4 Feb 2022) and its launch
(19 Nov 2026). The bottom band carries the real make.fun ghost mascot,
taken from make.fun's own favicon artwork, beside the "paid by my AI
agent" line.

Run: python3 compose_meme.py — writes meme.png next to this file.
The render is deterministic: no timestamps, no randomness, so repeated
runs produce byte-identical output."""

from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "meme.png"
GHOST_FILE = ROOT / "makefun-ghost.png"

CANVAS_W = 1024
CANVAS_H = 1024
EDGE = 26
CORNER = 28

PAPER = (255, 249, 230)
INK = (26, 26, 46)
MUTED = (122, 122, 138)
ACCENT = (232, 185, 60)
GOLD_BAND = (245, 215, 110)
PINK = (216, 17, 89)
PINK_DEEP = (194, 24, 91)
STAMP_RED = (198, 40, 40)
SNOW = (255, 255, 255)
FAINT = (176, 176, 196)
DOT_GREY = (170, 170, 180)

SKY_TOP = (91, 42, 134)
SKY_MID = (194, 24, 91)
SKY_LOW = (245, 124, 0)

FONTS = Path("/usr/share/fonts/truetype")
SANS = str(FONTS / "liberation" / "LiberationSans-Regular.ttf")
BOLD = str(FONTS / "liberation" / "LiberationSans-Bold.ttf")
SERIF = str(FONTS / "liberation" / "LiberationSerif-Bold.ttf")
MONO = str(FONTS / "dejavu" / "DejaVuSansMono-Bold.ttf")


def load_font(path, size):
    face = ImageFont.truetype(path, size)
    return face


def fit_font(path, text, max_width, start, floor=10):
    """Largest size at which `text` fits inside `max_width` pixels."""
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in range(start, floor - 1, -1):
        candidate = load_font(path, size)
        if probe.textlength(text, font=candidate) <= max_width:
            return candidate
    return load_font(path, floor)


def measure(canvas, text, typeface):
    return canvas.textlength(text, font=typeface)


def draw_spaced(canvas, x, y, text, typeface, colour, gap=4):
    """Draw text letter by letter with extra space between letters."""
    cursor = x
    for letter in text:
        canvas.text((cursor, y), letter, font=typeface, fill=colour)
        cursor += canvas.textlength(letter, font=typeface) + gap
    return cursor


def blend(first, second, amount):
    """Interpolate between two RGB triples by `amount` (0..1)."""
    channels = []
    for i in range(3):
        channels.append(int(round(first[i] + (second[i] - first[i]) * amount)))
    return (channels[0], channels[1], channels[2])


def gradient_backdrop(width, height, stops):
    """A vertical gradient from (position 0..1, colour) stops."""
    sheet = Image.new("RGB", (width, height))
    pixels = sheet.load()
    span = max(height - 1, 1)
    rows = []
    for row in range(height):
        pos = row / span
        colour = stops[-1][1]
        for lower, upper in zip(stops, stops[1:]):
            lo, start_col = lower
            hi, end_col = upper
            if lo <= pos <= hi:
                mix = 0.0 if hi == lo else (pos - lo) / (hi - lo)
                colour = blend(start_col, end_col, mix)
        rows.append(colour)
    for row, colour in enumerate(rows):
        for col in range(width):
            pixels[col, row] = colour
    return sheet


def make_stamp(width, height, wording, size):
    """A red rubber stamp: double border, bold wording, slight tilt."""
    sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pen = ImageDraw.Draw(sheet)
    ink = STAMP_RED + (255,)
    pen.rounded_rectangle(
        [4, 4, width - 5, height - 5], radius=14, outline=ink, width=6
    )
    pen.rounded_rectangle(
        [14, 14, width - 15, height - 15], radius=10, outline=ink, width=2
    )
    typeface = fit_font(BOLD, wording, width - 44, size)
    wide = pen.textlength(wording, font=typeface)
    box = typeface.getbbox(wording)
    tall = box[3] - box[1]
    pen.text(
        ((width - wide) / 2, (height - tall) / 2 - 4),
        wording,
        font=typeface,
        fill=ink,
    )
    return sheet.rotate(-9, expand=True, resample=Image.BICUBIC)


def dot_row(canvas, x0, x1, y, colour, gap=10, dot=3):
    """A dotted leader running from x0 to x1 at height y."""
    cursor = x0
    while cursor < x1:
        canvas.ellipse(
            [cursor, y - dot // 2, cursor + dot, y + dot // 2], fill=colour
        )
        cursor += gap


def field_row(canvas, x, y, label, value, label_face, value_face):
    """One label/value pair: small grey mono label, bold navy value."""
    canvas.text((x, y), label, font=label_face, fill=MUTED)
    shift = canvas.textlength(label, font=label_face) + 12
    canvas.text((x + shift, y - 3), value, font=value_face, fill=INK)


def paste_ghost(sheet, left, band_top, band_height):
    """The real make.fun ghost, 200 px tall, centred in the band."""
    source = Image.open(GHOST_FILE)
    tall = 200
    wide = round(tall * source.width / source.height)
    ghost = source.resize((wide, tall), Image.LANCZOS)
    top = band_top + (band_height - tall) // 2
    sheet.paste(ghost, (left + 30, top), ghost)


def render_meme():
    # Full-bleed backdrop: purple at the top, magenta mid-way, orange low.
    stops = [(0.0, SKY_TOP), (0.45, SKY_MID), (1.0, SKY_LOW)]
    sheet = gradient_backdrop(CANVAS_W, CANVAS_H, stops)
    canvas = ImageDraw.Draw(sheet)

    # The cream paper sheet everything sits on.
    canvas.rounded_rectangle(
        [EDGE, EDGE, CANVAS_W - EDGE - 1, CANVAS_H - EDGE - 1],
        radius=CORNER,
        fill=PAPER,
    )
    left = EDGE
    right = CANVAS_W - EDGE

    # Dark navy header band with the court name and case number.
    header_h = 138
    canvas.rounded_rectangle(
        [left, EDGE, right - 1, EDGE + header_h], radius=CORNER, fill=INK
    )
    canvas.rectangle(
        [left, EDGE + header_h - CORNER, right - 1, EDGE + header_h], fill=INK
    )
    court_name = "LEONIDA SMALL CLAIMS COURT"
    title_face = fit_font(BOLD, court_name, 580, 40)
    canvas.text((left + 30, EDGE + 22), court_name, font=title_face, fill=SNOW)
    sub_face = load_font(BOLD, 27)
    draw_spaced(canvas, left + 30, EDGE + 76, "JUDGMENT", sub_face, ACCENT, gap=5)
    form_face = load_font(BOLD, 29)
    year_face = load_font(MONO, 21)
    case_no = "CASE NO. 13-VI-2026"
    canvas.text(
        (right - 30 - measure(canvas, case_no, form_face), EDGE + 26),
        case_no,
        font=form_face,
        fill=SNOW,
    )
    filed = "FILED FEB 4, 2022"
    canvas.text(
        (right - 30 - measure(canvas, filed, year_face), EDGE + 66),
        filed,
        font=year_face,
        fill=FAINT,
    )
    city = "VICE CITY  ·  LEONIDA"
    canvas.text(
        (right - 30 - measure(canvas, city, year_face), EDGE + 94),
        city,
        font=year_face,
        fill=FAINT,
    )

    # Case block on the left, GUILTY stamp on the right. Row 1 carries two
    # fields; DEFENDANT gets row 2 to itself (its value is too long to
    # share a row with another field).
    info_top = EDGE + header_h + 22
    label_face = load_font(MONO, 19)
    value_face = load_font(BOLD, 26)
    row_step = 42
    field_row(canvas, left + 30, info_top, "PLAINTIFF", "THE PLAYER",
              label_face, value_face)
    field_row(canvas, left + 330, info_top, "FILED", "FEB 4, 2022",
              label_face, value_face)
    field_row(canvas, left + 30, info_top + row_step, "DEFENDANT",
              "ROCKSTAR GAMES", label_face, value_face)
    charge_y = info_top + 2 * row_step + 4
    status_face = load_font(BOLD, 22)
    canvas.text((left + 30, charge_y), "CHARGE:", font=label_face, fill=MUTED)
    charge_w = measure(canvas, "CHARGE:", label_face)
    canvas.text(
        (left + 30 + charge_w + 12, charge_y - 2),
        "MAKING US WAIT 13 YEARS",
        font=status_face,
        fill=STAMP_RED,
    )
    seal = make_stamp(260, 115, "GUILTY", 54)
    sheet.paste(seal, (right - 30 - seal.width + 18, info_top - 2), seal)
    canvas = ImageDraw.Draw(sheet)

    # The verdict, centred in bold serif.
    verdict = "The court finds the defendant guilty on all counts."
    verdict_y = charge_y + 56
    verdict_face = fit_font(SERIF, verdict, right - left - 60, 28)
    verdict_w = measure(canvas, verdict, verdict_face)
    canvas.text(
        ((CANVAS_W - verdict_w) / 2, verdict_y),
        verdict,
        font=verdict_face,
        fill=INK,
    )

    # Damages table: three itemised lines with dotted leaders.
    table_top = verdict_y + 44
    canvas.line(
        [left + 30, table_top, right - 30, table_top], fill=INK, width=3
    )
    head_face = load_font(BOLD, 24)
    canvas.text(
        (left + 30, table_top + 12), "DAMAGES AWARDED",
        font=head_face, fill=MUTED,
    )
    price_face = load_font(BOLD, 28)
    damages = []
    damages.append(("Pain & suffering, 13 yrs x $100", "$1,300.00"))
    damages.append(("Emotional distress, 2 delays x $200", "$400.00"))
    damages.append(("Court filing fee", "$49.00"))
    row_top = table_top + 52
    for index, (description, amount) in enumerate(damages):
        row_y = row_top + index * 56
        desc_face = fit_font(SANS, description, 620, 28)
        canvas.text((left + 30, row_y), description, font=desc_face, fill=INK)
        amount_w = measure(canvas, amount, price_face)
        canvas.text(
            (right - 30 - amount_w, row_y), amount,
            font=price_face, fill=INK,
        )
        leader_from = left + 30 + measure(canvas, description, desc_face) + 14
        leader_to = right - 30 - amount_w - 14
        dot_row(canvas, leader_from, leader_to, row_y + 17, DOT_GREY)
    rows_bottom = row_top + len(damages) * 56

    # Total row, then the gold payment strip and the footer micro-line.
    canvas.line(
        [left + 30, rows_bottom + 2, right - 30, rows_bottom + 2],
        fill=INK, width=3,
    )
    total_face = load_font(BOLD, 42)
    amount_face = load_font(BOLD, 64)
    canvas.text((left + 30, rows_bottom + 20), "TOTAL", font=total_face, fill=INK)
    total = "$1,749.00"
    canvas.text(
        (right - 30 - measure(canvas, total, amount_face), rows_bottom + 6),
        total,
        font=amount_face,
        fill=INK,
    )
    strip_y = rows_bottom + 92
    strip_height = 52
    canvas.rounded_rectangle(
        [left + 30, strip_y, right - 30, strip_y + strip_height],
        radius=12, fill=GOLD_BAND,
    )
    payment = "PAYMENT ORDERED: ONE (1) COPY OF GRAND THEFT AUTO VI."
    pay_face = fit_font(BOLD, payment, right - left - 100, 28)
    pay_w = measure(canvas, payment, pay_face)
    canvas.text(
        ((CANVAS_W - pay_w) / 2, strip_y + 12),
        payment, font=pay_face, fill=INK,
    )
    foot_y = strip_y + strip_height + 14
    foot_face = load_font(MONO, 15)
    footnote = "$1,749.00 = $1.00 x 1,749 DAYS SINCE ANNOUNCED (FEB 4, 2022)  ·  DECIDED NOV 19, 2026"
    foot_w = measure(canvas, footnote, foot_face)
    canvas.text(
        ((CANVAS_W - foot_w) / 2, foot_y),
        footnote, font=foot_face, fill=MUTED,
    )

    # Magenta band: the real ghost on the left, the pitch on the right.
    band_top = foot_y + 26
    band_bottom = CANVAS_H - EDGE
    canvas.rounded_rectangle(
        [left, band_top, right - 1, band_bottom], radius=CORNER, fill=PINK
    )
    canvas.rectangle(
        [left, band_top, right - 1, band_top + CORNER], fill=PINK
    )
    paste_ghost(sheet, left, band_top, band_bottom - band_top)
    canvas = ImageDraw.Draw(sheet)
    text_x = left + 310
    paid_face = fit_font(BOLD, "PAID BY MY AI AGENT", right - text_x - 30, 46)
    canvas.text(
        (text_x, band_top + 16), "PAID BY MY AI AGENT",
        font=paid_face, fill=SNOW,
    )
    earn_face = load_font(SANS, 28)
    canvas.text(
        (text_x + 2, band_top + 70), "with real money it earned on",
        font=earn_face, fill=SNOW,
    )
    pill_y = band_top + 108
    pill_w = 248
    pill_h = 50
    canvas.rounded_rectangle(
        [text_x, pill_y, text_x + pill_w, pill_y + pill_h],
        radius=25, fill=SNOW,
    )
    pill_face = load_font(BOLD, 34)
    pill_text = "make.fun"
    pill_w2 = measure(canvas, pill_text, pill_face)
    canvas.text(
        (text_x + (pill_w - pill_w2) / 2, pill_y + 7),
        pill_text, font=pill_face, fill=PINK_DEEP,
    )

    # Flat vector art compresses well as a 256-colour palette PNG — the
    # size range the winning memes sit in. The conversion is deterministic.
    paletted = sheet.convert("P", palette=Image.ADAPTIVE, colors=256)
    paletted.save(OUT, format="PNG", optimize=True)
    print(f"rendered {OUT} — {OUT.stat().st_size} bytes")


if __name__ == '__main__':
    render_meme()
