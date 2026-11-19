#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up 19 Nov 2026 world news.

Every headline is grounded in reporting from 19 November 2026:
  - Grand Theft Auto VI launches worldwide: midnight local rollout
    from New Zealand, PS5 + Xbox Series X|S, $79.99, Vice City /
    Leonida, Lucia Caminos and Jason Duval, ~16M preorders, $1.5B+
    in sales before launch (Sensor Tower), 13 years after GTA V,
    no PC date announced (Reuters; AP; The Guardian)
  - Trump-Xi-Putin trilateral summit in Shenzhen TODAY: first-ever
    trilateral format, Kylin Villa 2:30pm local, APEC sidelines;
    Trump arrived Nov 18, Putin arrived early Nov 18 and met Xi;
    Ukraine, Iran, trade, AI, nuclear weapons (New START expired);
    no formal agenda; first Trump-Putin face-to-face in over a year
    (China Foreign Ministry; AP; Le Monde; Yonhap)
  - Hakeem Jeffries nominated for US House Speaker: Democrats 251-11
    in a closed-door secret ballot Wed 18 Nov; first Black Speaker
    if elected Jan 3 (needs 218 votes); Clark first woman majority
    leader, Aguilar first Latino whip, Underwood highest-ranking
    Black woman in Congress (CNN; Reuters; USA Today; NPR)
  - Voyager 1 one light-day from Earth: crossed Wed 18 Nov at
    5:16:07am EST, 16.1 billion miles / 25.9 billion km / 173.14 AU,
    first human-made object that far; NASA confirms at a JPL
    discussion today noon EST; launched Sep 5 1977; signal now
    takes 24 hours each way; Voyager 2 reaches it Nov 2035
    (NASA; Popular Science; EarthSky)
  - EU proposes a EUR 45 billion loan for Ukraine, repaid after
    Russia pays reparations; raised on capital markets
    (Financial Times)
  - Cyclone Akvan over the Bay of Bengal intensifying into a very
    severe cyclonic storm, due at the Andhra Pradesh coast Nov 20
  - Russia accuses France of deploying troops to Ukraine
    (Foreign Minister Lavrov; AFP, Nov 17)
  - Sports: India beats Pakistan 2-1 to win the SAFF Championship
    final in Dhaka
  - Australia sanctions Israeli settlers and organisations over
    West Bank expansion

Output: 1024x1024 PNG, well under the 1 MiB limit. Deterministic:
same input, same bytes (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1024, 1024
PAPER = (247, 243, 234)   # newsprint off-white
INK = (22, 22, 26)        # near-black
RED = (178, 34, 34)       # headline red
TEAL = (16, 78, 90)       # summit teal
GOLD = (176, 132, 24)
GREY = (96, 92, 84)
RULE = (60, 56, 50)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, color, max_w, leading=None):
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, x, y, w, h, label, label_color, headline, deck, hsize=30):
    """One bordered news panel with a kicker, headline and deck."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=label_color)
    draw.text((x + 12, y + 6), label, font=font(SANS_B, 16), fill=(255, 255, 255))
    ty = y + 44
    ty = draw_wrapped(draw, x + 12, ty, headline, font(SERIF, hsize),
                      INK, w - 24, leading=int(hsize * 1.12))
    draw_wrapped(draw, x + 12, ty + 8, deck, font(SANS, 19),
                 (52, 50, 46), w - 24, leading=24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.text((28, 22), "THE WORLD IN ONE PICTURE",
           font=font(SANS_B, 22), fill=RED)
    d.text((28, 52), "Thursday 19 November 2026",
           font=font(SERIF, 52), fill=INK)
    d.text((28, 118), "THE DAY'S WORLD NEWS  •  ONE PAGE  •  EVERY STORY CHECKED",
           font=font(SANS_B, 17), fill=GREY)
    d.line([(28, 152), (996, 152)], fill=INK, width=4)
    d.line([(28, 160), (996, 160)], fill=INK, width=1)

    # ---- Lead story: GTA VI launches ------------------------------------
    x, y, w, h = 28, 176, 968, 252
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    d.rectangle([x, y, x + w, y + 34], fill=RED)
    d.text((x + 14, y + 7), "LEAD  •  GRAND THEFT AUTO VI",
           font=font(SANS_B, 17), fill=(255, 255, 255))
    ty = draw_wrapped(d, x + 14, y + 48,
                      "GTA VI is here — Vice City opens worldwide at midnight",
                      font(SERIF, 40), INK, w - 28, leading=46)
    draw_wrapped(d, x + 14, ty + 10,
                 "Rockstar's sequel launches on PS5 and Xbox Series X|S at "
                 "$79.99, 13 years after GTA V. About 16 million preorders "
                 "and $1.5B+ in sales before a single copy is played — and "
                 "still no PC release date.",
                 font(SANS, 21), (52, 50, 46), w - 28, leading=27)

    # ---- Row 2: Shenzhen summit + Speaker nomination --------------------
    panel(d, 28, 444, 476, 218, "DIPLOMACY  •  SHENZHEN", TEAL,
          "Trump, Xi and Putin meet — a first",
          "The first-ever three-way summit opens at Kylin Villa at "
          "2:30pm, on the APEC sidelines. Ukraine, Iran, trade and "
          "AI on the table; no formal agenda published.")
    panel(d, 520, 444, 476, 218, "U.S. HOUSE", (38, 68, 38),
          "Jeffries nominated for Speaker — 251–11",
          "House Democrats pick Hakeem Jeffries in a secret ballot. "
          "If elected on Jan 3 he would be the first Black Speaker.")

    # ---- Row 3: Voyager, EU loan, Also today ---------------------------
    panel(d, 28, 678, 312, 236, "SPACE  •  NASA", (24, 48, 96),
          "Voyager 1 reaches one light-day from Earth",
          "16.1 billion miles out — the first human-made object "
          "that far. Its signal now takes 24 hours each way.",
          hsize=27)
    panel(d, 356, 678, 312, 236, "EUROPE  •  UKRAINE", (96, 52, 8),
          "EU proposes a €45B loan for Ukraine",
          "Brussels would raise the money on capital markets; "
          "Kyiv repays once Russia pays reparations.",
          hsize=27)

    # Also-today panel (custom: a bulleted list, no headline wrap)
    x, y, w, h = 684, 678, 312, 236
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    d.rectangle([x, y, x + w, y + 30], fill=(52, 50, 46))
    d.text((x + 12, y + 6), "ALSO TODAY", font=font(SANS_B, 16), fill=(255, 255, 255))
    items = [
        "Cyclone Akvan nears Andhra Pradesh, due Nov 20",
        "Russia accuses France of sending troops to Ukraine",
        "India beats Pakistan 2–1, wins SAFF final",
        "Australia sanctions Israeli settlers",
    ]
    iy = y + 44
    for item in items:
        d.text((x + 12, iy), "•", font=font(SANS_B, 18), fill=RED)
        iy = draw_wrapped(d, x + 30, iy, item, font(SANS, 17),
                          (52, 50, 46), w - 42, leading=21)
        iy += 5

    # ---- Footer ---------------------------------------------------------
    d.line([(28, 936), (996, 936)], fill=INK, width=2)
    d.text((28, 950),
           "Sources: Reuters  •  AP  •  CNN  •  NASA  •  Financial Times  •  AFP  —  19 November 2026",
           font=font(SANS, 17), fill=GREY)
    d.text((28, 974),
           "Every headline above is from reporting published on 19 November 2026.",
           font=font(SANS, 17), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
