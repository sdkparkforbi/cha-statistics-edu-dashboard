# -*- coding: utf-8 -*-
"""보고서용 SVG 차트 그림 생성 (예시/개념 데이터). 브라우저 폰트로 렌더링."""
import math

GOLD='#b88a5e'; GOLDBR='#d4a574'; FOREST='#5a7d6b'; SLATE='#4a6b85'
RUST='#c4554d'; PLUM='#8c6b9d'; INK='#2a2620'; MUTED='#8a8275'
LINE='#e8e1d3'; PANEL2='#f5f1e8'; PANEL='#ffffff'
FAM = "'Malgun Gothic','Pretendard','Noto Sans KR',sans-serif"

def T(x, y, s, size=13, fill=INK, anchor='start', weight='400'):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAM}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')

def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="100%" role="img">'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{PANEL}"/>')

# ── 그림 3: 구인별 평균 (가로 막대) ─────────────────────
def fig_constructs():
    w, h = 700, 300
    s = [head(w, h)]
    s.append(T(20, 30, '구인별 평균 (5점 척도) · 예시', 14, INK, weight='700'))
    items = [('A. 퀴즈–챗봇 연동', 4.08), ('B. 멀티모달 인터랙션', 3.92),
             ('C. 교수자 실재감', 4.31), ('D. 정확성·안전감', 4.05),
             ('E. 학습몰입·호기심', 3.84), ('F. 인지된 학습효과', 4.19)]
    x0, x1 = 230, 620        # bar track
    full = x1 - x0           # = 5.0
    # gridlines 1..5
    for v in range(1, 6):
        gx = x0 + full * v / 5
        s.append(f'<line x1="{gx:.1f}" y1="52" x2="{gx:.1f}" y2="270" stroke="{LINE}" stroke-width="1"/>')
        s.append(T(gx, 288, str(v), 10, MUTED, 'middle'))
    y = 70
    for label, val in items:
        bw = full * val / 5
        col = FOREST if val >= 4 else GOLD
        s.append(T(20, y + 12, label, 12.5, INK, weight='600'))
        s.append(f'<rect x="{x0}" y="{y}" width="{full}" height="16" rx="8" fill="{PANEL2}"/>')
        s.append(f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="16" rx="8" fill="{col}"/>')
        s.append(T(x0 + bw + 8, y + 13, f'{val:.2f}', 12, INK, weight='700'))
        y += 35
    s.append('</svg>')
    return ''.join(s)

# ── 그림 4: 모드 사용 분포 (도넛 x2) ────────────────────
def donut(cx, cy, r, segs, title):
    C = 2 * math.pi * r
    out = [T(cx, cy - r - 18, title, 13, INK, 'middle', '700')]
    cum = 0.0
    for name, pct, col in segs:
        L = C * pct / 100
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" '
            f'stroke-width="30" stroke-dasharray="{L:.2f} {C-L:.2f}" '
            f'stroke-dashoffset="{-cum:.2f}" transform="rotate(-90 {cx} {cy})"/>')
        cum += L
    return ''.join(out)

def fig_modes():
    w, h = 700, 330
    s = [head(w, h)]
    s.append(T(20, 30, '모드 사용 분포 (%) · 예시', 14, INK, weight='700'))
    primary = [('FTF 아바타', 45, GOLD), ('STS 음성', 32, FOREST), ('TTT 텍스트', 23, SLATE)]
    helpful = [('FTF 아바타', 52, GOLD), ('STS 음성', 28, FOREST), ('TTT 텍스트', 20, SLATE)]
    s.append(donut(185, 165, 72, primary, '주 사용 모드'))
    s.append(donut(515, 165, 72, helpful, '가장 도움된 모드'))
    # legend
    lx, ly = 250, 290
    for name, col in [('FTF 아바타', GOLD), ('STS 음성', FOREST), ('TTT 텍스트', SLATE)]:
        s.append(f'<rect x="{lx}" y="{ly-10}" width="13" height="13" rx="3" fill="{col}"/>')
        s.append(T(lx + 19, ly + 1, name, 12, MUTED))
        lx += 110
    s.append('</svg>')
    return ''.join(s)

