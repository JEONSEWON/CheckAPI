FILE = r"C:\home\jeon\api-health-monitor\frontend\components\CreateMonitorModal.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

old_kw = """                  {keyword && (
                    <div className="mt-2 flex items-center gap-3">
                      <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <input
                          type="radio"
                          checked={keywordPresent}
                          onChange={() => setKeywordPresent(true)}
                        />
                        Must be present
                      </label>
                      <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <input
                          type="radio"
                          checked={!keywordPresent}
                          onChange={() => setKeywordPresent(false)}
                        />
                        Must be absent
                      </label>
                    </div>
                  )}"""

new_kw = """                  {keyword && (
                    <div className="mt-2 space-y-2">
                      <div className="flex items-center gap-3">
                        <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                          <input
                            type="radio"
                            checked={keywordPresent}
                            onChange={() => setKeywordPresent(true)}
                          />
                          Must be present
                        </label>
                        <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                          <input
                            type="radio"
                            checked={!keywordPresent}
                            onChange={() => setKeywordPresent(false)}
                          />
                          Must be absent
                        </label>
                      </div>
                      <label className="flex items-center gap-2 text-sm text-orange-600 dark:text-orange-400 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={useRegex}
                          onChange={(e) => setUseRegex(e.target.checked)}
                          className="rounded"
                        />
                        Use as Regex pattern
                      </label>
                      {useRegex && (
                        <p className="text-xs text-gray-400 dark:text-gray-500">e.g. <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">"status":\s*"ok"</code> or <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">[1-9]\d*</code></p>
                      )}
                    </div>
                  )}"""

if old_kw in c:
    c = c.replace(old_kw, new_kw)
    print("Replaced!")
else:
    print("ERROR: not found")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", "Use as Regex" in c)
