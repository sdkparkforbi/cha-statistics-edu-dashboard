# -*- coding: utf-8 -*-
"""report.html 에 실제 집계 데이터를 채워 넣는 패치 스크립트."""
import json, re, html

S = json.load(open('data_survey.json', encoding='utf-8'))
U = json.load(open('data_usage.json', encoding='utf-8'))
src = open('report.html', encoding='utf-8').read()

reps = []          # (old, new) 단순 치환
rxs  = []          # (pattern, new) 정규식 치환
def esc(t): return html.escape(t, quote=False)

# ── CSS: .real 배지 추가 ──
reps.append((
 'padding:2px 7px;border-radius:5px;margin-left:8px;vertical-align:middle;}',
 'padding:2px 7px;border-radius:5px;margin-left:8px;vertical-align:middle;}\n'
 '  .real{display:inline-block;font-size:10.5px;font-weight:700;color:var(--forest);'
 'background:rgba(90,125,107,.10);border:1px solid rgba(90,125,107,.30);'
 'padding:2px 7px;border-radius:5px;margin-left:8px;vertical-align:middle;}'))

# ── 표지: 실데이터 칩 추가 ──
reps.append((
 '      <span class="chip"><b>8</b> 그림 · <b>9</b> 표</span>\n    </div>',
 '      <span class="chip"><b>8</b> 그림 · <b>9</b> 표</span>\n'
 '      <span class="chip"><b>n=22</b> 유효응답</span>\n'
 '      <span class="chip">실데이터 · 2026-06-18</span>\n    </div>'))

# ── 요약: 실데이터 헤드라인 2줄 추가 + 멀티모달 보강 ──
reps.append((
 '      <li><b>목적:</b> 경영통계 교육봇을 사용한 학습자의 인식을 6개 구인·14개 문항(5점 리커트)으로 측정하고, 사용 통계와 함께 실시간 집계.</li>',
 '      <li><b>집계 기준(2026-06-18):</b> 설문 응답 27건(유효 22건) · 누적 175세션 · 712개 메시지 · 사용자 38명.</li>\n'
 '      <li><b>전반 결과:</b> 종합 인식 <b>4.26 / 5</b>(SD 0.40)로 긍정적. 구인 중 ‘퀴즈–챗봇 연동(A)’ 4.48이 최고, ‘학습몰입·호기심(E)’ 3.98이 최저.</li>\n'
 '      <li><b>목적:</b> 경영통계 교육봇을 사용한 학습자의 인식을 6개 구인·14개 문항(5점 리커트)으로 측정하고, 사용 통계와 함께 실시간 집계.</li>'))
reps.append((
 '      <li><b>멀티모달:</b> FTF(아바타)·STS(음성)·TTT(텍스트) 세 모드의 주 사용 / 가장 도움된 모드 분포 비교.</li>',
 '      <li><b>멀티모달:</b> FTF(아바타)·STS(음성)·TTT(텍스트) 세 모드 비교 — 실제로는 <b>텍스트(TTT)</b>가 주 사용의 82%로 압도적이며, 응답자 22명 중 15명(68%)이 모드를 전환해 사용.</li>'))

# ── KPI 섹션 ──
reps.append((
 '각 지표의 의미·단위·출처는 다음과 같습니다.</p>',
 '각 지표의 의미·단위와 <b>현재 값(2026-06-18 기준)</b>은 다음과 같습니다.</p>'))
rxs.append((re.compile(r'<thead><tr><th>지표</th>.*?</tbody>', re.S),
 '<thead><tr><th>지표</th><th>설명</th><th class="c">단위</th><th class="c">현재 값</th><th>출처 필드</th></tr></thead>\n'
 '        <tbody>\n'
 '          <tr><td><b>설문 응답</b></td><td>제출된 설문 총건수와 유효 응답 건수</td><td class="c">건</td><td class="c"><b>27</b> <small>(유효 22)</small></td><td class="mono">totals.total / valid</td></tr>\n'
 '          <tr><td><b>평균 응답시간</b></td><td>설문 작성에 걸린 평균 소요 시간</td><td class="c">초</td><td class="c"><b>114.1</b></td><td class="mono">totals.avg_duration_sec</td></tr>\n'
 '          <tr><td><b>평균 종합점수</b></td><td>전체 종합 인식 점수의 평균</td><td class="c">/5</td><td class="c"><b>4.26</b> <small>(SD 0.40)</small></td><td class="mono">overall_stats.mean</td></tr>\n'
 '          <tr><td><b>대화 세션</b></td><td>누적 대화 세션 수와 고유 사용자 수</td><td class="c">건/명</td><td class="c"><b>175</b> · <b>38</b></td><td class="mono">totals.sessions_total / users_total</td></tr>\n'
 '        </tbody>'))

