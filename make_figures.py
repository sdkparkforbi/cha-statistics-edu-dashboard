# -*- coding: utf-8 -*-
"""보고서용 SVG 차트 그림 생성 — 실제 집계 데이터(data_survey.json, data_usage.json) 기반."""
import json, math

GOLD='#b88a5e'; GOLDBR='#d4a574'; FOREST='#5a7d6b'; SLATE='#4a6b85'
RUST='#c4554d'; PLUM='#8c6b9d'; INK='#2a2620'; MUTED='#8a8275'
LINE='#e8e1d3'; PANEL2='#f5f1e8'; PANEL='#ffffff'
FAM = "'Malgun Gothic','Pretendard','Noto Sans KR',sans-serif"

S = json.load(open('data_survey.json', encoding='utf-8'))
U = json.load(open('data_usage.json', encoding='utf-8'))

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
    order = [('A_quiz','A. 퀴즈–챗봇 연동'), ('B_multimodal','B. 멀티모달 인터랙션'),
             ('C_presence','C. 교수자 실재감'), ('D_accuracy','D. 정확성·안전감'),
             ('E_flow','E. 학습몰입·호기심'), ('F_learning','F. 인지된 학습효과')]
    cs = S['construct_stats']
    s = [head(w, h)]
    s.append(T(20, 30, '구인별 평균 (5점 척도, n=22)', 14, INK, weight='700'))
    x0, x1 = 230, 620
    full = x1 - x0
    for v in range(1, 6):
        gx = x0 + full * v / 5
        s.append(f'<line x1="{gx:.1f}" y1="52" x2="{gx:.1f}" y2="270" stroke="{LINE}" stroke-width="1"/>')
        s.append(T(gx, 288, str(v), 10, MUTED, 'middle'))
    y = 70
    for key, label in order:
        val = float(cs[key]['mean'])
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
MODE_COL = {'ftf': GOLD, 'sts': FOREST, 'ttt': SLATE}
MODE_NM  = {'ftf': 'FTF 아바타', 'sts': 'STS 음성', 'ttt': 'TTT 텍스트'}
ORDER = ['ftf', 'sts', 'ttt']

def donut(cx, cy, r, segs, title, total):
    C = 2 * math.pi * r
    out = [T(cx, cy - r - 38, title, 13, INK, 'middle', '700'),
           T(cx, cy - r - 22, f'n={total}', 11, MUTED, 'middle')]
    cum = 0.0
    for pct, col in segs:
        L = C * pct / 100
        if L <= 0: continue
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" '
            f'stroke-width="30" stroke-dasharray="{L:.2f} {C-L:.2f}" '
            f'stroke-dashoffset="{-cum:.2f}" transform="rotate(-90 {cx} {cy})"/>')
        cum += L
    return ''.join(out)

def mode_segs(rows):
    d = {r['mode']: int(r['cnt']) for r in rows}
    total = sum(d.values()) or 1
    return [(d.get(m, 0) / total * 100, MODE_COL[m]) for m in ORDER], total, d

def fig_modes():
    w, h = 700, 340
    s = [head(w, h)]
    s.append(T(20, 30, '모드 사용 분포', 14, INK, weight='700'))
    pseg, ptot, pd = mode_segs(S['modes']['primary'])
    hseg, htot, hd = mode_segs(S['modes']['helpful'])
    s.append(donut(185, 175, 72, pseg, '주 사용 모드', ptot))
    s.append(donut(515, 175, 72, hseg, '가장 도움된 모드', htot))
    lx, ly = 220, 300
    for m in ORDER:
        s.append(f'<rect x="{lx}" y="{ly-10}" width="13" height="13" rx="3" fill="{MODE_COL[m]}"/>')
        s.append(T(lx + 19, ly + 1, f'{MODE_NM[m]} ({pd.get(m,0)}/{hd.get(m,0)})', 11.5, MUTED))
        lx += 130
    s.append('</svg>')
    return ''.join(s)