# ── 그림 5: 사전 통계수준별 효과 (그룹 막대) ─────────────
def fig_prior():
    w, h = 700, 320
    s = [head(w, h)]
    s.append(T(20, 30, '사전 통계수준별 효과 (5점 척도) · 예시', 14, INK, weight='700'))
    base, top = 255, 55
    def yv(v): return base - (base - top) * v / 5
    for v in range(0, 6):
        gy = yv(v)
        s.append(f'<line x1="60" y1="{gy:.1f}" x2="650" y2="{gy:.1f}" stroke="{LINE}" stroke-width="1"/>')
        s.append(T(50, gy + 4, str(v), 10, MUTED, 'end'))
    groups = [('사전수준 하', [3.6, 3.5, 3.9]), ('사전수준 중', [4.0, 3.9, 4.1]),
              ('사전수준 상', [4.3, 4.2, 4.2])]
    cols = [GOLD, FOREST, SLATE]
    centers = [185, 355, 525]
    bw = 40
    for (gname, vals), cx in zip(groups, centers):
        start = cx - (bw * 3 + 12) / 2
        for i, v in enumerate(vals):
            bx = start + i * (bw + 6)
            by = yv(v)
            s.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{base-by:.1f}" rx="4" fill="{cols[i]}"/>')
            s.append(T(bx + bw/2, by - 5, f'{v:.1f}', 10.5, INK, 'middle', '700'))
        s.append(T(cx, base + 20, gname, 12, INK, 'middle', '600'))
    # legend
    lx = 230
    for name, col in [('종합', GOLD), ('학습효과', FOREST), ('정확성', SLATE)]:
        s.append(f'<rect x="{lx}" y="290" width="13" height="13" rx="3" fill="{col}"/>')
        s.append(T(lx + 19, 301, name, 12, MUTED))
        lx += 110
    s.append('</svg>')
    return ''.join(s)

# ── 그림 6: 일자별 사용 (그룹 막대) ─────────────────────
def fig_daily():
    w, h = 700, 300
    s = [head(w, h)]
    s.append(T(20, 30, '일자별 사용 · 예시', 14, INK, weight='700'))
    days = ['6/02', '6/03', '6/04', '6/05', '6/06', '6/07', '6/08', '6/09', '6/10', '6/11']
    sessions = [12, 18, 15, 22, 9, 25, 30, 21, 17, 14]
    active = [8, 11, 10, 15, 6, 17, 20, 14, 12, 9]
    base, top = 235, 55
    mx = 32
    def yv(v): return base - (base - top) * v / mx
    s.append(f'<line x1="44" y1="{base}" x2="660" y2="{base}" stroke="{LINE}"/>')
    n = len(days)
    slot = (660 - 50) / n
    for i, d in enumerate(days):
        cx = 50 + slot * (i + 0.5)
        bw = 16
        sx = cx - bw - 2
        ax = cx + 2
        s.append(f'<rect x="{sx:.1f}" y="{yv(sessions[i]):.1f}" width="{bw}" height="{base-yv(sessions[i]):.1f}" rx="3" fill="{GOLD}"/>')
        s.append(f'<rect x="{ax:.1f}" y="{yv(active[i]):.1f}" width="{bw}" height="{base-yv(active[i]):.1f}" rx="3" fill="{FOREST}"/>')
        s.append(T(cx, base + 16, d, 10, MUTED, 'middle'))
    # legend
    lx = 280
    for name, col in [('세션', GOLD), ('활성 사용자', FOREST)]:
        s.append(f'<rect x="{lx}" y="268" width="13" height="13" rx="3" fill="{col}"/>')
        s.append(T(lx + 19, 279, name, 12, MUTED))
        lx += 120
    s.append('</svg>')
    return ''.join(s)

# ── 그림 7: 시간대별 사용 (막대 24) ─────────────────────
def fig_hourly():
    w, h = 700, 240
    s = [head(w, h)]
    s.append(T(20, 30, '시간대별 사용 (메시지 수) · 예시', 14, INK, weight='700'))
    vals = [0, 0, 0, 1, 0, 2, 3, 5, 8, 12, 15, 18, 14, 16, 22, 20, 17, 13, 15, 19, 24, 21, 11, 4]
    base, top = 190, 50
    mx = 26
    def yv(v): return base - (base - top) * v / mx
    s.append(f'<line x1="40" y1="{base}" x2="668" y2="{base}" stroke="{LINE}"/>')
    n = 24
    slot = (668 - 44) / n
    for hh in range(n):
        cx = 44 + slot * (hh + 0.5)
        bw = slot * 0.66
        v = vals[hh]
        s.append(f'<rect x="{cx-bw/2:.1f}" y="{yv(v):.1f}" width="{bw:.1f}" height="{base-yv(v):.1f}" rx="2" fill="{SLATE}"/>')
        if hh % 3 == 0:
            s.append(T(cx, base + 16, f'{hh}', 9.5, MUTED, 'middle'))
    s.append(T(354, 222, '시 (0–23시)', 10, MUTED, 'middle'))
    s.append('</svg>')
    return ''.join(s)

figs = {
    'fig-constructs.svg': fig_constructs(),
    'fig-modes.svg': fig_modes(),
    'fig-prior.svg': fig_prior(),
    'fig-daily.svg': fig_daily(),
    'fig-hourly.svg': fig_hourly(),
}
for name, content in figs.items():
    with open(name, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('saved', name, len(content), 'bytes')
