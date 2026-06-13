# 🐻 claude-code-bear-statusline

Claude Code용 곰 상태표시줄. 모델명, 세션 비용, 5시간 세션 한도(초기화 **시각**), 주간 한도(초기화 **날짜**)를 한 줄로 보여줍니다.

A bear-themed status line for Claude Code — shows model name, session cost, 5-hour session limit (with reset time) and weekly limit (with reset date) in one line.

```
🐻 [Fable 5] | 💰 $1.23 | ⏳ 세션 24% (10:55 초기화) | 📅 주간 81% (6/18(목) 초기화)
```

## 표시 항목

| 항목 | 의미 |
|---|---|
| 🐻 `[모델명]` | 현재 세션에서 사용 중인 모델 |
| 💰 `$1.23` | 현재 세션의 누적 비용 (API 요금 환산치, USD) |
| ⏳ `세션 24% (10:55 초기화)` | 5시간 세션 한도 사용률과 초기화 시각 |
| 📅 `주간 81% (6/18(목) 초기화)` | 주간(7일) 한도 사용률과 초기화 날짜 |

사용률 색상: **70% 미만 초록 · 70~89% 노랑 · 90% 이상 빨강**

> 한도 정보(`rate_limits`)는 Claude Pro/Max 구독자에게 세션의 첫 API 응답 이후부터 전달됩니다.
> 새 세션 시작 직후에는 `🐻 [모델] | 💰 $0.00`만 표시되는 것이 정상입니다.

## 설치

요구사항: [Node.js](https://nodejs.org) (의존성 패키지 없음, 스크립트 파일 하나면 됩니다)

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

자세한 스키마는 [Claude Code 상태표시줄 공식 문서](https://code.claude.com/docs/en/statusline)를 참고하세요.

## 커스터마이징

- **마스코트 변경**: 스크립트의 `🐻`를 원하는 이모지로 바꾸면 됩니다 (🐱 🐶 🦊 …)
- **요일 표기**: `DAYS` 배열(`['일', '월', ...]`)을 수정해 다른 언어로 변경
- **색상 임계값**: `pctColor` 함수의 `90` / `70` 값을 조정

## License

MIT
