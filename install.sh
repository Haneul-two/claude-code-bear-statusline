#!/usr/bin/env bash
# 곰 상태표시줄 원클릭 설치 (macOS / Linux)
# 사용법: curl -fsSL https://raw.githubusercontent.com/Haneul-two/claude-code-bear-statusline/main/install.sh | bash
set -euo pipefail

# 로케일이 한국어면 한국어, 아니면 영어 메시지 (Korean locale -> Korean, else English)
case "${LANG:-}${LC_ALL:-}" in
  *ko*) KO=1 ;;
  *) KO=0 ;;
esac

if ! command -v node >/dev/null 2>&1; then
  if [ "$KO" = 1 ]; then
    echo 'Node.js가 필요합니다. https://nodejs.org 에서 설치 후 다시 실행해 주세요.' >&2
  else
    echo 'Node.js is required. Install it from https://nodejs.org and run again.' >&2
  fi
  exit 1
fi

CLAUDE_DIR="$HOME/.claude"
DEST="$CLAUDE_DIR/statusline-bear.js"
mkdir -p "$CLAUDE_DIR"

curl -fsSL 'https://raw.githubusercontent.com/Haneul-two/claude-code-bear-statusline/main/statusline-bear.js' -o "$DEST"

# settings.json의 statusLine만 갱신하고 나머지 설정은 보존한다
node - "$CLAUDE_DIR" <<'EOF'
const fs = require('fs');
const path = require('path');
const dir = process.argv[2];
const settingsPath = path.join(dir, 'settings.json');
let settings = {};
try { settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8').replace(/^﻿/, '')); } catch {}
settings.statusLine = { type: 'command', command: `node "${path.join(dir, 'statusline-bear.js')}"` };
fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
EOF

echo ''
echo ' ∩─────∩'
if [ "$KO" = 1 ]; then
  echo 'ʕ  ◕ᴥ◕  ʔ  설치 완료!'
  echo ' (  u u  )  Claude Code를 재시작하면 곰이 나타납니다.'
else
  echo 'ʕ  ◕ᴥ◕  ʔ  Done!'
  echo ' (  u u  )  Restart Claude Code and the bear appears.'
fi
