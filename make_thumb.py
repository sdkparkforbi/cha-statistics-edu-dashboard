# -*- coding: utf-8 -*-
"""경영통계 교육봇 대시보드 썸네일(OG image) 생성 — Pillow"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG       = (250, 248, 243)
PANEL    = (255, 255, 255)
LINE     = (232, 225, 211)
INK      = (42, 38, 32)
MUTED    = (138, 130, 117)
GOLD     = (184, 138, 94)
GOLD_BR  = (212, 165, 116)
FOREST   = (90, 125, 107)
SLATE    = (74, 107, 133)

FONT = "C:/Windows/Fonts/malgun.ttf"
FONTB = "C:/Windows/Fonts/malgunbd.ttf"
def f(size, bold=True):
    return ImageFont.truetype(FONTB if bold else FONT, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# soft radial-ish corner glow (approx with translucent ellipses)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W-420, -260, W+200, 360], fill=(184, 138, 94, 28))
gd.ellipse([-260, H-300, 320, H+220], fill=(90, 125, 107, 20))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

PAD = 80

# top-left gold accent bar
d.rounded_rectangle([PAD, 70, PAD+6, 118], radius=3, fill=GOLD)

# brand icon tile
ix, iy, isz = PAD+24, 64, 60
d.rounded_rectangle([ix, iy, ix+isz, iy+isz], radius=14, fill=GOLD)
ic = f(34)
tb = d.textbbox((0,0), "통", font=ic)
d.text((ix + isz/2 - (tb[2]-tb[0])/2, iy + isz/2 - (tb[3]-tb[1])/2 - tb[1]), "통", font=ic, fill="#ffffff")

# brand text
d.text((ix+isz+22, 70), "경영통계 교육봇", font=f(26), fill=INK)
d.text((ix+isz+22, 106), "Learner Perception Dashboard · v2_edu", font=f(16, False), fill=MUTED)

# eyebrow pill
ey = "LEARNER PERCEPTION · 5-POINT LIKERT"
eyf = f(17)
eb = d.textbbox((0,0), ey, font=eyf)
ew = eb[2]-eb[0]
d.rounded_rectangle([PAD, 210, PAD+ew+44, 252], radius=21, fill=(238, 222, 197))
d.text((PAD+22, 217), ey, font=eyf, fill=GOLD)

# title
d.text((PAD, 280), "학습자 인식 대시보드", font=f(70), fill=INK)
d.text((PAD, 366), "6개 구인 · 14개 문항 · 멀티모달 인터랙션", font=f(34), fill=(90, 84, 74))

# stat chips row
chips = [("6", "구인"), ("14", "문항"), ("5점", "리커트"), ("3", "모드")]
cx = PAD
cy = 452
for num, lab in chips:
    nf, lf = f(40), f(20, False)
    nb = d.textbbox((0,0), num, font=nf)
    lb = d.textbbox((0,0), lab, font=lf)
    cw = max(nb[2]-nb[0], lb[2]-lb[0]) + 56
    ch = 110
    d.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=18, fill=PANEL, outline=LINE, width=2)
    d.text((cx + cw/2 - (nb[2]-nb[0])/2, cy+18), num, font=nf, fill=GOLD)
    d.text((cx + cw/2 - (lb[2]-lb[0])/2, cy+70), lab, font=lf, fill=MUTED)
    cx += cw + 18

# right-side mini construct bars (decorative)
bx = W - 300
by = 250
bar_colors = [GOLD, GOLD_BR, FOREST, SLATE, GOLD_BR, FOREST]
widths = [210, 196, 220, 200, 188, 214]
for i, (col, bw) in enumerate(zip(bar_colors, widths)):
    yy = by + i*46
    d.rounded_rectangle([bx, yy, bx+220, yy+14], radius=7, fill=(240, 234, 222))
    d.rounded_rectangle([bx, yy, bx+bw, yy+14], radius=7, fill=col)

# bottom URL
d.line([PAD, 560, W-PAD, 560], fill=LINE, width=2)
d.text((PAD, 578), "cha-statistics-bot-liveavatar.vercel.app", font=f(18, False), fill=MUTED)

img.save("thumbnail.png", "PNG")
print("saved thumbnail.png", img.size)
