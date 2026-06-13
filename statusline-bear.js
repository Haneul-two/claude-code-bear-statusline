// 곰 상태표시줄(3줄): 다마고치처럼 1분마다 기분이 랜덤으로 바뀌는 곰 + 오른쪽에 세션 정보
// settings.json의 statusLine 명령으로 실행되며, stdin으로 세션 JSON을 받는다.
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  let data;
  try {
    // 셸/파이프가 붙일 수 있는 BOM 제거 후 파싱
    data = JSON.parse(input.replace(/^﻿/, '').trim());
  } catch {
    console.log('🐻 statusline: JSON parse error');
    return;
  }

  const GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RED = '\x1b[31m',
    CYAN = '\x1b[36m', MAGENTA = '\x1b[35m', DIM = '\x1b[2m', RESET = '\x1b[0m';

  const pctColor = (p) => (p >= 90 ? RED : p >= 70 ? YELLOW : GREEN);
  const DAYS = ['일', '월', '화', '수', '목', '금', '토'];
  const pad2 = (n) => String(n).padStart(2, '0');

  // ── 곰의 기분: 한도와 무관하게 랜덤. 매 실행마다 바뀌면 깜빡거리므로
  //    시간 버킷(MOOD_INTERVAL_MS) + 세션 ID를 시드로 써서 버킷 안에서는 같은 기분 유지.
  const MOOD_INTERVAL_MS = 60 * 1000; // 1분마다 기분 전환
  const MOODS = [
    { eyes: '◕ᴥ◕', color: GREEN },   // 신남
    { eyes: '≧ᴥ≦', color: GREEN },   // 행복
    { eyes: '-ᴥ◕', color: MAGENTA }, // 윙크
    { eyes: '•ᴥ•', color: '' },      // 평온
    { eyes: '-ᴥ-', color: DIM },     // 졸림
    { eyes: '◉ᴥ◉', color: YELLOW }, // 깜짝
    { eyes: '@ᴥ@', color: YELLOW },  // 어지러움
    { eyes: '´•ᴥ•`', color: YELLOW }, // 시무룩
    { eyes: ';ᴥ;', color: CYAN },    // 눈물
    { eyes: 'òᴥó', color: RED },     // 심통
  ];
  const bucket = Math.floor(Date.now() / MOOD_INTERVAL_MS);
  const seedStr = `${bucket}:${data.session_id || ''}`;
  let h = 0;
  for (const ch of seedStr) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const mood = MOODS[h % MOODS.length];

  // ── 곰 3줄: 귀 / 얼굴 / 앞발. 귀는 표정 폭에 맞춰 늘어난다.
  const ears = ` ∩${'─'.repeat(mood.eyes.length + 2)}∩`;
  const face = `ʕ  ${mood.eyes}  ʔ`;
  const body = ' (  u u  )';

  // ── 오른쪽 정보 3줄
  const model = data.model?.display_name || '?';
  const cost = data.cost?.total_cost_usd || 0;
  const info1 = `${CYAN}[${model}]${RESET} | 💰 $${cost.toFixed(2)}`;

  let info2 = '';
  // rate_limits는 Pro/Max 구독자에게 첫 API 응답 이후에만 들어온다
  const fiveH = data.rate_limits?.five_hour;
  if (fiveH && fiveH.used_percentage != null) {
    const p = Math.round(fiveH.used_percentage);
    let reset = '';
    if (fiveH.resets_at) {
      const d = new Date(fiveH.resets_at * 1000);
      reset = ` ${DIM}(${pad2(d.getHours())}:${pad2(d.getMinutes())} 초기화)${RESET}`;
    }
    info2 = `⏳ 세션 ${pctColor(p)}${p}%${RESET}${reset}`;
  }

  let info3 = '';
  const week = data.rate_limits?.seven_day;
  if (week && week.used_percentage != null) {
    const p = Math.round(week.used_percentage);
    let reset = '';
    if (week.resets_at) {
      const d = new Date(week.resets_at * 1000);
      reset = ` ${DIM}(${d.getMonth() + 1}/${d.getDate()}(${DAYS[d.getDay()]}) 초기화)${RESET}`;
    }
    info3 = `📅 주간 ${pctColor(p)}${p}%${RESET}${reset}`;
  }

  // ── 곰 열을 고정 폭으로 맞추고 옆에 정보를 붙인다 (곰 글자는 전부 폭 1)
  const COL = 13;
  const stripAnsi = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');
  const padCol = (s) => s + ' '.repeat(Math.max(0, COL - stripAnsi(s).length));

  console.log(padCol(`${mood.color}${ears}${RESET}`) + info1);
  console.log(info2 ? padCol(`${mood.color}${face}${RESET}`) + info2 : `${mood.color}${face}${RESET}`);
  console.log(info3 ? padCol(`${mood.color}${body}${RESET}`) + info3 : `${mood.color}${body}${RESET}`);
});
