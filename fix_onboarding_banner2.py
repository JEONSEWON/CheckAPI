file_path = "frontend/app/dashboard/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = """          ) : (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {monitors.map((monitor) => (
                <MonitorRow key={monitor.id} monitor={monitor} />
              ))}
            </div>"""

new = """          ) : (
            <>
              {monitors.length <= 2 && (
                <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 bg-green-50 dark:bg-green-950">
                  <p className="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wide mb-3">Getting started</p>
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
              <div className="divide-y divide-gray-200 dark:divide-gray-700">
                {monitors.map((monitor) => (
                  <MonitorRow key={monitor.id} monitor={monitor} />
                ))}
              </div>
            </>"""

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 교체 성공!")
else:
    print("❌ 못 찾음")