# ── 그림 5: 사전 통계수준별 효과 (그룹 막대) ─────────────
def fig_prior():
    rows = sorted(S['by_prior_level'], key=lambda r: int(r['level']))
    w, h = 700, 320
    s = [head(w, h)]
    s.append(T(20, 30, '사전 통계수준별 효과 (5점 척도)', 14, INK, weight='700'))
    base, top = 255, 55
    def yv(v): return base - (base - top) * v / 5
    for v in range(0, 6):
        gy = yv(v)
        s.append(f'<line x1="60" y1="{gy:.1f}" x2="660" y2="{gy:.1f}" stroke="{LINE}" stroke-width="1"/>')
        s.append(T(50, gy + 4, str(v), 10, MUTED, 'end'))
    cols = [GOLD, FOREST, SLATE]
    keys = ['overall', 'learning', 'accuracy']
    n = len(rows)
    span = (660 - 60)
    bw = 30
    for i, r in enumerate(rows):
        cx = 60 + span * (i + 0.5) / n
        start = cx - (bw * 3 + 10) / 2
        for j, k in enumerate(keys):
            v = float(r[k]); bx = start + j * (bw + 5); by = yv(v)
            s.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{base-by:.1f}" rx="4" fill="{cols[j]}"/>')
            s.append(T(bx + bw/2, by - 5, f'{v:.1f}', 10, INK, 'middle', '700'))
        s.append(T(cx, base + 20, f'수준 {r["level"]} (n={r["n"]})', 11.5, INK, 'middle', '600'))
    lx = 210
    for name, col in [('종합', GOLD), ('학습효과', FOREST), ('정확성', SLATE)]:
        s.append(f'<rect x="{lx}" y="292" width="13" height="13" rx="3" fill="{col}"/>')
        s.append(T(lx + 19, 303, name, 12, MUTED))
        lx += 120
    s.append('</svg>')
    return ''.join(s)

# ── 그림 6(보고서상 그림 7): 일자별 사용 ─────────────────
def md(dstr):
    p = dstr.split('-'); return f'{int(p[1])}/{int(p[2])}'

def fig_daily():
    act = U['activity']
    w, h = 720, 300
    s = [head(w, h)]
    s.append(T(20, 30, '일자별 사용 (세션 · 활성 사용자)', 14, INK, weight='700'))
    base, top = 235, 55
    mx = max([int(a['sessions']) for a in act] + [1])
    mx = math.ceil(mx / 5) * 5
    def yv(v): return base - (base - top) * v / mx
    s.append(f'<line x1="40" y1="{base}" x2="700" y2="{base}" stroke="{LINE}"/>')
    for gl in range(0, mx + 1, max(5, mx // 4)):
        gy = yv(gl); s.append(T(34, gy + 4, str(gl), 9.5, MUTED, 'end'))
        s.append(f'<line x1="40" y1="{gy:.1f}" x2="700" y2="{gy:.1f}" stroke="{LINE}" stroke-width="0.7"/>')
    n = len(act)
    slot = (700 - 46) / n
    for i, a in enumerate(act):
        cx = 46 + slot * (i + 0.5)
        ss = int(a['sessions']); au = int(a['active_users'])
        bw = min(11, slot/2 - 1)
        s.append(f'<rect x="{cx-bw-1:.1f}" y="{yv(ss):.1f}" width="{bw:.1f}" height="{base-yv(ss):.1f}" rx="2" fill="{GOLD}"/>')
        s.append(f'<rect x="{cx+1:.1f}" y="{yv(au):.1f}" width="{bw:.1f}" height="{base-yv(au):.1f}" rx="2" fill="{FOREST}"/>')
        if i % 2 == 0:
            s.append(T(cx, base + 15, md(a['d']), 8.5, MUTED, 'middle'))
    lx = 300
    for name, col in [('세션', GOLD), ('활성 사용자', FOREST)]:
        s.append(f'<rect x="{lx}" y="270" width="13" height="13" rx="3" fill="{col}"/>')
        s.append(T(lx + 19, 281, name, 12, MUTED))
        lx += 120
    s.append('</svg>')
    return ''.join(s)

# ── 그림 7(보고서상 그림 8): 시간대별 사용 ───────────────
def fig_hourly():
    hd = {int(x['h']): int(x['n']) for x in U['hourly']}
    vals = [hd.get(i, 0) for i in range(24)]
    w, h = 720, 240
    s = [head(w, h)]
    s.append(T(20, 30, '시간대별 사용 (메시지 수)', 14, INK, weight='700'))
    base, top = 190, 50
    mx = math.ceil((max(vals) or 1) / 10) * 10
    def yv(v): return base - (base - top) * v / mx
    s.append(f'<line x1="40" y1="{base}" x2="690" y2="{base}" stroke="{LINE}"/>')
    for gl in range(0, mx + 1, max(10, mx // 5)):
        gy = yv(gl); s.append(T(34, gy + 4, str(gl), 9, MUTED, 'end'))
    slot = (690 - 44) / 24
    for hh in range(24):
        cx = 44 + slot * (hh + 0.5); bw = slot * 0.66; v = vals[hh]
        s.append(f'<rect x="{cx-bw/2:.1f}" y="{yv(v):.1f}" width="{bw:.1f}" height="{base-yv(v):.1f}" rx="2" fill="{SLATE}"/>')
        if hh % 3 == 0:
            s.append(T(cx, base + 16, f'{hh}', 9.5, MUTED, 'middle'))
    s.append(T(365, 222, '시 (0–23시)', 10, MUTED, 'middle'))
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