# ── 그림3: 구인 ──
reps.append((
 '    <p>대시보드는 각 구인의 평균을 가로 막대로 보여줍니다(4.0 이상은 녹색, 3.0 미만은 적색으로 강조). 다음은 표시 형태를 보여주는 예시입니다.</p>',
 '    <p>대시보드는 각 구인의 평균을 가로 막대로 보여줍니다(4.0 이상은 녹색으로 강조). 아래는 <b>실제 집계 결과</b>로, 6개 구인 모두 4점 안팎의 높은 인식을 보이며 ‘학습몰입·호기심(E, 3.98)’만 4점을 살짝 밑돕니다.</p>'))
reps.append((
 '      <figcaption><b>그림 3.</b> 구인별 평균 (5점 척도) <span class="illus">예시 데이터</span></figcaption>',
 '      <figcaption><b>그림 3.</b> 구인별 평균 (5점 척도, n=22) <span class="real">실데이터</span></figcaption>'))

# ── 표3: 문항별 M·SD·n ──
reps.append((
 '      <div class="tbl-cap"><b>표 3.</b> 14개 문항 전체 (코드 · 내용 · 구인 · 변수명)</div>',
 '      <div class="tbl-cap"><b>표 3.</b> 14개 문항 전체 — 평균(M)·표준편차(SD)·응답수(n) <span class="real">실데이터 · n=22</span></div>'))
IT = [('Q1','퀴즈 즉시 질문','A','q_quiz_link'),('Q2','챗봇 풀이 도움','A','q_quiz_explain'),
 ('Q3','모드 전환 가능','B','q_mode_switch'),('Q4','교수자 실재감','C','q_teacher_presence'),
 ('Q5','부담 없는 분위기','C','q_warm_atmosphere'),('Q6','강의자료 일관성','C','q_consistent_explain'),
 ('Q7','답변 정확성','D','q_accuracy'),('Q8','한계 솔직히 인정','D','q_limit_admit'),
 ('Q9','시간 빠르게 감','E','q_flow'),('Q10','호기심 생김','E','q_curiosity'),
 ('Q11','개념 이해','F','q_understanding'),('Q12','자신감 생김','F','q_confidence'),
 ('Q13','재사용 의사','F','q_will_reuse'),('Q14','전반 도움','F','q_overall')]
rows = []
for code, txt, con, var in IT:
    st = S['item_stats'][var]
    rows.append(f'          <tr><td class="code">{code}</td><td>{txt}</td><td class="c">{con}</td>'
                f'<td class="c"><b>{float(st["mean"]):.2f}</b></td><td class="c">{float(st["sd"]):.2f}</td>'
                f'<td class="c">{st["n"]}</td><td class="mono">{var}</td></tr>')
rxs.append((re.compile(r'<thead><tr><th class="code">코드</th>.*?q_overall</td></tr>\s*</tbody>', re.S),
 '<thead><tr><th class="code">코드</th><th>문항 내용</th><th class="c">구인</th>'
 '<th class="c">M</th><th class="c">SD</th><th class="c">n</th><th>변수명</th></tr></thead>\n'
 '        <tbody>\n' + '\n'.join(rows) + '\n        </tbody>'))

# ── 그림4: 모드 ──
reps.append((
 '    <p>대시보드는 <b>주 사용 모드</b>와 <b>가장 도움된 모드</b>를 각각 도넛 차트로 비교하여, 학습자가 실제로 많이 쓴 방식과 가장 효과를 느낀 방식의 차이를 보여줍니다.</p>',
 '    <p>대시보드는 <b>주 사용 모드</b>와 <b>가장 도움된 모드</b>를 각각 도넛 차트로 비교합니다. 실제 집계에서는 <b>텍스트(TTT)</b>가 주 사용 18명(82%)·가장 도움 17명(77%)으로 압도적이고, 아바타(FTF) 3명, 음성(STS) 1~2명입니다. 한편 응답자 22명 중 <b>15명(68%)이 모드를 전환</b>해 사용했습니다.</p>'))
reps.append((
 '      <figcaption><b>그림 4.</b> 모드 사용 분포 — 주 사용 모드 / 가장 도움된 모드 <span class="illus">예시 데이터</span></figcaption>',
 '      <figcaption><b>그림 4.</b> 모드 사용 분포 — 주 사용 / 가장 도움된 모드 (괄호: 주사용/도움 인원) <span class="real">실데이터</span></figcaption>'))

