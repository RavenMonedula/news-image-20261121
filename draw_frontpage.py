#!/usr/bin/env python3
"""Front page for news-image-20261121 — Saturday 21 November 2026.
Newspaper front page: light paper header, stat strip, region bar,
3 illustrated heroes, 12 medium stories in a 6x2 grid, dotted world
map with numbered pins, 20 more stories, a date-check box, footer.
35 stories total. All facts verified live 2026-11-21 from Reuters /
AP / AFP / USGS / ESA. Own headlines, decks and drawings; the
newspaper-front-page formula is followed, never another entry's
content. Renders repo/entry.png (1024x1024, <1 MiB) with PIL."""
from PIL import Image, ImageDraw, ImageFont
import math, os

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MX = 28
CW = W - 2 * MX

PAPER = (247, 243, 232)
INK = (26, 26, 26)
MUTED = (88, 84, 74)
RED = (178, 34, 41)
RULE = (150, 142, 125)
NAVY = (28, 41, 71)
NAVY_D = (20, 28, 48)
CREAM = (232, 224, 200)
TEAL = (0, 128, 128)
GOLD = (198, 158, 40)


def load_font(name, size):
    for base in (os.path.join(BASE, "fonts"),
                 "/usr/share/fonts/truetype/dejavu"):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TOP = load_font("DejaVuSans-Bold.ttf", 11)
F_TITLE = load_font("DejaVuSerif-Bold.ttf", 44)
F_SUB = load_font("DejaVuSerif.ttf", 13)
F_CAP = load_font("DejaVuSans-Bold.ttf", 8)
F_KICK = load_font("DejaVuSans-Bold.ttf", 10)
F_KICK2 = load_font("DejaVuSans-Bold.ttf", 8)
F_HERO_H = load_font("DejaVuSerif-Bold.ttf", 16)
F_MED_H = load_font("DejaVuSerif-Bold.ttf", 12)
F_NUM = load_font("DejaVuSans-Bold.ttf", 12)
F_NUM2 = load_font("DejaVuSans-Bold.ttf", 10)
F_DECK = load_font("DejaVuSans.ttf", 11)
F_DECK2 = load_font("DejaVuSans.ttf", 9)
F_SECT = load_font("DejaVuSans-Bold.ttf", 11)
F_BIGN = load_font("DejaVuSerif-Bold.ttf", 20)
F_BIGL = load_font("DejaVuSans.ttf", 9)
F_ALSO_N = load_font("DejaVuSans-Bold.ttf", 8)
F_ALSO_B = load_font("DejaVuSans-Bold.ttf", 8)
F_ALSO = load_font("DejaVuSans.ttf", 8)
F_MAPN = load_font("DejaVuSans-Bold.ttf", 10)
F_FOOT = load_font("DejaVuSans.ttf", 8)
F_MAPC = load_font("DejaVuSans.ttf", 9)
F_REG = load_font("DejaVuSans-Bold.ttf", 9)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def textlines(x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def circle_num(cx, cy, r, num, fnt):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    bb = d.textbbox((0, 0), num, font=fnt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), num, font=fnt,
           fill=(255, 255, 255))


# ---------------- HEADER ----------------
d.text((MX, 12), "THE WORLD IN ONE DAY", font=F_TOP, fill=INK)
t = "SATURDAY'S NEWS \u00b7 ONE PAGE \u00b7 35 STORIES"
d.text((W - MX - d.textlength(t, font=F_TOP), 12), t, font=F_TOP, fill=INK)
d.line([MX, 30, W - MX, 30], fill=INK, width=2)
d.text((MX, 38), "Saturday 21 November 2026", font=F_TITLE, fill=INK)
d.text((MX, 92), "COP31 runs into overtime \u00b7 Three missiles downed over Riyadh "
                 "\u00b7 BepiColombo at Mercury \u00b7 Peru quake",
       font=F_SUB, fill=RED)
d.line([MX, 112, W - MX, 112], fill=RULE, width=1)

