#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news poster.

Build-time only: renders entry.png (1024x1024, RGB) with PIL.
Everything is drawn from primitives; no downloaded images, no network,
no randomness, no clock -- the output bytes are fully deterministic.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
NAVY = (15, 27, 45)
CREAM = (245, 239, 224)
INK = (20, 32, 46)
RED = (192, 57, 43)
WHITE = (255, 255, 255)
PANEL_LINE = (216, 222, 230)
GREY = (90, 100, 114)
SKY = (38, 62, 96)
GOLD = (212, 160, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 54)
F_DATE = font("DejaVuSans-Bold.ttf", 46)
F_SUB = font("DejaVuSans.ttf", 21)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 18)
F_STRIP = font("DejaVuSans-Bold.ttf", 18)
F_STRIP_BODY = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 15)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_panel(draw, x, y, w, h, accent, kicker, headline, body, pict):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=WHITE, outline=PANEL_LINE, width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)
    draw.text((x + 18, y + 18), kicker, font=F_KICKER, fill=accent)
    tx = x + 18
    tw = w - 36
    lines = wrap(draw, headline, F_HEAD, tw)[:2]
    ly = y + 44
    for ln in lines:
        draw.text((tx, ly), ln, font=F_HEAD, fill=INK)
        ly += 32
    ly = y + 112
    for ln in wrap(draw, body, F_BODY, tw)[:3]:
        draw.text((tx, ly), ln, font=F_BODY, fill=(52, 64, 80))
        ly += 22
    pict(draw, x + 18, y + h - 56, w - 36, 44)


# ---- pictograms (simple flat drawings, one per story) -------------------

def pic_kryvyi(draw, x, y, w, h):
    # night sky, apartment blocks, one hit: jagged break, smoke, burst
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    for cx, cy, r in [(x + 40, y + 10, 2), (x + 120, y + 18, 2),
                      (x + 210, y + 8, 2), (x + 330, y + 14, 2)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    base = y + h - 4
    blocks = [(x + 14, 30), (x + 64, 38), (x + 150, 26), (x + 200, 36),
              (x + 250, 30), (x + 300, 40)]
    for bx, bh in blocks:
        draw.rectangle([bx, base - bh, bx + 36, base], fill=(120, 140, 168))
        for wy in range(base - bh + 6, base - 4, 10):
            draw.rectangle([bx + 5, wy, bx + 12, wy + 5], fill=(255, 214, 90))
            draw.rectangle([bx + 20, wy, bx + 27, wy + 5], fill=(255, 214, 90))
    # hit block: jagged top, smoke, orange burst
    bx, bh = blocks[2]
    draw.polygon([(bx, base - bh), (bx + 12, base - bh - 9),
                  (bx + 22, base - bh), (bx + 36, base - bh - 7),
                  (bx + 36, base - bh + 4), (bx, base - bh + 4)],
                 fill=(200, 120, 90))
    for sx, sy, sr in [(bx + 8, base - bh - 2, 3), (bx + 24, base - bh - 6, 4),
                       (bx + 16, base - bh - 10, 3)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 200))
    ex, ey = bx + 18, base - 6
    for dx, dy in [(0, -8), (7, -4), (8, 4), (0, 8), (-8, 4), (-7, -4)]:
        draw.line([ex, ey, ex + dx, ey + dy], fill=(255, 120, 40), width=2)


def pic_cop(draw, x, y, w, h):
    # globe on the left, clock on the right, "OVERTIME" between
    draw.rectangle([x, y, x + w, y + h], fill=(226, 240, 232))
    cx, cy, r = x + 46, y + h // 2, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 125, 190))
    draw.ellipse([cx - 12, cy - 10, cx - 2, cy - 2], fill=(74, 160, 90))
    draw.ellipse([cx + 2, cy + 4, cx + 12, cy + 12], fill=(74, 160, 90))
    draw.ellipse([cx - 6, cy + 8, cx + 4, cy + 14], fill=(74, 160, 90))
    # clock: running late
    kx, ky, kr = x + w - 46, y + h // 2, 19
    draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE,
                 outline=(60, 70, 84), width=3)
    draw.line([kx, ky, kx, ky - 12], fill=(60, 70, 84), width=2)
    draw.line([kx, ky, kx + 10, ky + 5], fill=(60, 70, 84), width=2)
    draw.text((x + 92, y + 12), "OVERTIME", font=F_STRIP, fill=(46, 125, 60))
    draw.text((x + 92, y + 30), "no deal yet", font=F_STRIP_BODY,
              fill=(52, 64, 80))