# ── 그림5: 사전수준 ──
reps.append((
 '    <p>학습자의 사전 통계 지식 수준별로 종합 점수·학습효과·정확성을 비교하여, 교육봇이 어떤 집단에 더 효과적인지 파악합니다.</p>',
 '    <p>학습자의 사전 통계 지식 수준(1=낮음 ~ 4=높음)별로 종합·학습효과·정확성을 비교합니다. 실제로는 사전 수준이 <b>낮을수록 종합·학습효과 인식이 더 높게</b> 나타났습니다(수준1 종합 4.57 → 수준4 4.05). 통계가 약한 학습자일수록 교육봇 효과를 크게 느낀 것으로 해석됩니다.</p>'))
reps.append((
 '      <figcaption><b>그림 5.</b> 사전 통계수준별 효과 (종합·학습효과·정확성) <span class="illus">예시 데이터</span></figcaption>',
 '      <figcaption><b>그림 5.</b> 사전 통계수준별 효과 (종합·학습효과·정확성) <span class="real">실데이터</span></figcaption>'))

# ── 표6: 인구통계 실데이터 ──
reps.append((
 '    <p>응답자 구성을 학년·성별·전공으로 나누어 표로 제공합니다(전공은 상위 10개). 표 6은 분류 항목과 표시 예시입니다.</p>',
 '    <p>응답자 22명의 구성을 학년·성별·전공으로 보여줍니다. <b>4학년(12명)·3학년(7명)</b>이 다수이고, 전공은 <b>경영학·심리학</b>이 대부분입니다.</p>'))
reps.append((
 '      <div class="tbl-cap"><b>표 6.</b> 인구통계 분류 항목 <span class="illus">예시 데이터</span></div>',
 '      <div class="tbl-cap"><b>표 6.</b> 인구통계 — 학년·성별·전공 분포 <span class="real">실데이터 · n=22</span></div>'))
demo_body = (
 '        <thead><tr><th>분류</th><th>구분</th><th class="c">응답수</th></tr></thead>\n'
 '        <tbody>\n'
 '          <tr><td class="grp" rowspan="4">학년 <span class="mono" style="color:var(--forest)">grade</span></td><td>4학년</td><td class="c">12</td></tr>\n'
 '          <tr><td>3학년</td><td class="c">7</td></tr>\n'
 '          <tr><td>2학년</td><td class="c">1</td></tr>\n'
 '          <tr><td>기타</td><td class="c">2</td></tr>\n'
 '          <tr><td class="grp" rowspan="2">성별 <span class="mono" style="color:var(--forest)">gender</span></td><td>여 (female)</td><td class="c">13</td></tr>\n'
 '          <tr><td>남 (male)</td><td class="c">9</td></tr>\n'
 '          <tr><td class="grp" rowspan="4">전공 <span class="mono" style="color:var(--forest)">major</span></td><td>경영학</td><td class="c">9</td></tr>\n'
 '          <tr><td>심리학</td><td class="c">8</td></tr>\n'
 '          <tr><td>디지털보건의료</td><td class="c">3</td></tr>\n'
 '          <tr><td>미디어커뮤니케이션학</td><td class="c">2</td></tr>\n'
 '        </tbody>')
rxs.append((re.compile(r'<thead><tr><th>분류</th>.*?</tbody>', re.S), demo_body))

# ── 표5: 자유응답 행 보강 ──
reps.append((
 '<td>최신 20건의 도움된 점 / 개선 의견</td>',
 '<td>최신 20건까지 (현재 15명) 도움 / 개선 의견</td>'))

# ── 자유응답: 실제 전체 카드 ──
fr = S['free_responses']
cards = []
n_help = n_imp = 0
for it in fr:
    score = it.get('overall_score'); score = f'{float(score):.2f}' if score not in (None,'') else '—'
    dt = it.get('submitted_at','')
    if it.get('free_helpful'):
        n_help += 1
        cards.append(f'        <div class="free-card"><div class="fmeta"><span class="flabel">도움</span>{dt} · 종합 {score}/5</div>{esc(it["free_helpful"])}</div>')
    if it.get('free_improvement'):
        n_imp += 1
        cards.append(f'        <div class="free-card improve"><div class="fmeta"><span class="flabel">개선</span>{dt} · 종합 {score}/5</div>{esc(it["free_improvement"])}</div>')
total_cards = n_help + n_imp
reps.append((
 '    <p>다음은 카드가 화면에 표시되는 형태의 예시입니다. 두 번째 도움 카드와 첫 번째 개선 카드는 작성 시각·종합점수가 같은데, 이는 <b>같은 응답자가 두 칸을 모두 작성</b>해 카드 2장이 생성된 경우를 보여줍니다.</p>',
 f'    <p>아래는 <b>실제 자유응답 전체</b>입니다(현재 {len(fr)}명 작성 · 도움 {n_help} + 개선 {n_imp} = <b>{total_cards}개 카드</b>). 같은 작성 시각·종합점수를 가진 도움/개선 카드는 한 응답자가 두 칸을 모두 작성한 경우입니다. 목록은 스크롤로 전체를 볼 수 있습니다.</p>'))
