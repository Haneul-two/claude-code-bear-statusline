// 곰 상태표시줄: 곰 표정(감정) | 모델명 | 세션 비용 | 5시간 한도(초기화 시각) | 주간 한도(초기화 날짜)
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
    CYAN = '\x1b[36m', DIM = '\x1b[2m', RESET = '\x1b[0m';

  const pctColor = (p) => (p >= 90 ? RED : p >= 70 ? YELLOW : GREEN);
  const DAYS = ['일', '월', '화', '수', '목', '금', '토'];
  const pad = (n) => String(n).padStart(2, '0');

  const model = data.model?.display_name || '?';
  const cost = data.cost?.total_cost_usd || 0;

  // 곰의 감정: 세션·주간 한도 중 더 높은 사용률 기준. 한도 정보가 오기 전엔 기본 표정.
  const sessionPct = data.rate_limits?.five_hour?.used_percentage;
  const weekPct = data.rate_limits?.seven_day?.used_percentage;
  let bear;
  if (data.exceeds_200k_tokens) {
    bear = `${RED}ʕ@ᴥ@ʔ${RESET} ${DIM}과부하${RESET}`; // 컨텍스트 한계 — 눈이 핑핑
  } else if (sessionPct == null && weekPct == null) {
    bear = 'ʕ•ᴥ•ʔ'; // 아직 한도 정보 없음 — 기본 표정
  } else {
    const worst = Math.max(sessionPct ?? 0, weekPct ?? 0);
    bear =
      worst >= 90 ? `${RED}ʕ;ᴥ;ʔ${RESET} ${DIM}비상${RESET}`
      : worst >= 70 ? `${YELLOW}ʕ´•ᴥ•\`ʔ${RESET} ${DIM}긴장${RESET}`
      : worst >= 40 ? `ʕ•ᴥ•ʔ ${DIM}평온${RESET}`
      : `${GREEN}ʕ◕ᴥ◕ʔ${RESET} ${DIM}여유${RESET}`;
  }

  const parts = [
    `${bear} ${CYAN}[${model}]${RESET}`,
    `💰 $${cost.toFixed(2)}`,
  ];

  // rate_limits는 Pro/Max 구독자에게 첫 API 응답 이후에만 들어온다
  const fiveH = data.rate_limits?.five_hour;
  if (fiveH && fiveH.used_percentage != null) {
    const p = Math.round(fiveH.used_percentage);
    let reset = '';
    if (fiveH.resets_at) {
      const d = new Date(fiveH.resets_at * 1000);
      reset = ` ${DIM}(${pad(d.getHours())}:${pad(d.getMinutes())} 초기화)${RESET}`;
    }
    parts.push(`⏳ 세션 ${pctColor(p)}${p}%${RESET}${reset}`);
  }

  const week = data.rate_limits?.seven_day;
  if (week && week.used_percentage != null) {
    const p = Math.round(week.used_percentage);
    let reset = '';
    if (week.resets_at) {
      const d = new Date(week.resets_at * 1000);
      reset = ` ${DIM}(${d.getMonth() + 1}/${d.getDate()}(${DAYS[d.getDay()]}) 초기화)${RESET}`;
    }
    parts.push(`📅 주간 ${pctColor(p)}${p}%${RESET}${reset}`);
  }

  console.log(parts.join(' | '));
});
