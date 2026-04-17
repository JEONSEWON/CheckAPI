FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. state 추가
old_state = "  const [checks, setChecks] = useState<any[]>([]);\n  const [loading, setLoading] = useState(true);"
new_state = """  const [checks, setChecks] = useState<any[]>([]);
  const [checksTotal, setChecksTotal] = useState(0);
  const [checksPage, setChecksPage] = useState(1);
  const [checksLoadingMore, setChecksLoadingMore] = useState(false);
  const [loading, setLoading] = useState(true);"""
content = content.replace(old_state, new_state)

# 2. loadData의 checks 부분 수정
old_checks_load = """      // Get recent checks
      const checksResponse = await monitorsAPI.checks(monitorId, {
        page: 1,
        page_size: 20,
        hours: 24
      });
      setChecks(checksResponse.checks);"""
new_checks_load = """      // Get recent checks
      const checksResponse = await monitorsAPI.checks(monitorId, {
        page: 1,
        page_size: 20,
      });
      setChecks(checksResponse.checks);
      setChecksTotal(checksResponse.total);
      setChecksPage(1);"""
content = content.replace(old_checks_load, new_checks_load)

# 3. handleLoadMoreChecks 함수 추가 (handleDelete 앞에)
old_delete = "  const handleDelete = async () => {"
new_load_more = """  const handleLoadMoreChecks = async () => {
    setChecksLoadingMore(true);
    try {
      const nextPage = checksPage + 1;
      const checksResponse = await monitorsAPI.checks(monitorId, {
        page: nextPage,
        page_size: 20,
      });
      setChecks(prev => [...prev, ...checksResponse.checks]);
      setChecksTotal(checksResponse.total);
      setChecksPage(nextPage);
    } catch (error) {
      toast.error('Failed to load more checks');
    } finally {
      setChecksLoadingMore(false);
    }
  };

  const handleDelete = async () => {"""
content = content.replace(old_delete, new_load_more)

# 4. Recent Checks 섹션에 헤더 카운트 + 더 보기 버튼 추가
old_checks_section = """        {/* Recent Checks */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Checks</h2>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {checks.length === 0 ? (
              <div className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                No checks yet
              </div>
            ) : (
              checks.map((check) => (
                <CheckRow key={check.id} check={check} />
              ))
            )}
          </div>
        </div>"""
new_checks_section = """        {/* Recent Checks */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Checks</h2>
            <span className="text-sm text-gray-500 dark:text-gray-400">{checks.length} / {checksTotal}</span>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {checks.length === 0 ? (
              <div className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                No checks yet
              </div>
            ) : (
              checks.map((check) => (
                <CheckRow key={check.id} check={check} />
              ))
            )}
          </div>
          {checks.length < checksTotal && (
            <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={handleLoadMoreChecks}
                disabled={checksLoadingMore}
                className="w-full py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-green-500 transition disabled:opacity-50"
              >
                {checksLoadingMore ? 'Loading...' : `Load more (${checksTotal - checks.length} remaining)`}
              </button>
            </div>
          )}
        </div>"""
content = content.replace(old_checks_section, new_checks_section)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("checksTotal state:", "checksTotal" in content)
print("handleLoadMoreChecks:", "handleLoadMoreChecks" in content)
print("Load more button:", "Load more" in content)
