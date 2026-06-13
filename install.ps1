# 곰 상태표시줄 원클릭 설치 (Windows PowerShell 5.1+)
# 사용법: irm https://raw.githubusercontent.com/Haneul-two/claude-code-bear-statusline/main/install.ps1 | iex
# 주의: 이 파일은 UTF-8(BOM 없음)이며 irm|iex 실행 기준입니다.
#       PS 5.1에서 파일을 직접 실행하면 한글이 깨질 수 있으니 위 한 줄 명령을 사용하세요.
& {
  $ErrorActionPreference = 'Stop'

  if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host 'Node.js가 필요합니다. https://nodejs.org 에서 설치 후 다시 실행해 주세요.' -ForegroundColor Red
    return
  }

  $claudeDir = Join-Path $env:USERPROFILE '.claude'
  if (-not (Test-Path $claudeDir)) { New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null }

  $dest = Join-Path $claudeDir 'statusline-bear.js'
  Invoke-WebRequest -UseBasicParsing `
    -Uri 'https://raw.githubusercontent.com/Haneul-two/claude-code-bear-statusline/main/statusline-bear.js' `
    -OutFile $dest

  # settings.json의 statusLine만 갱신하고 나머지 설정은 보존한다
  $settingsPath = Join-Path $claudeDir 'settings.json'
  if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
  } else {
    $settings = New-Object PSObject
  }
  $statusLine = [PSCustomObject]@{ type = 'command'; command = "node `"$dest`"" }
  if ($settings.PSObject.Properties['statusLine']) {
    $settings.statusLine = $statusLine
  } else {
    $settings | Add-Member -MemberType NoteProperty -Name statusLine -Value $statusLine
  }
  $json = $settings | ConvertTo-Json -Depth 100
  [System.IO.File]::WriteAllText($settingsPath, $json, (New-Object System.Text.UTF8Encoding($false)))

  Write-Host ''
  Write-Host ' ∩─────∩' -ForegroundColor Green
  Write-Host 'ʕ  ◕ᴥ◕  ʔ  설치 완료!' -ForegroundColor Green
  Write-Host ' (  u u  )  Claude Code를 재시작하면 곰이 나타납니다.' -ForegroundColor Green
}