def pic_cartel(draw, x, y, w, h):
    # police shield with star, "WANTED" banner
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    sx, sy = x + 40, y + 2
    draw.polygon([(sx, sy), (sx + 40, sy), (sx + 40, sy + 26),
                  (sx + 20, sy + 40), (sx, sy + 26)], fill=(38, 62, 96),
                 outline=GOLD, width=2)
    # five-point star
    cx, cy = sx + 20, sy + 17
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 10 if i % 2 == 0 else 4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=GOLD)
    draw.text((sx + 52, y + 6), "WANTED", font=F_STRIP, fill=(178, 34, 52))
    draw.text((sx + 52, y + 26), "FBI TOP 10", font=F_STRIP_BODY, fill=INK)
    # handcuffs: two rings joined by a link
    for hx in (x + w - 120, x + w - 72):
        draw.ellipse([hx, y + 6, hx + 34, y + 38], outline=(60, 70, 84),
                     width=4)
    draw.line([x + w - 86, y + 22, x + w - 72, y + 22], fill=(60, 70, 84),
              width=3)


def pic_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(248, 232, 230))
    pts = [(x + 10, y + 8), (x + 70, y + 12), (x + 120, y + 10),
           (x + 180, y + 22), (x + 240, y + 28), (x + 300, y + h - 10)]
    draw.line(pts, fill=RED, width=4)
    draw.polygon([(x + 300, y + h - 10), (x + 300, y + h - 20),
                  (x + 312, y + h - 6), (x + 292, y + h - 4)], fill=RED)
    for bx, bh in [(20, 12), (70, 18), (120, 14), (170, 24), (220, 30), (270, 40)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + 26, y + h - 4],
                       fill=(200, 120, 110))
    draw.text((x + w - 108, y + 4), "-3.7%", font=F_STRIP, fill=RED)


def pic_gulf(draw, x, y, w, h):
    # sea, burning platform, jet overhead
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 244))
    draw.rectangle([x, y + 26, x + w, y + h], fill=(46, 125, 190))
    for wy in (y + 30, y + 36):
        draw.line([(x + 10, wy), (x + 60, wy), (x + 110, wy),
                   (x + 160, wy), (x + 210, wy), (x + 260, wy),
                   (x + 310, wy), (x + 360, wy), (x + w - 10, wy)],
                  fill=(120, 190, 230), width=2)
    # platform with flame
    px = x + 60
    draw.rectangle([px, y + 22, px + 56, y + 34], fill=(60, 70, 84))
    draw.rectangle([px + 8, y + 12, px + 14, y + 22], fill=(60, 70, 84))
    fx, fy = px + 28, y + 8
    draw.polygon([(fx, fy - 8), (fx + 8, fy + 2), (fx + 4, fy + 6),
                  (fx - 4, fy + 6), (fx - 8, fy + 2)], fill=(255, 120, 40))
    # jet silhouette
    jx, jy = x + w - 130, y + 2
    draw.polygon([(jx, jy + 6), (jx + 60, jy + 6), (jx + 72, jy + 9),
                  (jx + 60, jy + 12), (jx, jy + 12), (jx + 10, jy + 9)],
                 fill=(60, 70, 84))
    draw.polygon([(jx + 24, jy + 6), (jx + 34, jy - 4), (jx + 40, jy + 6)],
                 fill=(60, 70, 84))
    draw.text((x + w - 130, y + h - 20), "GULF", font=F_STRIP, fill=WHITE)


def pic_mercury(draw, x, y, w, h):
    # cratered Mercury, spacecraft with solar panels, sun rays
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    for cx, cy, r in [(x + 300, y + 8, 2), (x + 340, y + 20, 2),
                      (x + 260, y + 30, 2), (x + 380, y + 12, 2)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    # sun rays top-left
    sx, sy = x + 16, y + 4
    for dx, dy in [(10, 0), (7, 7), (0, 10), (-7, 7), (10, 10)]:
        draw.line([sx, sy, sx + dx, sy + dy], fill=GOLD, width=2)
    draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=GOLD)
    # Mercury
    cx, cy, r = x + 70, y + h // 2, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 160, 148))
    for kx, ky, kr in [(cx - 8, cy - 6, 4), (cx + 8, cy + 4, 3),
                       (cx + 2, cy - 10, 2), (cx - 4, cy + 10, 2)]:
        draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(140, 132, 120))
    # spacecraft: body + two solar panels (low, clear of the label)
    bx, by = x + w - 140, y + 24
    draw.rectangle([bx, by, bx + 26, by + 16], fill=(200, 200, 200),
                   outline=(90, 100, 114))
    draw.rectangle([bx - 34, by + 3, bx, by + 13], fill=(38, 62, 96),
                   outline=GOLD)
    draw.rectangle([bx + 26, by + 3, bx + 60, by + 13], fill=(38, 62, 96),
                   outline=GOLD)
    draw.text((x + 110, y + 4), "8 YEARS",
              font=F_STRIP, fill=(255, 214, 90))
    draw.text((x + 110, y + 24), "10 BILLION KM",
              font=F_STRIP, fill=(255, 214, 90))


