#!/usr/bin/env python3
"""Render THE WORLD TODAY — the 21 November 2026 front page.

Draws a 1024x1024 newspaper page with PIL: masthead, lead story with an
editorial illustration band, four columns, a markets strip and a ticker.
Deterministic: same inputs always produce the same PNG bytes.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PAGE = 1024
MARGIN = 36
CONTENT = PAGE - 2 * MARGIN  # 952

PAPER = (246, 241, 229)
INK = (28, 26, 22)
FADED = (74, 70, 62)
RED = (164, 31, 31)
RULE = (28, 26, 22)
BAR_RED = (164, 31, 31)
BAR_GREY = (150, 142, 128)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, face, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, face, x, y, leading, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def build_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)
    left = MARGIN
    right = PAGE - MARGIN

    # --- top eyebrow -------------------------------------------------
    small = font(SANS_B, 13)
    draw.text((left, 26), "LATE EDITION", font=small, fill=FADED)
    mid = "WORLD NEWS IN ONE PAGE"
    draw.text(((PAGE - draw.textlength(mid, font=small)) / 2, 26),
              mid, font=small, fill=FADED)
    num = "No. 325"
    draw.text((right - draw.textlength(num, font=small), 26),
              num, font=small, fill=FADED)
    hline(draw, left, right, 48, 2)

    # --- masthead ----------------------------------------------------
    mast = font(SERIF_B, 76)
    title = "THE WORLD TODAY"
    draw.text(((PAGE - draw.textlength(title, font=mast)) / 2, 56),
              title, font=mast, fill=INK)
    hline(draw, left, right, 132, 3)
    hline(draw, left, right, 137, 1)

    # --- dateline ----------------------------------------------------
    date_face = font(SERIF_B, 19)
    draw.text((left, 146), "Saturday, November 21, 2026",
              font=date_face, fill=INK)
    places = "WARSAW  ·  ANTALYA  ·  HORMUZ"
    pf = font(SANS_B, 12)
    draw.text((right - draw.textlength(places, font=pf), 149),
              places, font=pf, fill=FADED)
    hline(draw, left, right, 174, 1)

    # --- lead kicker -------------------------------------------------
    kick = font(SANS_B, 14)
    draw.text((left, 184), "SECURITY", font=kick, fill=RED)
    draw.text((left + draw.textlength("SECURITY  ", font=kick), 184),
              "·  NATO'S EASTERN FLANK — POLAND", font=kick, fill=INK)

    # --- lead headline ----------------------------------------------
    head = font(SERIF_B, 56)
    headline = ("Russian Missiles Crash in Poland "
                "as NATO Chief Rushes to Warsaw")
    y = draw_lines(draw, wrap(draw, headline, head, CONTENT),
                   head, left, 206, 56)
    deck_face = font(SERIF_I, 23)
    deck = ("Two cruise missiles and a jet drone fell beside a NATO exercise; "
            "Rutte pledges to defend \u201cevery inch\u201d of Polish soil as "
            "Warsaw asks for F-35s and AWACS.")
    y = draw_lines(draw, wrap(draw, deck, deck_face, CONTENT),
                   deck_face, left, y + 6, 27, fill=FADED)

    # --- hero illustration -------------------------------------------
    hero = Image.open(os.path.join(ROOT, "assets", "lead-illustration.webp"))
    hero = hero.convert("RGB")
    # Keep the broken missile, the exercise camp and the jets: a band
    # from 24% to 72.6% of the height matches the 952x260 frame exactly.
    w0, h0 = hero.size
    hero = hero.crop((0, int(h0 * 0.24), w0, int(h0 * 0.726)))
    hero = hero.resize((CONTENT, 260), Image.LANCZOS)
    hy = y + 12
    page.paste(hero, (left, hy))
    draw.rectangle([left, hy, right - 1, hy + 259], outline=INK, width=2)

    cap_face = font(SERIF_I, 16)
    caption = ("An artist's impression of the wrecked missile in a Polish "
               "wheat field.")
    draw.text((left, hy + 268), caption, font=cap_face, fill=FADED)
    credit = "ILLUSTRATION: MISSILE WRECKAGE IN POLAND"
    cf = font(SANS_B, 11)
    draw.text((right - draw.textlength(credit, font=cf), hy + 270),
              credit, font=cf, fill=FADED)
    y = hy + 296
    hline(draw, left, right, y, 1)

    # --- four columns ------------------------------------------------
    cols = [
        ("CLIMATE · ANTALYA", "COP31 Nears a Deal at Last",
         "After two days of overtime, a new package was tabled overnight; a "
         "vote is set for Sunday morning. The presidency says fossil-fuel "
         "wording is back in, after 130 nations demanded it."),
        ("WAR IN THE GULF", "Two More Tankers Hit in the Strait",
         "Two tankers were struck off Oman on Saturday, one in the stern and "
         "one in the engine room, with no casualties. Iran says it downed a "
         "U.S. drone over Qeshm; Qatari mediators reached Tehran."),
        ("ESPIONAGE · COPENHAGEN", "Denmark Expels Russian Attach\u00e9",
         "Copenhagen says Russian intelligence plotted to kill rapper "
         "Kyivstoner at a September concert, using a banned gang. Two men are "
         "charged; Denmark halts non-essential visas for Russians."),
        ("MARKETS & AI", "Worst Week of the AI Rout",
         "The S&P 500 fell 3.7% for a seventh straight session and the Nasdaq "
         "lost 5.3%, erasing its 2026 gains. Anthropic closed at $88.30 on day "
         "two, near its $83 debut price; bitcoin slid to about $61,000."),
    ]
    gap = 16
    col_w = (CONTENT - 3 * gap) // 4
    cy = y + 12
    kick_f = font(SANS_B, 12)
    col_head = font(SERIF_B, 26)
    body_f = font(SERIF, 15)
    bottom = cy
    for i, (kicker, head_text, body) in enumerate(cols):
        x = left + i * (col_w + gap)
        draw.text((x, cy), kicker, font=kick_f, fill=RED)
        hy2 = draw_lines(draw, wrap(draw, head_text, col_head, col_w),
                         col_head, x, cy + 18, 28)
        end = draw_lines(draw, wrap(draw, body, body_f, col_w),
                         body_f, x, hy2 + 4, 19)
        bottom = max(bottom, end)
    for i in range(3):
        vx = left + (i + 1) * col_w + i * gap + gap // 2
        draw.line([(vx, cy), (vx, bottom)], fill=(200, 192, 176), width=1)
    y = bottom + 10
    hline(draw, left, right, y, 1)

    # --- markets strip -----------------------------------------------
    my = y + 10
    lab = font(SANS_B, 14)
    draw.text((left, my), "MARKETS", font=lab, fill=RED)
    tick = font(SERIF_B, 20)
    px = left + 108
    draw.text((px, my - 1), "ANTHROPIC $88.30", font=tick, fill=INK)
    px += draw.textlength("ANTHROPIC $88.30  ", font=tick)
    small_b = font(SANS_B, 12)
    draw.text((px, my + 2), "\u22129.1%",
              font=small_b, fill=RED)
    # index bars
    bx = left + 380
    bars = [("S&P 500", "-3.70%", 0.70), ("NASDAQ", "-5.28%", 1.00),
            ("DOW", "-1.93%", 0.37)]
    bar_f = font(SANS_B, 11)
    for name, pct, frac in bars:
        draw.text((bx, my + 2), name, font=bar_f, fill=FADED)
        draw.rectangle([bx + 60, my + 4, bx + 60 + 84, my + 14],
                       outline=(180, 172, 156), width=1)
        draw.rectangle([bx + 60, my + 4, bx + 60 + int(84 * frac), my + 14],
                       fill=BAR_RED)
        draw.text((bx + 150, my + 2), pct, font=bar_f, fill=INK)
        bx += 200
    y = my + 30

    # --- bottom ticker ------------------------------------------------
    ty = y + 6
    draw.rectangle([left, ty, right, ty + 30], fill=INK)
    tick_f = font(SANS_B, 12)
    tick_text = ("ALSO SATURDAY  —  Youth rally in 25 countries over living "
                 "costs  ·  Italy's strike, a million claimed  ·  France: "
                 "82,500 march  ·  GTA VI wins praise")
    draw.text((left + 12, ty + 8), tick_text, font=tick_f, fill=PAPER)

    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    page = build_page()
    target = os.path.join(out_dir, "entry.png")
    page.save(target, format="PNG", optimize=True)
    size = os.path.getsize(target)
    print(f"wrote {target} {page.size[0]}x{page.size[1]} {size} bytes")
    if size > 1048576:
        print("ERROR: entry.png exceeds 1 MiB", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
