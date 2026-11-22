#!/usr/bin/env python3
"""Render the 21 November 2026 world-news poster (1024x1024, deterministic).

Build-time only: uses Pillow to draw a newspaper-style poster of six stories
from Saturday 21 November 2026 plus an "also today" strip, and writes
entry.png next to this file. No network, no randomness, no timestamps: two
runs produce byte-identical output. The graded entrypoint is main.py, which
only copies entry.png and never imports Pillow.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette -----------------------------------------------------------------
NAVY = (15, 28, 46)
CREAM = (246, 239, 220)
INK = (20, 33, 61)
RED = (179, 39, 30)
BODY = (43, 43, 43)
MUTED = (90, 90, 90)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREEN = (29, 122, 61)
TEAL = (15, 118, 110)
AMBER = (180, 83, 9)
BLUE = (29, 78, 216)
GOLD = (212, 160, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 54)
F_DATE = font("DejaVuSans-Bold.ttf", 40)
F_SUB = font("DejaVuSans.ttf", 19)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 18)
F_STRIP_B = font("DejaVuSans-Bold.ttf", 17)
F_STRIP = font("DejaVuSans.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 15)


def wrap(text, fnt, max_w, max_lines=None):
    """Greedy word wrap; returns at most max_lines lines (drops the rest)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def star_points(cx, cy, r_out, r_in, points=5, rot=-90.0):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# --- the day's stories --------------------------------------------------------
STORIES = [
    {
        "kicker": "WAR  ·  KRYVYI RIH",
        "accent": RED,
        "headline": "Russian missiles hit Zelenskyy's hometown",
        "body": (
            "Ballistic missiles struck Kryvyi Rih on Friday night, killing "
            "a boy of 7 and a woman of 20 and wounding 60, six of them children."
        ),
        "strip": (28, 43, 69),
        "art": "war",
    },
    {
        "kicker": "CLIMATE  ·  COP31",
        "accent": GREEN,
        "headline": "COP31 talks run into overtime",
        "body": (
            "The Antalya summit overran its Friday deadline with no deal yet. "
            "The draft text drops any call to phase out fossil fuels."
        ),
        "strip": (227, 240, 228),
        "art": "climate",
    },
    {
        "kicker": "MEXICO  ·  CARTELS",
        "accent": TEAL,
        "headline": "Mexico captures \u201cEl Chapo Isidro\u201d",
        "body": (
            "Troops seized FBI most-wanted boss Fausto Isidro Meza Flores in "
            "Sinaloa overnight, with US help. Violence flared after the arrest."
        ),
        "strip": (230, 238, 242),
        "art": "mexico",
    },
    {
        "kicker": "MARKETS  ·  ECONOMY",
        "accent": RED,
        "headline": "AI sell-off drags markets down",
        "body": (
            "The S&P 500 fell 3.7% on Friday and Japan's Nikkei slid 5.1% as "
            "chip shares plunged on doubts the AI boom will pay off."
        ),
        "strip": (251, 233, 231),
        "art": "markets",
    },
    {
        "kicker": "MIDDLE EAST  ·  THE GULF",
        "accent": AMBER,
        "headline": "Gulf tensions flare as Iran claims US jet hit",
        "body": (
            "Bahrain says an Iranian attack set a civilian industrial site "
            "ablaze. Tehran claims it damaged a US F-16 and shot down a "
            "drone over the Gulf."
        ),
        "strip": (219, 234, 254),
        "art": "gulf",
    },
    {
        "kicker": "SPACE  ·  MERCURY",
        "accent": BLUE,
        "headline": "BepiColombo reaches Mercury",
        "body": (
            "After an eight-year journey, the ESA-JAXA spacecraft entered "
            "orbit around the innermost planet. Its two orbiters separate "
            "in December."
        ),
        "strip": (20, 29, 51),
        "art": "space",
    },
]

ALSO_TODAY = [
    "Magnitude 6.8 quake off Timor-Leste, no tsunami threat  ·  EU approves "
    "\u20ac1bn more aid for Ukraine",
    "Russian cargo ship ablaze in the Gulf of Finland  ·  UN to draft "
    "AI-weapons rules by 2028",
]


