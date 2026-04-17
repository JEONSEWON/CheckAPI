$filePath = "frontend\app\dashboard\page.tsx"
$lines = Get-Content $filePath -Encoding UTF8

# 시작/끝 라인 찾기
$startIdx = -1
$endIdx = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'monitors\.length === 0') {
        $startIdx = $i
    }
    if ($startIdx -ge 0 -and $lines[$i] -match 'Create Monitor' -and $lines[$i] -match 'button') {
        # Create Monitor 버튼 닫는 태그 찾기 (</button> 다음 줄의 </div>)
        $endIdx = $i + 2
        break
    }
}

if ($startIdx -eq -1) {
    Write-Host "❌ monitors.length === 0 블록을 찾지 못했어요." -ForegroundColor Red
    exit
}

Write-Host "✅ 블록 발견: 라인 $($startIdx+1) ~ $($endIdx+1)" -ForegroundColor Cyan

$newBlock = @(
'          {monitors.length === 0 ? (',
'            <div className="px-6 py-10">',
'              <div className="max-w-lg mx-auto">',
'                <h3 className="text-xl font-bold text-gray-900 mb-2 text-center">',
'                  Get started in 3 steps',
'                </h3>',
'                <p className="text-gray-500 text-center mb-8">',
"                  You&apos;ll be monitoring your first API in under 60 seconds.",
'                </p>',
'                <div className="space-y-4">',
'                  <div',
'                    onClick={() => setIsModalOpen(true)}',
'                    className="flex items-start gap-4 p-4 rounded-lg border-2 border-green-200 bg-green-50 cursor-pointer hover:border-green-400 transition"',
'                  >',
'                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center font-bold text-sm">',
'                      1',
'                    </div>',
'                    <div>',
'                      <h4 className="font-semibold text-gray-900">Create your first monitor</h4>',
'                      <p className="text-sm text-gray-600 mt-0.5">',
"                        Enter an API URL and we&apos;ll start checking it automatically.",
'                      </p>',
'                    </div>',
'                    <span className="ml-auto text-green-600 font-medium text-sm whitespace-nowrap">',
'                      Start →',
'                    </span>',
'                  </div>',
'                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 opacity-50">',
'                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">',
'                      2',
'                    </div>',
'                    <div>',
'                      <h4 className="font-semibold text-gray-900">Set up alerts</h4>',
'                      <p className="text-sm text-gray-600 mt-0.5">',
'                        Get notified via Email, Slack, Telegram, Discord, or Webhook.',
'                      </p>',
'                    </div>',
'                  </div>',
'                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 opacity-50">',
'                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">',
'                      3',
'                    </div>',
'                    <div>',
'                      <h4 className="font-semibold text-gray-900">Relax</h4>',
'                      <p className="text-sm text-gray-600 mt-0.5">',
"                        We&apos;ll watch your APIs 24/7 and alert you the moment something breaks.",
'                      </p>',
'                    </div>',
'                  </div>',
'                </div>',
'              </div>',
'            </div>'
)

$newLines = $lines[0..($startIdx-1)] + $newBlock + $lines[($endIdx+1)..($lines.Count-1)]
Set-Content $filePath $newLines -Encoding UTF8
Write-Host "✅ 교체 완료!" -ForegroundColor Green
