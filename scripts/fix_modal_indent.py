file_path = "frontend/components/CreateMonitorModal.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 들여쓰기 잘못된 부분 수정
old = """            {/* Silent Failure Detection */}
          <div className="bg-orange-50 dark:bg-orange-950 border border-orange-200 dark:border-orange-800 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-orange-500">⚡</span>
              <label className="text-sm font-semibold text-orange-700 dark:text-orange-400">
                Silent Failure Detection
              </label>
              <span className="text-xs text-orange-500 bg-orange-100 dark:bg-orange-900 px-2 py-0.5 rounded-full">Optional</span>
            </div>
            <p className="text-xs text-orange-600 dark:text-orange-400 mb-3">
              Catch failures even when your API returns 200 OK — check if a keyword exists in the response body.
            </p>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder='e.g. "status":"ok" or "error":false'
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                className="flex-1 px-3 py-2 border border-orange-200 dark:border-orange-700 rounded-lg text-sm focus:ring-2 focus:ring-orange-400 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
              />
              <select
                value={keywordPresent ? 'present' : 'absent'}
                onChange={(e) => setKeywordPresent(e.target.value === 'present')}
                className="px-3 py-2 border border-orange-200 dark:border-orange-700 rounded-lg text-sm text-gray-900 dark:text-white bg-white dark:bg-gray-700"
              >
                <option value="present">Must exist</option>
                <option value="absent">Must not exist</option>
              </select>
            </div>
          </div>
          {/* Advanced toggle */}"""

new = """            {/* Silent Failure Detection */}
            <div className="bg-orange-50 dark:bg-orange-950 border border-orange-200 dark:border-orange-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-orange-500">⚡</span>
                <label className="text-sm font-semibold text-orange-700 dark:text-orange-400">
                  Silent Failure Detection
                </label>
                <span className="text-xs text-orange-500 bg-orange-100 dark:bg-orange-900 px-2 py-0.5 rounded-full">Optional</span>
              </div>
              <p className="text-xs text-orange-600 dark:text-orange-400 mb-3">
                Catch failures even when your API returns 200 OK — check if a keyword exists in the response body.
              </p>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder='e.g. "status":"ok" or "error":false'
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  className="flex-1 px-3 py-2 border border-orange-200 dark:border-orange-700 rounded-lg text-sm focus:ring-2 focus:ring-orange-400 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                />
                <select
                  value={keywordPresent ? 'present' : 'absent'}
                  onChange={(e) => setKeywordPresent(e.target.value === 'present')}
                  className="px-3 py-2 border border-orange-200 dark:border-orange-700 rounded-lg text-sm text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                >
                  <option value="present">Must exist</option>
                  <option value="absent">Must not exist</option>
                </select>
              </div>
            </div>
            {/* Advanced toggle */}"""

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