# ---------------- STAT STRIP (6 numbers) ----------------
STATS = [
    ("3", "missiles downed over Riyadh"),
    ("0", "climate deal agreed at COP31"),
    ("6.7", "Peru quake magnitude"),
    ("2", "killed in Kryvyi Rih strike"),
    ("8 yrs", "BepiColombo's voyage to Mercury"),
    ("124*", "Rahul at tea, India reply"),
]
SX = [MX, 190, 352, 514, 676, 838]
for (num, lab), sx in zip(STATS, SX):
    d.text((sx, 120), num, font=F_BIGN, fill=RED)
    textlines(sx, 144, wrap(lab, F_BIGL, 150), F_BIGL, MUTED, 11)
d.line([MX, 170, W - MX, 170], fill=RULE, width=1)

# ---------------- REGION BAR ----------------
REGIONS = [
    ("ASIA", 7, (122, 63, 146)),
    ("MIDDLE EAST", 5, (180, 132, 26)),
    ("EUROPE", 7, (0, 74, 137)),
    ("AFRICA", 2, (122, 74, 26)),
    ("AMERICAS", 9, (0, 128, 128)),
    ("OCEANIA", 4, (46, 125, 90)),
    ("SPACE", 1, (58, 58, 58)),
]
SEG_W = CW / 7.0
ry = 176
for i, (name, n, col) in enumerate(REGIONS):
    x0 = MX + i * SEG_W
    d.rectangle([x0, ry, x0 + SEG_W - 1, ry + 18], fill=col)
    label = "%s %d" % (name, n)
    tw = d.textlength(label, font=F_REG)
    d.text((x0 + (SEG_W - tw) / 2, ry + 4), label, font=F_REG,
           fill=(255, 255, 255))

# ---------------- HERO ILLUSTRATIONS (312x90) ----------------
def hero_cop31(w, h):
    s = Image.new("RGB", (w, h), (198, 224, 218))
    dd = ImageDraw.Draw(s)
    # globe, left
    cx, cy, r = 92, h // 2 + 2, 40
    dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 110, 170))
    dd.ellipse([cx - 26, cy - 22, cx - 2, cy + 2], fill=(70, 165, 95))
    dd.ellipse([cx + 4, cy + 6, cx + 26, cy + 26], fill=(70, 165, 95))
    dd.ellipse([cx + 12, cy - 28, cx + 28, cy - 10], fill=(70, 165, 95))
    # red tag, top right
    dd.rectangle([w - 132, 6, w - 6, 22], fill=RED)
    dd.text((w - 126, 9), "1.5\u00b0C LIMIT PASSED",
            font=load_font("DejaVuSans-Bold.ttf", 8), fill=(255, 255, 255))
    # thermometer, right, below the tag
    tx = w - 62
    dd.rounded_rectangle([tx, 28, tx + 22, h - 22], radius=10,
                         fill=(255, 255, 255), outline=(150, 150, 150))
    dd.rectangle([tx + 8, 36, tx + 14, h - 30], fill=RED)
    dd.ellipse([tx - 2, h - 34, tx + 24, h - 8], fill=RED)
    return s


def hero_riyadh(w, h):
    s = Image.new("RGB", (w, h), (16, 24, 48))
    dd = ImageDraw.Draw(s)
    # crescent moon, top right
    dd.ellipse([w - 52, 8, w - 20, 40], fill=(240, 220, 140))
    dd.ellipse([w - 44, 4, w - 12, 36], fill=(16, 24, 48))
    # skyline with lit windows
    heights = [34, 52, 44, 62, 38, 56, 48, 66, 40, 54]
    bw = w // 10
    for i, bh in enumerate(heights):
        x0 = i * bw
        dd.rectangle([x0 + 2, h - bh, x0 + bw - 2, h], fill=(8, 12, 28))
        for wy in range(h - bh + 6, h - 6, 10):
            for wx in range(x0 + 6, x0 + bw - 6, 9):
                if (i * 7 + wy) % 3 == 0:
                    dd.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    # three interceptor trails, dashed arcs with starbursts
    for (x0, y0, x1, y1) in [(30, h - 10, 120, 18), (120, h - 10, 200, 12),
                             (210, h - 10, 280, 22)]:
        ccx = (x0 + x1) // 2
        ccy = min(y0, y1) - 30
        pts = []
        for k in range(13):
            tt = k / 12.0
            px = (1 - tt) ** 2 * x0 + 2 * (1 - tt) * tt * ccx + tt ** 2 * x1
            py = (1 - tt) ** 2 * y0 + 2 * (1 - tt) * tt * ccy + tt ** 2 * y1
            pts.append((px, py))
        for j in range(0, len(pts) - 1, 2):
            dd.line([pts[j], pts[j + 1]], fill=(255, 150, 40), width=2)
        ex, ey = pts[-1]
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            dd.line([(ex, ey), (ex + 9 * math.cos(a), ey + 9 * math.sin(a))],
                    fill=(255, 220, 0), width=2)
    return s