PANELS = [
    ((192, 57, 43), "WAR  ·  KRYVYI RIH",
     "Russian missiles hit Zelenskyy's hometown",
     "Ballistic missiles struck Kryvyi Rih on Friday night, killing a "
     "7-year-old boy and a 20-year-old woman and wounding 60, six of "
     "them children.",
     pic_kryvyi),
    ((46, 125, 60), "CLIMATE  ·  COP31",
     "COP31 talks run into overtime",
     "The Antalya summit overran its Friday deadline with no deal yet. "
     "The draft text drops any call to phase out fossil fuels.",
     pic_cop),
    ((14, 124, 123), "MEXICO  ·  CARTELS",
     "Mexico captures \u201cEl Chapo Isidro\u201d",
     "Troops seized FBI most-wanted boss Fausto Isidro Meza Flores in "
     "Sinaloa overnight, with US help. Violence flared after the "
     "arrest.",
     pic_cartel),
    ((142, 31, 31), "MARKETS  ·  ECONOMY",
     "AI sell-off drags markets down",
     "The S&P 500 fell 3.7% on Friday and Japan\u2019s Nikkei slid 5.1% "
     "as chip shares plunged on doubts the AI boom will pay off.",
     pic_markets),
    ((178, 106, 0), "MIDDLE EAST  ·  THE GULF",
     "Gulf tensions flare as Iran claims US jet hit",
     "Bahrain says an Iranian attack set a civilian industrial site "
     "ablaze. Tehran claims it damaged a US F-16 and shot down a drone "
     "over the Gulf.",
     pic_gulf),
    ((31, 78, 121), "SPACE  ·  MERCURY",
     "BepiColombo reaches Mercury",
     "After an eight-year journey, the ESA\u2013JAXA spacecraft entered "
     "orbit around the innermost planet. Its two orbiters separate in "
     "December.",
     pic_mercury),
]

STRIP_LINES = [
    "Magnitude 6.8 quake off Timor-Leste, no tsunami threat  ·  "
    "EU approves \u20ac1bn more aid for Ukraine",
    "Russian cargo ship ablaze in the Gulf of Finland  ·  "
    "UN to draft AI-weapons rules by 2028",
]


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=CREAM)
    d.rectangle([0, 148, W, 154], fill=RED)
    d.text((24, 10), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.text((24, 74), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=RED)
    d.text((24, 126), "Six stories from around the world",
           font=F_SUB, fill=GREY)

    # ---- story grid ----------------------------------------------------
    gx, gy = 24, 166
    pw, ph = 480, 238
    gap = 14
    for i, (accent, kicker, head, body, pict) in enumerate(PANELS):
        col, row = i % 2, i // 2
        draw_panel(d, gx + col * (pw + gap), gy + row * (ph + gap),
                   pw, ph, accent, kicker, head, body, pict)

    # ---- also-today strip ----------------------------------------------
    sy = 166 + 3 * ph + 2 * gap + 10
    d.rounded_rectangle([24, sy, W - 24, sy + 72], radius=8, fill=WHITE)
    d.text((40, sy + 8), "ALSO TODAY:", font=F_STRIP, fill=RED)
    d.text((40, sy + 30), STRIP_LINES[0], font=F_STRIP_BODY, fill=INK)
    d.text((40, sy + 52), STRIP_LINES[1], font=F_STRIP_BODY, fill=INK)

    # ---- footer ---------------------------------------------------------
    d.text((24, H - 24),
           "Drawn from news reported on Saturday 21 November 2026.",
           font=F_FOOT, fill=(150, 164, 180))
    d.text((W - 24 - d.textlength("ONE DAY  ·  ONE PICTURE", font=F_FOOT),
            H - 26), "ONE DAY  ·  ONE PICTURE", font=F_FOOT,
           fill=(150, 164, 180))

    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
