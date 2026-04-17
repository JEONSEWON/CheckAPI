import os

# ── 1. CreateMonitorModal - use_regex 토글 추가 ──────────────────────────────
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\components\CreateMonitorModal.tsx"

with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

# state 추가
old_state = "  const [keywordPresent, setKeywordPresent] = useState(true);"
new_state = "  const [keywordPresent, setKeywordPresent] = useState(true);\n  const [useRegex, setUseRegex] = useState(false);"
c = c.replace(old_state, new_state)

# create payload에 use_regex 추가
old_payload = "        ...(keyword ? { keyword, keyword_present: keywordPresent } : {}),"
new_payload = "        ...(keyword ? { keyword, keyword_present: keywordPresent, use_regex: useRegex } : {}),"
c = c.replace(old_payload, new_payload)

# handleClose에 useRegex 리셋
old_close = "    setKeywordPresent(true);"
new_close = "    setKeywordPresent(true);\n    setUseRegex(false);"
c = c.replace(old_close, new_close)

# keyword 입력 필드 찾아서 Regex 토글 UI 추가
# 기존 keyword 관련 JSX 찾기
old_keyword_jsx = """                  className="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="e.g. \\"status\\":\\"ok\\" or \\"error\\":false"
                />"""

# 못 찾을 수 있어서 keyword placeholder로 찾기
if 'status":"ok"' in c or 'status\\":\\"ok\\"' in c or "keyword" in c:
    # keyword input 다음에 오는 체크박스 영역 찾기
    old_keyword_section = '                placeholder="e.g. \\"status\\":\\"ok\\" or \\"error\\":false"'
    if old_keyword_section not in c:
        # 다른 placeholder 찾기
        import re
        match = re.search(r'placeholder="[^"]*error[^"]*"', c)
        if match:
            print(f"Found placeholder: {match.group()}")

# keyword present 체크박스 찾아서 앞에 regex 토글 추가
old_kw_present = """                  <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={keywordPresent}
                      onChange={(e) => setKeywordPresent(e.target.checked)}
                      className="rounded"
                    />
                    Keyword should be present (uncheck = should be absent)
                  </label>"""

new_kw_present = """                  <div className="flex items-center gap-4 mt-1">
                    <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={useRegex}
                        onChange={(e) => setUseRegex(e.target.checked)}
                        className="rounded"
                      />
                      Use Regex
                    </label>
                    <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={keywordPresent}
                        onChange={(e) => setKeywordPresent(e.target.checked)}
                        className="rounded"
                      />
                      Should be present
                    </label>
                  </div>"""

if old_kw_present in c:
    c = c.replace(old_kw_present, new_kw_present)
    print("CreateMonitorModal keyword section replaced!")
else:
    print("WARNING: keyword section not found in CreateMonitorModal, searching...")
    import re
    matches = [(m.start(), c[m.start():m.start()+100]) for m in re.finditer('keywordPresent', c)]
    for pos, snippet in matches:
        print(f"  pos {pos}: {repr(snippet)}")

with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)

print("CreateMonitorModal done!", "useRegex" in c)


# ── 2. Edit 모달 (monitor detail page) - use_regex 토글 추가 ─────────────────
FILE2 = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE2, 'r', encoding='utf-8') as f:
    c2 = f.read()

# handleEdit에서 editForm 초기값에 use_regex 추가
old_edit_form = """      keyword: monitor.keyword || '',
      keyword_present: monitor.keyword_present ?? true,"""
new_edit_form = """      keyword: monitor.keyword || '',
      keyword_present: monitor.keyword_present ?? true,
      use_regex: monitor.use_regex ?? false,"""
c2 = c2.replace(old_edit_form, new_edit_form)

# handleEditSubmit payload에 use_regex 추가
old_submit = """      if (editForm.keyword) {
        payload.keyword = editForm.keyword;
        payload.keyword_present = editForm.keyword_present;
      } else {"""
new_submit = """      if (editForm.keyword) {
        payload.keyword = editForm.keyword;
        payload.keyword_present = editForm.keyword_present;
        payload.use_regex = editForm.use_regex;
      } else {"""
c2 = c2.replace(old_submit, new_submit)

# Edit 모달 keyword 체크박스 옆에 Regex 토글 추가
old_edit_kw = """                {editForm.keyword && (
                  <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={editForm.keyword_present}
                      onChange={e => setEditForm({ ...editForm, keyword_present: e.target.checked })}
                      className="rounded"
                    />
                    Keyword should be <strong>present</strong> (uncheck = should be absent)
                  </label>
                )}"""
new_edit_kw = """                {editForm.keyword && (
                  <div className="flex items-center gap-4 mt-1">
                    <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={editForm.use_regex ?? false}
                        onChange={e => setEditForm({ ...editForm, use_regex: e.target.checked })}
                        className="rounded"
                      />
                      Use Regex
                    </label>
                    <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={editForm.keyword_present}
                        onChange={e => setEditForm({ ...editForm, keyword_present: e.target.checked })}
                        className="rounded"
                      />
                      Should be present
                    </label>
                  </div>
                )}"""
c2 = c2.replace(old_edit_kw, new_edit_kw)

with open(FILE2, 'w', encoding='utf-8') as f:
    f.write(c2)

print("Edit modal done!", "use_regex" in c2)
