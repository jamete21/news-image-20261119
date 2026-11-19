#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page for 19 November 2026.

Everything is drawn with Pillow and the DejaVu fonts. No network, no
randomness, no timestamps: running this twice produces identical bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAGE_W, PAGE_H = 1024, 1024
PAPER = (245, 240, 226)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (163, 18, 18)          # kicker red
PANEL_LINE = (120, 110, 95)
SOFT = (60, 58, 52)             # secondary text
SKY_TOP = (255, 183, 94)
SKY_MID = (244, 120, 110)
SKY_LOW = (94, 58, 120)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 50)
F_DATE = font("DejaVuSans-Bold.ttf", 17)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSerif-Bold.ttf", 42)
F_DECK = font("DejaVuSans.ttf", 19)
F_STAT_NUM = font("DejaVuSans-Bold.ttf", 23)
F_STAT_LBL = font("DejaVuSans.ttf", 13)
F_LABEL = font("DejaVuSans-Bold.ttf", 15)
F_COL_HEAD = font("DejaVuSans-Bold.ttf", 25)
F_COL_BODY = font("DejaVuSans.ttf", 16)
F_SMALL_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_SMALL_BODY = font("DejaVuSans.ttf", 15)
F_BRIEF = font("DejaVuSans.ttf", 15)
F_BRIEF_LBL = font("DejaVuSans-Bold.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 14)

MARGIN = 30
CONTENT_W = PAGE_W - 2 * MARGIN


def wrap_text(text, fnt, max_width, draw):
    """Split text into lines that each fit max_width with font fnt."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw wrapped lines starting at (x, y); return y after last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def text_block(draw, x, y, text, fnt, max_width, fill, leading):
    """Draw a wrapped text block; return the y just below it."""
    lines = wrap_text(text, fnt, max_width, draw)
    return draw_lines(draw, x, y, lines, fnt, fill, leading)


def skyline(draw, x0, y0, x1, y1):
    """A small Vice City sunset: banded sky, sun, rooftops, two palms."""
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        r = int(SKY_TOP[0] + (SKY_MID[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_MID[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_MID[2] - SKY_TOP[2]) * t)
        ya = y0 + (y1 - y0) * i // steps
        yb = y0 + (y1 - y0) * (i + 1) // steps
        draw.rectangle([x0, ya, x1, yb], fill=(r, g, b))
    # low band of dusk purple
    draw.rectangle([x0, y0 + (y1 - y0) * 3 // 4, x1, y1], fill=SKY_LOW)
    # sun
    cx = x0 + (x1 - x0) * 2 // 3
    cy = y0 + (y1 - y0) // 3
    r = 16
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 170))
    # rooftops, left to right
    base = y1
    towers = [
        (0.00, 0.42, 0.14), (0.14, 0.60, 0.10), (0.24, 0.34, 0.12),
        (0.36, 0.52, 0.10), (0.46, 0.30, 0.12), (0.58, 0.48, 0.10),
        (0.68, 0.36, 0.12), (0.80, 0.55, 0.09), (0.89, 0.40, 0.11),
    ]
    for fx, fh, fw in towers:
        tx = x0 + (x1 - x0) * fx
        tw = (x1 - x0) * fw
        th = (y1 - y0) * fh
        draw.rectangle([tx, base - th, tx + tw, base], fill=(38, 24, 64))
    # two palm silhouettes, drawn against the brighter sky so they read
    for px, ph in [(0.10, 0.52), (0.93, 0.46)]:
        bx = x0 + (x1 - x0) * px
        top = base - (y1 - y0) * ph
        draw.line([bx, base, bx + 4, top], fill=(52, 30, 74), width=3)
        for dx, dy in [(-16, -6), (-12, -14), (0, -18), (12, -14), (16, -6)]:
            draw.line([bx + 4, top, bx + 4 + dx, top + dy],
                      fill=(52, 30, 74), width=3)


def main():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    warnings = []

    # ---- masthead ------------------------------------------------------
    title = "THE WORLD IN ONE PICTURE"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((PAGE_W - tw) / 2, 26), title, font=F_TITLE, fill=INK)
    date_line = "THURSDAY 19 NOVEMBER 2026"
    dw = draw.textlength(date_line, font=F_DATE)
    draw.text(((PAGE_W - dw) / 2, 92), date_line, font=F_DATE, fill=ACCENT)
    draw.line([MARGIN, 124, PAGE_W - MARGIN, 124], fill=RULE, width=3)
    draw.line([MARGIN, 130, PAGE_W - MARGIN, 130], fill=RULE, width=1)

    # ---- lead story: GTA VI -------------------------------------------
    lead_x, lead_y = MARGIN, 144
    lead_w, lead_h = CONTENT_W, 320
    draw.rectangle([lead_x, lead_y, lead_x + lead_w, lead_y + lead_h],
                   outline=RULE, width=2)
    lx = lead_x + 16
    draw.text((lx, lead_y + 12), "GRAND THEFT AUTO VI", font=F_KICKER,
              fill=ACCENT)
    head_y = text_block(draw, lx, lead_y + 38,
                        "Grand Theft Auto VI launches worldwide",
                        F_HEAD, lead_w - 32, INK, 48)
    deck_y = text_block(
        draw, lx, head_y + 8,
        "Rockstar's long-awaited sequel rolls out from midnight local time, "
        "starting in New Zealand, on PlayStation 5 and Xbox Series X|S. Set in "
        "Vice City and the fictional state of Leonida, it follows Lucia "
        "Caminos and Jason Duval \u2014 thirteen years after GTA V, with no PC "
        "release date announced.",
        F_DECK, 600, SOFT, 23)
    # sunset artwork on the right of the deck
    art_x0 = lead_x + lead_w - 330
    art_y0 = head_y + 8
    art_x1 = lead_x + lead_w - 16
    art_y1 = lead_y + lead_h - 66
    skyline(draw, art_x0, art_y0, art_x1, art_y1)
    draw.rectangle([art_x0, art_y0, art_x1, art_y1], outline=RULE, width=1)
    if deck_y > art_y1 + 4:
        warnings.append("lead deck runs past artwork")
    # stat strip along the bottom of the lead panel
    stats = [
        ("\u224816 million", "preorders"),
        ("$1.5B+", "sales before launch (Sensor Tower)"),
        ("$79.99", "standard edition"),
    ]
    stat_y = lead_y + lead_h - 56
    draw.line([lead_x, stat_y - 8, lead_x + lead_w, stat_y - 8],
              fill=PANEL_LINE, width=1)
    sw = lead_w // 3
    for i, (num, lbl) in enumerate(stats):
        cx = lead_x + i * sw
        if i:
            draw.line([cx, stat_y - 4, cx, lead_y + lead_h - 10],
                      fill=PANEL_LINE, width=1)
        nw = draw.textlength(num, font=F_STAT_NUM)
        draw.text((cx + (sw - nw) / 2, stat_y), num, font=F_STAT_NUM,
                  fill=INK)
        lw = draw.textlength(lbl, font=F_STAT_LBL)
        draw.text((cx + (sw - lw) / 2, stat_y + 28), lbl, font=F_STAT_LBL,
                  fill=SOFT)

    # ---- two-column row -------------------------------------------------
    row2_y, row2_h = 480, 196
    col_gap = 20
    col_w = (CONTENT_W - col_gap) // 2
    cols2 = [
        ("SUMMIT \u2014 SHENZHEN",
         "Trump, Xi and Putin meet in first-ever trilateral summit",
         "The three leaders gather at Kylin Villa at 2:30pm local time, on "
         "the APEC sidelines. Trump arrived Nov 18; Putin arrived early Nov "
         "18 for talks with Xi. Possible subjects: Ukraine, Iran, trade, AI "
         "and nuclear weapons. No formal agenda published; first Trump\u2013"
         "Putin meeting in over a year."),
        ("WASHINGTON",
         "Jeffries nominated for House Speaker",
         "Democrats nominated Hakeem Jeffries 251\u201311 in a ballot on "
         "Wednesday. If elected Jan 3 he would be the first Black Speaker "
         "(218 votes needed). Katherine Clark is set to be the first woman "
         "majority leader, Pete Aguilar the first Latino whip, Lauren "
         "Underwood the highest-ranking Black woman in Congress."),
    ]
    for i, (label, head, body) in enumerate(cols2):
        x = MARGIN + i * (col_w + col_gap)
        draw.text((x, row2_y), label, font=F_LABEL, fill=ACCENT)
        hy = text_block(draw, x, row2_y + 22, head, F_COL_HEAD, col_w, INK, 28)
        end = text_block(draw, x, hy + 6, body, F_COL_BODY, col_w, SOFT, 18)
        if end > row2_y + row2_h:
            warnings.append(f"two-col {i} overflows by {end - row2_y - row2_h}px")
    draw.line([MARGIN, row2_y + row2_h + 8, PAGE_W - MARGIN,
               row2_y + row2_h + 8], fill=PANEL_LINE, width=1)

    # ---- three-column row ----------------------------------------------
    row3_y, row3_h = 700, 164
    col3_w = (CONTENT_W - 2 * col_gap) // 3
    cols3 = [
        ("SPACE",
         "Voyager 1 one light-day from Earth",
         "It crossed the mark Wednesday at 5:16:07am EST \u2014 16.1 billion "
         "miles, 173.14 AU \u2014 the first human-made object that far. NASA "
         "confirms at JPL."),
        ("EUROPE",
         "EU proposes \u20ac45B loan for Ukraine",
         "The European Commission is to present a \u20ac45 billion loan for "
         "Ukraine, raised on capital markets and repaid after Russia pays "
         "reparations (Financial Times)."),
        ("WEATHER",
         "Cyclone Akvan strengthens",
         "The storm is intensifying into a very severe cyclonic storm over "
         "the Bay of Bengal and is expected to reach the Andhra Pradesh "
         "coast on Nov 20."),
    ]
    for i, (label, head, body) in enumerate(cols3):
        x = MARGIN + i * (col3_w + col_gap)
        draw.text((x, row3_y), label, font=F_LABEL, fill=ACCENT)
        hy = text_block(draw, x, row3_y + 22, head, F_SMALL_HEAD, col3_w,
                        INK, 25)
        end = text_block(draw, x, hy + 5, body, F_SMALL_BODY, col3_w, SOFT,
                         18)
        if end > row3_y + row3_h:
            warnings.append(f"three-col {i} overflows by "
                            f"{end - row3_y - row3_h}px")
    draw.line([MARGIN, row3_y + row3_h + 8, PAGE_W - MARGIN,
               row3_y + row3_h + 8], fill=PANEL_LINE, width=1)

    # ---- in brief --------------------------------------------------------
    brief_y = 880
    draw.text((MARGIN, brief_y), "IN BRIEF", font=F_BRIEF_LBL, fill=ACCENT)
    briefs = [
        "Russia accuses France of deploying troops to Ukraine, Foreign "
        "Minister Lavrov said (AFP).",
        "India beat Pakistan 2\u20131 to win the SAFF Championship final in "
        "Dhaka.",
        "Australia sanctions Israeli settlers and organisations over West "
        "Bank expansion.",
    ]
    bw = (CONTENT_W - 2 * col_gap) // 3
    for i, item in enumerate(briefs):
        x = MARGIN + i * (bw + col_gap)
        if i:
            draw.line([x - col_gap // 2, brief_y + 2, x - col_gap // 2,
                       brief_y + 62], fill=PANEL_LINE, width=1)
        end = text_block(draw, x, brief_y + 24, item, F_BRIEF, bw, SOFT, 18)
        if end > brief_y + 78:
            warnings.append(f"brief {i} overflows by {end - brief_y - 78}px")

    # ---- footer ----------------------------------------------------------
    draw.line([MARGIN, 972, PAGE_W - MARGIN, 972], fill=RULE, width=2)
    foot = "Sources: Reuters, AP, CNN, NASA, Financial Times, AFP."
    fw = draw.textlength(foot, font=F_FOOT)
    draw.text(((PAGE_W - fw) / 2, 982), foot, font=F_FOOT, fill=SOFT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    size = os.path.getsize(out)
    print(f"wrote {out}: {PAGE_W}x{PAGE_H}, {size} bytes")
    if size > 1048576:
        warnings.append(f"entry.png over 1 MiB ({size} bytes)")
    for w in warnings:
        print(f"WARNING: {w}")
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
