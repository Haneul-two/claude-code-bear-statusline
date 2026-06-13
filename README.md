# 🐻 claude-code-bear-statusline

Claude Code용 곰 상태표시줄. **다마고치처럼 1분마다 기분이 랜덤으로 바뀌는 곰(3줄)** 옆에 모델명, 세션 비용, 5시간 세션 한도(초기화 **시각**), 주간 한도(초기화 **날짜**)를 보여줍니다.

A bear-themed status line for Claude Code — a tamagotchi-style bear whose **mood changes randomly every minute** (3-line layout with ears and paws!), with model name, session cost, 5-hour session limit (with reset time) and weekly limit (with reset date) beside it.

```
 ∩─────∩     [Fable 5] | 💰 $1.23
ʕ  ≧ᴥ≦  ʔ    ⏳ 세션 24% (10:55 초기화)
 (  u u  )   📅 주간 81% (6/18(목) 초기화)
```

## 표시 항목

| 항목 | 의미 |
|---|---|
| `ʕ  ≧ᴥ≦  ʔ` | 곰의 기분 — 1분마다 표정이 랜덤으로 바뀝니다 (아래 표 참고) |
| `[모델명]` | 현재 세션에서 사용 중인 모델 |
| 💰 `$1.23` | 현재 세션의 누적 비용 (API 요금 환산치, USD) |
| ⏳ `세션 24% (10:55 초기화)` | 5시간 세션 한도 사용률과 초기화 시각 |
| 📅 `주간 81% (6/18(목) 초기화)` | 주간(7일) 한도 사용률과 초기화 날짜 |

사용률 색상: **70% 미만 초록 · 70~89% 노랑 · 90% 이상 빨강**

## 곰의 기분

다마고치처럼 **1분마다 기분이 랜덤으로** 바뀝니다. 한도 사용률과는 무관한 순수한 기분이며, 기분 단어 없이 표정과 색상으로만 표현됩니다.
(매 실행마다 바뀌면 깜빡거리므로, 시간 버킷 + 세션 ID를 시드로 사용해 같은 1분 안에서는 같은 기분을 유지합니다. 세션마다 기분도 다릅니다.)

| 표정 | 기분 | 색상 |
|---|---|---|
| ʕ  ◕ᴥ◕  ʔ | 신남 | 초록 |
| ʕ  ≧ᴥ≦  ʔ | 행복 | 초록 |
| ʕ  -ᴥ◕  ʔ | 윙크 | 자홍 |
| ʕ  •ᴥ•  ʔ | 평온 | 기본 |
| ʕ  -ᴥ-  ʔ | 졸림 | 흐림 |
| ʕ  ◉ᴥ◉  ʔ | 깜짝 | 노랑 |
| ʕ  @ᴥ@  ʔ | 어지러움 | 노랑 |
| ʕ  ´•ᴥ•\`  ʔ | 시무룩 | 노랑 |
| ʕ  ;ᴥ;  ʔ | 눈물 | 청록 |
| ʕ  òᴥó  ʔ | 심통 | 빨강 |

귀(`∩─────∩`)는 표정 폭에 맞춰 자동으로 늘어납니다. 한도 사용률 색상(초록/노랑/빨강)은 숫자 쪽에 그대로 유지됩니다.

> 한도 정보(`rate_limits`)는 Claude Pro/Max 구독자에게 세션의 첫 API 응답 이후부터 전달됩니다.
> 새 세션 시작 직후에는 `🐻 [모델] | 💰 $0.00`만 표시되는 것이 정상입니다.

## 설치

요구사항: [Node.js](https://nodejs.org) (의존성 패키지 없음, 스크립트 파일 하나면 됩니다)

### 원클릭 설치

터미널에서 한 줄만 실행하면 됩니다. 스크립트를 `~/.claude/`에 내려받고 `settings.json`의 `statusLine` 항목만 추가합니다 (기존 설정은 그대로 보존).

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/Haneul-two/claude-code-bear-statusline/main/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/Haneul-two/claude-code-bear-statusline/main/install.sh | bash
```

설치 후 Claude Code를 재시작하면 곰이 나타납니다.

### 수동 설치

1. `statusline-bear.js`를 원하는 위치에 저장합니다. 예: `~/.claude/statusline-bear.js`

2. `~/.claude/settings.json`에 statusLine 설정을 추가합니다.

   **Windows:**
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "node \"C:\\Users\\<사용자명>\\.claude\\statusline-bear.js\""
     }
   }
   ```

   **macOS / Linux:**
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "node ~/.claude/statusline-bear.js"
     }
   }
   ```

3. Claude Code를 재시작하면 적용됩니다.

## 동작 원리

Claude Code는 상태표시줄 명령에 세션 정보를 JSON으로 stdin에 전달합니다. 이 스크립트가 사용하는 필드:

- `model.display_name` — 모델명
- `cost.total_cost_usd` — 세션 누적 비용
- `rate_limits.five_hour.used_percentage` / `.resets_at` — 5시간 한도 사용률·초기화 시점(Unix epoch)
- `rate_limits.seven_day.used_percentage` / `.resets_at` — 주간 한도 사용률·초기화 시점(Unix epoch)
- `session_id` — 기분 랜덤 시드 (세션마다 다른 기분)

자세한 스키마는 [Claude Code 상태표시줄 공식 문서](https://code.claude.com/docs/en/statusline)를 참고하세요.

## 커스터마이징

- **기분 추가/변경**: `MOODS` 배열에 `{ eyes, color }`를 추가하거나 수정
- **기분 전환 주기**: `MOOD_INTERVAL_MS` 값을 조정 (기본 1분)
- **곰 열 폭**: 정보 열이 너무 붙거나 멀면 `COL` 값을 조정
- **요일 표기**: `DAYS` 배열(`['일', '월', ...]`)을 수정해 다른 언어로 변경
- **색상 임계값**: `pctColor` 함수의 `90` / `70` 값을 조정

## License

MIT
