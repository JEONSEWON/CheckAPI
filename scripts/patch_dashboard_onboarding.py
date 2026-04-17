file_path = "frontend/app/dashboard/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# monitors.length === 0 일 때만 온보딩 보여주던 것을
# monitors.length < 3 이거나 onboarding이 완료되지 않은 경우에도 보여주도록 변경
# Step 1: 모니터 있으면 체크 표시, Step 2: 알림 채널로 이동 유도

old = """          {monitors.length === 0 ? (
            <div className="px-6 py-10">
              <div className="max-w-lg mx-auto">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 text-center">
                  Get started in 3 steps
                </h3>
                <p className="text-gray-500 dark:text-gray-400 text-center mb-8">
                  You&apos;ll be monitoring your first API in under 60 seconds.
                </p>
                <div className="space-y-4">
                  <div
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-start gap-4 p-4 rounded-lg border-2 border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800 cursor-pointer hover:border-green-400 transition"
                  >
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center font-bold text-sm">
                      1
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Create your first monitor</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
                        Enter an API URL and we&apos;ll start checking it automatically.
                      </p>
                    </div>
                    <span className="ml-auto text-green-600 font-medium text-sm whitespace-nowrap">
                      Start →
                    </span>
                  </div>
                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700 opacity-50">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      2
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Set up alerts</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
                        Get notified via Email, Slack, Telegram, Discord, or Webhook.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700 opacity-50">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      3
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Relax</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
                        We&apos;ll watch your APIs 24/7 and alert you the moment something breaks.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : ("""

new = """          {monitors.length === 0 ? (
            <div className="px-6 py-10">
              <div className="max-w-lg mx-auto">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 text-center">
                  Get started in 3 steps
                </h3>
                <p className="text-gray-500 dark:text-gray-400 text-center mb-8">
                  You&apos;ll be monitoring your first API in under 60 seconds.
                </p>
                <div className="space-y-4">
                  <div
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-start gap-4 p-4 rounded-lg border-2 border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800 cursor-pointer hover:border-green-400 transition"
                  >
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center font-bold text-sm">
                      1
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Create your first monitor</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
                        Enter an API URL and we&apos;ll start checking it automatically.
                      </p>
                    </div>
                    <span className="ml-auto text-green-600 font-medium text-sm whitespace-nowrap">
                      Start →
                    </span>
                  </div>
                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700 opacity-50">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      2
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Set up alerts</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
                        Get notified via Email, Slack, Telegram, Discord, or Webhook.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700 opacity-50">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      3
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Relax</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
                        We&apos;ll watch your APIs 24/7 and alert you the moment something breaks.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : monitors.length > 0 && monitors.length <= 2 ? (
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

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 교체 성공!")
else:
    print("❌ 블록을 찾지 못했어요.")
