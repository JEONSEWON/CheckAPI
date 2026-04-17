file_path = "frontend/components/CreateMonitorModal.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Advanced 섹션에서 Keyword Check 블록 찾아서 제거
# 먼저 Keyword Check 블록 전체 찾기
kw_start = content.find('                {/* Keyword Check */}')
kw_end = content.find('                </div>\n                {/* ', kw_start)
# 다음 주석까지
next_section = content.find('\n                {/* ', kw_start + 1)
old_keyword_block = content[kw_start:next_section]
print("Keyword 블록:")
print(old_keyword_block[:200])

# 2. Advanced 섹션에서 제거
content = content.replace(old_keyword_block, '')
print("✅ Advanced에서 Keyword 제거 완료!")

# 3. URL 입력 필드 다음에 Keyword 섹션 추가
url_input_end = content.find('          {/* Advanced toggle')
if url_input_end == -1:
    url_input_end = content.find('          <button\n            type="button"\n')
    print(f"Advanced toggle 위치: {url_input_end}")

new_keyword_section = '''          {/* Silent Failure Detection */}
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

'''

if url_input_end != -1:
    content = content[:url_input_end] + new_keyword_section + content[url_input_end:]
    print("✅ Keyword 섹션 URL 아래 추가 완료!")
else:
    print("❌ 삽입 위치 못 찾음")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n완료!")