def hero_peru(w, h):
    s = Image.new("RGB", (w, h), (235, 214, 178))
    dd = ImageDraw.Draw(s)
    # Andes peaks with snow caps
    dd.polygon([(0, h), (70, 18), (150, h)], fill=(120, 85, 50))
    dd.polygon([(90, h), (180, 8), (280, h)], fill=(150, 105, 60))
    dd.polygon([(200, h), (262, 30), (312, h)], fill=(120, 85, 50))
    dd.polygon([(62, 30), (70, 18), (78, 30), (70, 36)], fill=(255, 255, 255))
    dd.polygon([(170, 22), (180, 8), (190, 22), (180, 28)],
               fill=(255, 255, 255))
    # red seismograph trace across the middle
    pts = [(8, 62), (30, 62), (40, 48), (50, 76), (60, 62), (80, 62),
           (92, 40), (104, 84), (116, 62), (140, 62), (152, 52), (164, 72),
           (176, 62), (200, 62), (212, 44), (224, 80), (236, 62), (260, 62),
           (272, 54), (284, 70), (296, 62), (308, 62)]
    for i in range(len(pts) - 1):
        dd.line([pts[i], pts[i + 1]], fill=RED, width=2)
    dd.rectangle([8, h - 20, 116, h - 4], fill=NAVY_D)
    dd.text((14, h - 17), "M 6.7 \u00b7 108 KM DEEP",
            font=load_font("DejaVuSans-Bold.ttf", 8), fill=(255, 255, 255))
    return s


# ---------------- HEROES (1-3) ----------------
HEROES = [
    dict(fn=hero_cop31, cap="ANTALYA \u00b7 COP31",
         kick="ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE \u00b7 Reuters, AP",
         head="COP31 runs into overtime with no deal",
         deck="Talks pass their deadline as a third draft is due Saturday "
              "morning; fossil-fuel language is out and nearly 200 "
              "countries stay split."),
    dict(fn=hero_riyadh, cap="RIYADH \u00b7 AIR DEFENCE",
         kick="RIYADH, SAUDI ARABIA \u00b7 CONFLICT \u00b7 Reuters, AFP",
         head="Coalition downs three Houthi missiles over Riyadh",
         deck="Air defences destroy three ballistic missiles fired at the "
              "capital early on Saturday, the second attack on Riyadh in "
              "days."),
    dict(fn=hero_peru, cap="JUN\u00cdN \u00b7 00:09 UTC",
         kick="JUN\u00cdN, PERU \u00b7 QUAKE \u00b7 USGS, AFP",
         head="Magnitude 6.7 quake shakes central Peru",
         deck="The tremor hits at 00:09 UTC, 34 km north of Jun\u00edn, "
              "108 km deep; felt in Lima, no deaths reported."),
]
HW = 312
HG = 16
HX = [MX, MX + HW + HG, MX + 2 * (HW + HG)]
HY_IMG = 202
HIMG_H = 90
hero_wrapped = [(wrap(hh["head"], F_HERO_H, HW),
                 wrap(hh["deck"], F_DECK, HW)) for hh in HEROES]
