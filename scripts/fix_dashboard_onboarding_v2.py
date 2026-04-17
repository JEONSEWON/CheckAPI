file_path = "frontend/app/dashboard/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# monitors.length > 0 && monitors.length <= 2 조건 블록을 제거하고
# 모니터 리스트 위에 온보딩을 배너로 보여주도록 변경
old = """          ) : monitors.length > 0 && monitors.length <= 2 ? (
            <div className="px-6 py-6 border-b border-gray-100 dark:border-gray-700">
              <div className="max-w-lg mx-auto">
                <p className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-3 text-center uppercase tracking-wide">Getting started</p>
                <div className="space-y-3">
                  {/* Step 1 — done */}
                  <div className="flex items-center gap-4 p-3 rounded-lg border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-950">
                    <div className="flex-shrink-0 w-7 h-7 rounded-full bg-green-600 text-white flex items-center justify-center text-sm">
                      ✓
                    </div>
                    <p className="text-sm font-medium text-green-700 dark:text-green-400">First monitor created</p>
                  </div>
                  {/* Step 2 — active */}
                  <div
                    onClick={() => window.location.href = '/dashboard/alerts'}
                    className="flex items-start gap-4 p-3 rounded-lg border-2 border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800 cursor-pointer hover:border-green-400 transition"
                  >
                    <div className="flex-shrink-0 w-7 h-7 rounded-full bg-green-600 text-white flex items-center justify-center font-bold text-sm">
                      2
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white text-sm">Set up alerts</h4>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                        Get notified via Email, Slack, Telegram, Discord, or Webhook.
                      </p>
                    </div>
                    <span className="ml-auto text-green-600 font-medium text-xs whitespace-nowrap">
                      Go →
                    </span>
                  </div>
                  {/* Step 3 — inactive */}
                  <div className="flex items-center gap-4 p-3 rounded-lg border border-gray-200 dark:border-gray-700 opacity-50">
                    <div className="flex-shrink-0 w-7 h-7 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      3
                    </div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">Relax — we&apos;ve got it from here</p>
                  </div>
                </div>
              </div>
            </div>
          ) : ("""

new = """          ) : ("""

if old in content:
    content = content.replace(old, new)
    # 모니터 리스트 위에 온보딩 배너 추가
    # monitors.length >= 1 일 때 리스트 위에 작은 배너로 표시
    content = content.replace(
        """          ) : (
            <div className="divide-y divide-gray-200">
              {monitors.map((monitor) => (
                <MonitorRow key={monitor.id} monitor={monitor} />
              ))}
            </div>""",
        """          ) : (
            <>
              {monitors.length <= 2 && (
                <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 bg-green-50 dark:bg-green-950">
                  <div className="flex items-center gap-6 flex-wrap">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-green-600 text-white flex items-center justify-center text-xs">✓</div>
                      <span className="text-sm text-green-700 dark:text-green-400 font-medium">Monitor created</span>
                    </div>
                    <div
                      onClick={() => window.location.href = '/dashboard/alerts'}
                      className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition"
                    >
                      <div className="w-6 h-6 rounded-full bg-green-600 text-white flex items-center justify-center text-xs font-bold">2</div>
                      <span className="text-sm text-green-700 dark:text-green-400 font-medium underline">Set up alerts →</span>
                    </div>
                    <div className="flex items-center gap-2 opacity-40">
                      <div className="w-6 h-6 rounded-full bg-gray-300 text-white flex items-center justify-center text-xs font-bold">3</div>
                      <span className="text-sm text-gray-600 dark:text-gray-400">Relax</span>
                    </div>
                  </div>
                </div>
              )}
              <div className="divide-y divide-gray-200">
                {monitors.map((monitor) => (
                  <MonitorRow key={monitor.id} monitor={monitor} />
                ))}
              </div>
            </>"""
    )
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 교체 성공!")
else:
    print("❌ 못 찾음")