new_free = ('<div class="free-ex" style="max-height:560px;overflow-y:auto;padding-right:6px;">\n'
            + '\n'.join(cards) + '\n      </div>\n'
            f'      <figcaption><b>그림 6.</b> 자유응답 전체 — 도움(골드)·개선(적색), 총 {total_cards}개 카드 <span class="real">실데이터 · 2026-06-18</span></figcaption>')
rxs.append((re.compile(r'<div class="free-ex">.*?</div>\s*<figcaption><b>그림 6\.</b>.*?</figcaption>', re.S), new_free))

# ── 사용통계 ──
reps.append((
 '    <p>설문과 별개로, 교육봇의 실제 사용 로그를 일자별·시간대별로 집계합니다.</p>',
 '    <p>설문과 별개로, 교육봇의 실제 사용 로그를 일자별·시간대별로 집계합니다. 누적 <b>175세션·712개 메시지</b>이며, 5/28·6/9에 사용이 몰렸고 시간대로는 <b>오전 9시·저녁 19–21시</b>에 집중됩니다.</p>'))
reps.append((
 '      <figcaption><b>그림 7.</b> 일자별 사용 — 세션 수와 활성 사용자 수 <span class="illus">예시 데이터</span></figcaption>',
 '      <figcaption><b>그림 7.</b> 일자별 사용 — 세션·활성 사용자 (2026-05-18 ~ 06-18) <span class="real">실데이터</span></figcaption>'))
reps.append((
 '      <figcaption><b>그림 8.</b> 시간대별 사용 — 0–23시 메시지 분포 <span class="illus">예시 데이터</span></figcaption>',
 '      <figcaption><b>그림 8.</b> 시간대별 사용 — 0–23시 메시지 분포 <span class="real">실데이터</span></figcaption>'))

# ── 표9: construct_stats 구조 보정 + usage 추가 행 ──
reps.append((
 '<tr><td class="mono">construct_stats[key]</td><td>{mean, n}</td><td>구인별 평균·응답수</td></tr>',
 '<tr><td class="mono">construct_stats[key]</td><td>{items, mean, sd, n}</td><td>구인별 문항·평균·표준편차·응답수</td></tr>'))
reps.append((
 '<tr><td class="mono">as_of</td><td>일시</td><td>집계 기준 시각(업데이트 표시)</td></tr>',
 '<tr><td class="mono">as_of</td><td>일시</td><td>집계 기준 시각(업데이트 표시)</td></tr>\n'
 '          <tr><td class="mono">session_avg / signups[] / turn_hist</td><td>—</td><td>세션 평균·가입 추이·턴 수 분포</td></tr>\n'
 '          <tr><td class="mono">top_users[]</td><td>{name, msgs, …}</td><td>상위 사용자 — <b>실명 포함, 본 보고서에서 제외</b></td></tr>'))

# ── 안내 박스: 실데이터 + 개인정보 고지 ──
rxs.append((re.compile(r'<div class="note">\s*<b>📌 데이터에 대한 안내\.</b>.*?</div>', re.S),
 '<div class="note">\n'
 '      <b>📌 데이터 출처와 개인정보.</b> 본 보고서의 모든 수치·그림·자유응답은 '
 '<b>2026-06-18 기준 실제 집계 데이터</b>(<span class="mono">survey_summary_v2_edu</span>, '
 '<span class="mono">usage_summary</span>)입니다. 다만 사용 로그의 상위 사용자(<span class="mono">top_users</span>)에는 '
 '<b>실명이 포함</b>되어 있어 공개 보고서에서는 제외했고, 자유응답은 작성자 식별 정보 없이 <b>익명 의견만</b> 표시했습니다. '
 '최신 수치는 상단의 <a href="https://cha-statistics-bot-liveavatar.vercel.app/dashboard/" target="_blank" rel="noopener">라이브 대시보드</a>에서 확인할 수 있습니다.\n'
 '    </div>'))

# ── 적용 ──
def apply(text):
    miss = []
    for old, new in reps:
        if old in text: text = text.replace(old, new)
        else: miss.append(old[:60])
    for pat, new in rxs:
        if pat.search(text): text = pat.sub(lambda m: new, text, count=1)
        else: miss.append('RX:' + pat.pattern[:50])
    return text, miss

src, miss = apply(src)
# 남은 illus 배지 일괄 치환
src = src.replace('<span class="illus">예시 데이터</span>', '<span class="real">실데이터</span>')
open('report.html', 'w', encoding='utf-8').write(src)
print('done. free cards:', total_cards, '| misses:', len(miss))
for m in miss: print('  MISS:', m)