max_head = max(len(hl) for hl, dl in hero_wrapped)
max_deck = max(len(dl) for hl, dl in hero_wrapped)
for i, hh in enumerate(HEROES):
    x = HX[i]
    im = hh["fn"](HW, HIMG_H)
    img.paste(im, (x, HY_IMG))
    d.rectangle([x, HY_IMG + HIMG_H - 16, x + HW, HY_IMG + HIMG_H], fill=NAVY_D)
    cw = d.textlength(hh["cap"], font=F_CAP)
    d.text((x + (HW - cw) / 2, HY_IMG + HIMG_H - 13), hh["cap"], font=F_CAP,
           fill=(255, 255, 255))
    ky = HY_IMG + HIMG_H + 8
    circle_num(x + 11, ky + 11, 11, str(i + 1), F_NUM)
    d.text((x + 26, ky + 2), hh["kick"], font=F_KICK, fill=RED)
    hy = ky + 26
    hl, dl = hero_wrapped[i]
    textlines(x, hy, hl, F_HERO_H, INK, 20)
    dy = hy + max_head * 20 + 6
    textlines(x, dy, dl, F_DECK, MUTED, 13)
heroes_end = hy + max_head * 20 + 6 + max_deck * 13
d.line([MX, heroes_end + 8, W - MX, heroes_end + 8], fill=RULE, width=1)

# ---------------- MEDIUM ILLUSTRATIONS (153x28 strips) ----------------
def med_burst(w, h):
    s = Image.new("RGB", (w, h), (20, 28, 48))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, 12, 60, h], fill=(8, 12, 28))
    for wy in range(16, h - 2, 7):
        for wx in range(6, 54, 10):
            if (wx + wy) % 4 == 0:
                dd.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 210, 90))
    cx, cy = 112, 15
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        dd.line([(cx, cy), (cx + 18 * math.cos(a), cy + 11 * math.sin(a))],
                fill=(255, 120, 0), width=2)
    dd.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 220, 0))
    return s


def med_mercury(w, h):
    s = Image.new("RGB", (w, h), (12, 12, 24))
    dd = ImageDraw.Draw(s)
    for sx, sy in ((14, 6), (40, 20), (140, 8), (126, 22), (70, 4)):
        dd.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    cx, cy, r = 76, 15, 13
    dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    for (ox, oy, orr) in ((-5, -4, 3), (5, 3, 4), (-2, 6, 2)):
        dd.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                   fill=(110, 110, 110))
    dd.rectangle([cx + r + 2, cy - 4, cx + r + 12, cy + 4], fill=(0, 128, 128))
    dd.rectangle([cx + r + 12, cy - 7, cx + r + 16, cy + 7], fill=(200, 200, 200))
    return s


def med_cricket(w, h):
    s = Image.new("RGB", (w, h), (0, 100, 60))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, h - 6, w, h], fill=(200, 180, 120))
    dd.rectangle([30, 6, 37, 20], fill=(220, 190, 140))
    dd.rectangle([30, 20, 44, 24], fill=(160, 120, 80))
    dd.ellipse([52, 8, 66, 22], fill=RED)
    dd.text((72, 8), "124*", font=load_font("DejaVuSans-Bold.ttf", 12),
            fill=(255, 255, 255))
    return s


