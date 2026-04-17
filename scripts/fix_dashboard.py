import re

file_path = "frontend/app/dashboard/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = """          {monitors.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No monitors yet
              </h3>
              <p className="text-gray-600 mb-4">
                Get started by creating your first monitor
              </p>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
              >
                Create Monitor
              </button>
            </div>"""

new = """          {monitors.length === 0 ? (
            <div className="px-6 py-10">
              <div className="max-w-lg mx-auto">
                <h3 className="text-xl font-bold text-gray-900 mb-2 text-center">
                  Get started in 3 steps
                </h3>
                <p className="text-gray-500 text-center mb-8">
                  You&apos;ll be monitoring your first API in under 60 seconds.
                </p>
                <div className="space-y-4">
                  <div
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-start gap-4 p-4 rounded-lg border-2 border-green-200 bg-green-50 cursor-pointer hover:border-green-400 transition"
                  >
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center font-bold text-sm">
                      1
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Create your first monitor</h4>
                      <p className="text-sm text-gray-600 mt-0.5">
                        Enter an API URL and we&apos;ll start checking it automatically.
                      </p>
                    </div>
                    <span className="ml-auto text-green-600 font-medium text-sm whitespace-nowrap">
                      Start →
                    </span>
                  </div>
                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 opacity-50">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      2
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Set up alerts</h4>
                      <p className="text-sm text-gray-600 mt-0.5">
                        Get notified via Email, Slack, Telegram, Discord, or Webhook.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4 p-4 rounded-lg border border-gray-200 opacity-50">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center font-bold text-sm">
                      3
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Relax</h4>
                      <p className="text-sm text-gray-600 mt-0.5">
                        We&apos;ll watch your APIs 24/7 and alert you the moment something breaks.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>"""

if old in content:
    new_content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    print("✅ 교체 성공!")
else:
    print("❌ 블록을 찾지 못했어요.")