# --- small illustrations, one per card ---------------------------------------
def art_war(d, x, y, w, h):
    # Night skyline: dark buildings with lit windows, one hit by a flame.
    d.rectangle([x, y, x + w, y + h], fill=(28, 43, 69))
    heights = [26, 34, 22, 38, 28, 32]
    bw = w / len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw + 3
        d.rectangle([bx, y + h - bh, bx + bw - 6, y + h], fill=(51, 65, 94))
        for wy in range(2):
            for wx in range(2):
                d.rectangle(
                    [bx + 5 + wx * 9, y + h - bh + 5 + wy * 10,
                     bx + 8 + wx * 9, y + h - bh + 8 + wy * 10],
                    fill=(240, 200, 90),
                )
    # Flame over the third building.
    fx = x + 2.5 * bw
    d.polygon(
        [(fx - 7, y + h - 22), (fx, y + h - 40), (fx + 7, y + h - 22)],
        fill=(230, 110, 30),
    )
    d.polygon(
        [(fx - 4, y + h - 22), (fx, y + h - 33), (fx + 4, y + h - 22)],
        fill=(245, 180, 60),
    )


def art_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(227, 240, 228))
    cx, cy, r = x + 26, y + h // 2, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 130, 80))
    d.ellipse([cx - 12, cy - 6, cx - 2, cy + 4], fill=(90, 160, 210))
    d.ellipse([cx + 2, cy + 2, cx + 12, cy + 12], fill=(90, 160, 210))
    d.text((x + 52, y + 3), "OVERTIME", font=F_STRIP_B, fill=GREEN)
    d.text((x + 52, y + 22), "no deal yet", font=F_STRIP, fill=MUTED)
    # Clock at the right.
    kx, ky, kr = x + w - 26, y + h // 2, 15
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], outline=(80, 80, 80),
              width=2, fill=WHITE)
    d.line([kx, ky, kx, ky - 9], fill=(60, 60, 60), width=2)
    d.line([kx, ky, kx + 7, ky + 3], fill=(60, 60, 60), width=2)


def art_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 238, 242))
    # Gold sheriff badge with a star.
    bx, by = x + 26, y + h // 2
    d.polygon(
        [(bx - 15, by - 13), (bx + 15, by - 13), (bx + 12, by + 4),
         (bx, by + 16), (bx - 12, by + 4)],
        fill=GOLD,
    )
    d.polygon(star_points(bx, by - 1, 9, 4), fill=(255, 255, 255))
    d.text((x + 50, y + 3), "WANTED", font=F_STRIP_B, fill=RED)
    d.text((x + 50, y + 22), "FBI TOP 10", font=F_STRIP, fill=MUTED)
    # Handcuffs at the right.
    cx = x + w - 62
    d.ellipse([cx, y + 8, cx + 20, y + 28], outline=(90, 90, 90), width=3)
    d.ellipse([cx + 26, y + 8, cx + 46, y + 28], outline=(90, 90, 90),
              width=3)
    d.line([cx + 20, y + 18, cx + 26, y + 18], fill=(90, 90, 90), width=3)


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(251, 233, 231))
    bars = [30, 26, 28, 22, 26, 18]
    bw = 26
    bx = x + 14
    for i, bh in enumerate(bars):
        d.rectangle([bx, y + h - 4 - bh, bx + 16, y + h - 4],
                    fill=(200, 70, 60) if i % 2 else (220, 110, 95))
        bx += bw
    # Falling trend line with an arrowhead.
    d.line([(x + 14, y + 6), (x + w - 92, y + h - 12)], fill=RED, width=3)
    ax, ay = x + w - 92, y + h - 12
    d.polygon([(ax, ay + 8), (ax + 12, ay - 2), (ax + 2, ay - 8)],
              fill=RED)
    d.text((x + w - 78, y + 10), "-3.7%", font=F_STRIP_B, fill=RED)