def med_capitol(w, h):
    s = Image.new("RGB", (w, h), (180, 200, 225))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, h - 4, w, h], fill=(120, 140, 170))
    dd.ellipse([w // 2 - 16, 2, w // 2 + 16, 14], fill=(245, 240, 225))
    dd.rectangle([w // 2 - 22, 12, w // 2 + 22, h - 4], fill=(245, 240, 225))
    for ccx in range(w // 2 - 17, w // 2 + 18, 10):
        dd.rectangle([ccx - 2, 14, ccx + 2, h - 4], fill=(200, 195, 180))
    return s


def med_eu(w, h):
    s = Image.new("RGB", (w, h), (0, 51, 153))
    dd = ImageDraw.Draw(s)
    cx, cy = w // 2, h // 2
    for k in range(12):
        a = -math.pi / 2 + k * (2 * math.pi / 12)
        dd.ellipse([cx + 26 * math.cos(a) - 2, cy + 10 * math.sin(a) - 2,
                    cx + 26 * math.cos(a) + 2, cy + 10 * math.sin(a) + 2],
                   fill=(255, 204, 0))
    dd.text((cx - 6, cy - 8), "\u20ac",
            font=load_font("DejaVuSans-Bold.ttf", 14), fill=(255, 255, 255))
    return s


def med_boat(w, h):
    s = Image.new("RGB", (w, h), (0, 74, 137))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, h - 8, w, h], fill=(0, 50, 90))
    dd.polygon([(52, 8), (138, 20), (128, 26), (62, 16)], fill=(120, 80, 40))
    dd.rectangle([90, 2, 93, 10], fill=(200, 200, 200))
    for wx in range(0, w, 20):
        dd.arc([wx, h - 6, wx + 20, h + 6], start=180, end=360,
               fill=(255, 255, 255), width=2)
    return s


def med_port(w, h):
    s = Image.new("RGB", (w, h), (240, 180, 110))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, h - 8, w, h], fill=(60, 60, 60))
    for i, col in enumerate([(178, 34, 41), (0, 100, 60), (0, 74, 137)]):
        dd.rectangle([10 + i * 26, h - 18, 32 + i * 26, h - 8], fill=col)
    dd.rectangle([100, 4, 104, h - 8], fill=(40, 40, 40))
    dd.line([(100, 4), (140, 4)], fill=(40, 40, 40), width=3)
    dd.line([(140, 4), (140, 12)], fill=(40, 40, 40), width=2)
    dd.rectangle([134, 12, 148, 18], fill=(40, 40, 40))
    return s


def med_march(w, h):
    s = Image.new("RGB", (w, h), (232, 224, 200))
    dd = ImageDraw.Draw(s)
    cols = [(178, 34, 41), (0, 128, 128), (0, 74, 137), (198, 158, 40)]
    for i in range(9):
        cx = 14 + i * 16
        dd.ellipse([cx - 4, 16, cx + 4, 24], fill=cols[i % 4])
        dd.rectangle([cx - 1, 8, cx + 1, 16], fill=(60, 60, 60))
        dd.rectangle([cx - 6, 4, cx + 6, 9], fill=cols[i % 4])
    return s


def med_court(w, h):
    s = Image.new("RGB", (w, h), (200, 210, 225))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, h - 4, w, h], fill=(140, 150, 165))
    dd.polygon([(w // 2 - 40, 10), (w // 2, 2), (w // 2 + 40, 10)],
               fill=(120, 110, 90))
    for ccx in range(w // 2 - 30, w // 2 + 31, 15):
        dd.rectangle([ccx - 3, 10, ccx + 3, h - 4], fill=(245, 240, 225))
    return s


def med_plane(w, h):
    s = Image.new("RGB", (w, h), (180, 210, 235))
    dd = ImageDraw.Draw(s)
    dd.ellipse([20, 8, 120, 20], fill=(255, 255, 255))
    dd.polygon([(100, 8), (138, 4), (138, 12)], fill=(255, 255, 255))
    dd.polygon([(60, 20), (80, 26), (70, 20)], fill=(220, 220, 220))
    dd.polygon([(96, 20), (112, 26), (104, 20)], fill=(220, 220, 220))
    dd.line([(30, 22), (18, 27)], fill=(178, 34, 41), width=2)
    dd.line([(60, 22), (52, 27)], fill=(178, 34, 41), width=2)
    return s


def med_train(w, h):
    s = Image.new("RGB", (w, h), (220, 220, 210))
    dd = ImageDraw.Draw(s)
    dd.rectangle([0, h - 6, w, h], fill=(90, 90, 90))
    for i in range(4):
        x0 = 8 + i * 36
        dd.rectangle([x0, 8, x0 + 30, 20], fill=(0, 74, 137))
        dd.rectangle([x0 + 4, 11, x0 + 12, 17], fill=(180, 220, 240))
        dd.rectangle([x0 + 18, 11, x0 + 26, 17], fill=(180, 220, 240))
    dd.polygon([(116, 8), (146, 8), (140, 20), (122, 20)], fill=(178, 34, 41))
    return s


def med_f1(w, h):
    s = Image.new("RGB", (w, h), (16, 16, 28))
    dd = ImageDraw.Draw(s)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                dd.rectangle([8 + c * 8, 4 + r * 8, 16 + c * 8, 12 + r * 8],
                             fill=(255, 255, 255))
    dd.polygon([(56, 20), (140, 20), (132, 26), (64, 26)], fill=(200, 0, 0))
    dd.ellipse([70, 14, 82, 24], fill=(30, 30, 30))
    dd.ellipse([118, 14, 130, 24], fill=(30, 30, 30))
    dd.text((100, 4), "1:34.041", font=load_font("DejaVuSans-Bold.ttf", 9),
            fill=(255, 220, 0))
    return s


MED_ICONS = [med_burst, med_mercury, med_cricket, med_capitol, med_eu,
             med_boat, med_port, med_march, med_court, med_plane,
             med_train, med_f1]
MED = [
    ("KRYVYI RIH \u00b7 WAR", "Overnight strike kills 2, injures 42",
     "A seven-year-old boy and a 20-year-old paramedic are killed in a "
     "Russian double-tap strike; 27 of the hurt are in serious condition."),
    ("MERCURY \u00b7 SPACE", "BepiColombo reaches Mercury after eight years",
     "The ESA-JAXA craft fires its thrusters at 19:24 CET tonight to be "
     "caught by Mercury's gravity, the first mission to put two orbiters "
     "there at once."),
    ("WELLINGTON \u00b7 CRICKET", "Rahul hits 124* as India reply to 368",
     "The opener reaches his century off 207 balls and becomes the first "
     "Indian opener with Test hundreds in all four SENA countries; India "
     "344 for 2 at tea."),
    ("WASHINGTON \u00b7 DIPLOMACY", "Trump upbeat on Putin talks",
     "The president says there is a real good chance of a deal after talks "
     "with Putin; Kyiv says it struck three Russian missile launch "
     "systems."),
    ("BRUSSELS \u00b7 EUROPE", "UK, EU agree Brexit reset",
     "The bloc completes its largest-ever reforms payment to Kyiv as the "
     "two sides agree 100,000 youth places each way."),
    ("BAYELSA \u00b7 DISASTER", "Funeral boat capsizes, at least 4 dead",
     "A boat carrying mourners overturns in Bayelsa state; rescue teams "
     "are still searching."),
    ("HODEIDAH \u00b7 WAR", "Strikes hit Hodeidah port",
     "Civilians are told to leave the port area as the coalition hits "
     "Houthi targets; the UN warns aid lifelines are at risk."),
    ("EUROPE \u00b7 PROTEST", "Youth march across Europe",
     "Young people march in 400 cities against the far right and for "
     "climate action."),
    ("LOS ANGELES \u00b7 COURTS", "LA fire suspect found guilty",
     "A jury convicts a man of starting the deadly Palisades fire after "
     "a retrial."),
    ("DAVAO \u00b7 AVIATION", "Air Niugini jet lands, 146 safe",
     "A Boeing 767 diverts to Davao after an engine fire warning; 137 "
     "passengers and nine crew leave by slides, none hurt."),
    ("SOUTH KOREA \u00b7 RAIL", "Train derails, five cars off the track",
     "Five of 21 freight cars leave the rails; no injuries are reported."),
    ("LAS VEGAS \u00b7 FORMULA 1", "Russell fastest in final Las Vegas practice",
     "George Russell sets 1:34.041 in a damp, messy session; qualifying "
     "runs under the lights on Saturday."),
]
MBW = 153
MGAP = 10
MROW_GAP = 12
med_wrapped = [(wrap(hd, F_MED_H, MBW), wrap(dc, F_DECK2, MBW))
               for (kk, hd, dc) in MED]
med_y = heroes_end + 16
row_tops = []
for r in range(2):
    row_tops.append(med_y)
    row_h = 0
    for c in range(6):
        i = r * 6 + c
        hl, dl = med_wrapped[i]
        bh = 28 + 4 + 11 + len(hl) * 14 + 3 + len(dl) * 11 + 2
        row_h = max(row_h, bh)
    med_y += row_h + MROW_GAP
med_end = med_y - MROW_GAP
for i, (kick, head, deck) in enumerate(MED):
    r, c = divmod(i, 6)
    x = MX + c * (MBW + MGAP)
    y = row_tops[r]
    img.paste(MED_ICONS[i](MBW, 28), (x, y))
    ky = y + 32
    circle_num(x + 9, ky + 8, 9, str(i + 4), F_NUM2)
    d.text((x + 22, ky), kick, font=F_KICK2, fill=RED)
    hy = ky + 14
    hl, dl = med_wrapped[i]
    textlines(x, hy, hl, F_MED_H, INK, 14)
    dy = hy + len(hl) * 14 + 3
    textlines(x, dy, dl, F_DECK2, MUTED, 11)
d.line([MX, med_end + 8, W - MX, med_end + 8], fill=RULE, width=1)

# ---------------- BOTTOM: DOTTED MAP + ALSO ----------------
bot_y = med_end + 16
d.text((MX, bot_y), "WHERE IT HAPPENED", font=F_SECT, fill=INK)
AX = 344
AW = 652
d.text((AX, bot_y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 20 MORE STORIES",
       font=F_SECT, fill=INK)
d.rectangle([AX, bot_y + 14, AX + AW, bot_y + 16], fill=RED)
MAP_X, MAP_Y, MAP_W, MAP_H = MX, bot_y + 22, 300, 130
LAT_TOP, LAT_BOT = 80.0, -60.0
# dotted world map: land cells of the downsampled worldmap become dots
wm = Image.open(os.path.join(BASE, "worldmap.png")).convert("RGB")
wm_small = wm.resize((150, 71), Image.LANCZOS)
SW, SH = wm_small.size
spx = wm_small.load()
row0 = int((90 - LAT_TOP) / 180.0 * SH)
row1 = int((90 - LAT_BOT) / 180.0 * SH)
cols, rows = SW, row1 - row0
cw, chh = MAP_W / cols, MAP_H / rows
for yy in range(row0, row1):
    for xx in range(SW):
        r, g, b = spx[xx, yy]
        if r > 200 and g > 200 and b > 200:
            cx = MAP_X + (xx + 0.5) * cw
            cy = MAP_Y + (yy - row0 + 0.5) * chh
            d.ellipse([cx - 1.1, cy - 1.1, cx + 1.1, cy + 1.1], fill=NAVY)


def map_xy(lon, lat):
    x = MAP_X + (lon + 180) / 360.0 * MAP_W
    y = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return x, y


MARKERS = [
    (30.7, 36.9, 0, 0),      # 1 Antalya
    (46.7, 24.7, 0, 0),      # 2 Riyadh
    (-76.0, -11.2, 0, 0),    # 3 Junin, Peru
    (33.4, 47.9, 0, 0),      # 4 Kryvyi Rih
    (None, None, 0, 0),      # 5 Mercury (in space) — top-right corner
    (174.8, -41.3, 0, 0),    # 6 Wellington
    (-77.0, 38.9, 0, 0),     # 7 Washington
    (4.35, 50.85, 0, 0),     # 8 Brussels
    (6.3, 4.9, 0, 0),        # 9 Bayelsa
    (42.9, 14.8, 0, 0),      # 10 Hodeidah
    (13.4, 52.5, 14, -12),   # 11 Europe (Berlin, offset from Brussels)
    (-118.2, 34.05, 0, 0),   # 12 Los Angeles
    (125.6, 7.1, 0, 0),      # 13 Davao
    (127.0, 37.5, 0, 0),     # 14 South Korea (Seoul)
    (-115.1, 36.2, 16, -12),  # 15 Las Vegas (offset from LA)
]
for i, (lon, lat, dx, dy) in enumerate(MARKERS, start=1):
    if lon is None:
        mx, my = MAP_X + MAP_W - 16, MAP_Y + 14
    else:
        mx, my = map_xy(lon, lat)
    circle_num(mx + dx, my + dy, 8, str(i), F_MAPN)
d.text((MAP_X, MAP_Y + MAP_H + 6),
       "Pins 1\u201315 mark the pictured stories. No. 5 is in space: Mercury.",
       font=F_MAPC, fill=MUTED)

# ALSO list 16-35 (20 stories, 2 columns of 10, one line each)
ALSO = [
    ("COPENHAGEN", "Denmark expels a Russian attach\u00e9.", "Reports"),
    ("WARSAW", "Rutte in Warsaw, Poland seeks NATO cover.", "AP"),
    ("ROME", "Italy rail strike as unions walk out.", "Reports"),
    ("GAZA", "Strikes kill six as aid talks stall.", "Reports"),
    ("TEHRAN", "Trump: Iran wants a deal; Israel urges strikes.", "AP"),
    ("JERUSALEM", "Car blast kills one in the city.", "Reports"),
    ("JOHANNESBURG", "ANC suffers its worst result yet.", "Reports"),
    ("NAGA", "City status vote divides the council.", "Reports"),
    ("PYONGYANG", "Kim tours factory sites.", "KCNA"),
    ("NEW DELHI", "Air quality stays poor, smog lingers.", "Reports"),
    ("CEBU", "Grid on yellow alert after a plant trip.", "Reports"),
    ("JAKARTA", "Quake offshore, no tsunami warning.", "Reports"),
    ("WASHINGTON", "Roundup deal backed by a US judge.", "Reports"),
    ("WASHINGTON", "Trump says he will rehire Huang.", "Reports"),
    ("WASHINGTON", "Trump floats a data centre tax.", "Reports"),
    ("NEW YORK", "Anthropic shares fall 9% on AI scare.", "Reports"),
    ("SANTIAGO", "Quake in the north, no damage.", "Reports"),
    ("CANBERRA", "AI camera row grows in parliament.", "Reports"),
    ("HOBART", "Party donors named in a new list.", "Reports"),
    ("MELBOURNE", "Australia v England open T20 at MCG.", "Reports"),
]
COLW = 320
COLX = [AX, AX + COLW + 12]
for i, (city, rest, src) in enumerate(ALSO):
    col, row = divmod(i, 10)
    x = COLX[col]
    y = bot_y + 22 + row * 13
    num = str(i + 16)
    cx = x
    for txt, fnt, fill in [(num + ". ", F_ALSO_N, RED),
                           (city + " \u2014 ", F_ALSO_B, INK),
                           (rest + " (" + src + ")", F_ALSO, INK)]:
        d.text((cx, y), txt, font=fnt, fill=fill)
        cx += d.textlength(txt, font=fnt)
    if cx > x + COLW:
        print("OVERFLOW also", num, city, "width", round(cx - x), ">", COLW)
also_end = bot_y + 22 + 10 * 13

# ---------------- DATE CHECK (red box) + FOOTER ----------------
dc_y = max(MAP_Y + MAP_H + 22, also_end + 8)
dc_text = ("Left out as Friday 20 November news, NOT shown as Saturday's: "
           "Russian missiles land in Poland \u00b7 Kyiv's bridges hit \u00b7 "
           "UK-EU summit deals \u00b7 Trump-Xi-Putin Shenzhen summit \u00b7 "
           "ICJ Myanmar genocide ruling \u00b7 Mongolia's president quits "
           "\u00b7 LA quake 4.2 \u00b7 US-China military-AI pact \u00b7 Pete "
           "Rose pardon \u00b7 Wall Street's AI sell-off.")
dc_lines = wrap(dc_text, F_FOOT, CW - 16)
dc_h = 8 + 14 + len(dc_lines) * 11 + 8
d.rectangle([MX, dc_y, W - MX, dc_y + dc_h], outline=RED, width=2)
d.text((MX + 8, dc_y + 8), "DATE CHECK", font=F_SECT, fill=RED)
textlines(MX + 8, dc_y + 24, dc_lines, F_FOOT, INK, 11)
foot_y = dc_y + dc_h + 10
d.line([MX, foot_y, W - MX, foot_y], fill=RULE, width=1)
d.text((MX, foot_y + 8),
       "Every story here happened, or was first reported, on Saturday "
       "21 November 2026 in at least one time zone. Claims are attributed; "
       "forecasts are flagged. Original drawings.",
       font=F_FOOT, fill=MUTED)
d.text((MX, foot_y + 20),
       "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 USGS \u00b7 ESA \u00b7 EU "
       "\u00b7 F1.",
       font=F_FOOT, fill=MUTED)
print("final content bottom y:", foot_y + 32, "of", H)

out = os.path.join(BASE, "entry.png")
img.save(out, "PNG")
print("saved", out, img.size, os.path.getsize(out), "bytes")