def art_gulf(d, x, y, w, h):
    # Sea with a tanker, a flame on deck, and the word GULF.
    d.rectangle([x, y, x + w, y + h], fill=(219, 234, 254))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 130, 190))
    d.line([x + 10, y + h - 10, x + w - 10, y + h - 10],
           fill=(140, 190, 230), width=2)
    # Tanker silhouette.
    sx = x + 30
    d.polygon([(sx, y + h - 16), (sx + 150, y + h - 16),
               (sx + 138, y + h - 6), (sx + 12, y + h - 6)], fill=(40, 50, 66))
    d.rectangle([sx + 92, y + h - 30, sx + 122, y + h - 16], fill=(40, 50, 66))
    d.polygon([(sx + 100, y + h - 30), (sx + 107, y + h - 42),
               (sx + 114, y + h - 30)], fill=(230, 110, 30))
    d.text((x + w - 78, y + h - 34), "GULF", font=F_STRIP_B, fill=WHITE)


def art_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 29, 51))
    for sx, sy in [(x + 8, y + 8), (x + 60, y + 6), (x + 210, y + 10),
                   (x + 250, y + 28), (x + 330, y + 8), (x + 400, y + 30)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    # Mercury with craters.
    cx, cy, r = x + 30, y + h // 2, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 168, 158))
    d.ellipse([cx - 8, cy - 4, cx - 2, cy + 2], fill=(140, 138, 130))
    d.ellipse([cx + 3, cy + 5, cx + 8, cy + 10], fill=(140, 138, 130))
    d.text((x + 56, y + 2), "8 YEARS", font=F_STRIP_B, fill=GOLD)
    d.text((x + 56, y + 21), "10 BILLION KM", font=F_STRIP_B, fill=GOLD)
    # Spacecraft: body with two solar panels.
    px = x + w - 78
    d.rectangle([px, y + 14, px + 16, y + 26], fill=(220, 220, 220))
    d.rectangle([px - 22, y + 16, px - 2, y + 24], fill=(230, 190, 60))
    d.rectangle([px + 18, y + 16, px + 38, y + 24], fill=(230, 190, 60))


ART = {
    "war": art_war,
    "climate": art_climate,
    "mexico": art_mexico,
    "markets": art_markets,
    "gulf": art_gulf,
    "space": art_space,
}


# --- card --------------------------------------------------------------------
def draw_card(d, story, x0, y0, cw, ch):
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=10, fill=CARD)
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + 10], radius=5,
                        fill=story["accent"])
    d.rectangle([x0, y0 + 5, x0 + cw, y0 + 10], fill=story["accent"])
    tx = x0 + 18
    d.text((tx, y0 + 16), story["kicker"], font=F_KICKER,
           fill=story["accent"])
    head = wrap(story["headline"], F_HEAD, cw - 36, max_lines=2)
    hy = y0 + 44
    for line in head:
        d.text((tx, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    body = wrap(story["body"], F_BODY, cw - 36, max_lines=3)
    by = y0 + 112
    for line in body:
        d.text((tx, by), line, font=F_BODY, fill=BODY)
        by += 23
    sx, sy, sw, sh = x0 + 18, y0 + ch - 52, cw - 36, 40
    ART[story["art"]](d, sx, sy, sw, sh)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 128], fill=CREAM)
    d.text((28, 8), "THE WORLD IN ONE DAY", font=F_MASTHEAD, fill=INK)
    d.text((28, 66), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=RED)
    d.text((30, 104), "Six stories from around the world", font=F_SUB,
           fill=MUTED)
    d.rectangle([0, 128, W, 133], fill=RED)

    # Story grid: 2 columns x 3 rows.
    cw, ch = 480, 240
    xs = [24, 520]
    ys = [144, 396, 648]
    for i, story in enumerate(STORIES):
        draw_card(d, story, xs[i % 2], ys[i // 2], cw, ch)

    # Also-today strip.
    d.rounded_rectangle([24, 892, 1000, 956], radius=10, fill=CARD)
    d.text((40, 898), "ALSO TODAY:", font=F_STRIP_B, fill=RED)
    d.text((40, 917), ALSO_TODAY[0], font=F_STRIP, fill=BODY)
    d.text((40, 935), ALSO_TODAY[1], font=F_STRIP, fill=BODY)

    # Footer.
    d.text((24, 968), "Drawn from news reported on Saturday 21 November 2026.",
           font=F_FOOT, fill=(180, 190, 205))
    foot_r = "ONE DAY  ·  ONE PICTURE"
    d.text((1000 - F_FOOT.getlength(foot_r), 968), foot_r, font=F_FOOT,
           fill=(180, 190, 205))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
