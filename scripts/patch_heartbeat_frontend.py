import os

# ── 1. CreateMonitorModal에 Heartbeat 타입 추가 ───────────────────────────────
FILE_MODAL = r"C:\home\jeon\api-health-monitor\frontend\components\CreateMonitorModal.tsx"

with open(FILE_MODAL, 'r', encoding='utf-8') as f:
    c = f.read()

# 1-1. import에 Activity 추가
old_import = "import { X, Loader2, CheckCircle, XCircle, ArrowRight, Zap } from 'lucide-react';"
new_import = "import { X, Loader2, CheckCircle, XCircle, ArrowRight, Zap, Activity } from 'lucide-react';"
c = c.replace(old_import, new_import)

# 1-2. state에 monitorType, heartbeatInterval, heartbeatGrace 추가
old_state = "  const [showUpgradeModal, setShowUpgradeModal] = useState(false);"
new_state = """  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [monitorType, setMonitorType] = useState<'http' | 'heartbeat'>('http');
  const [heartbeatInterval, setHeartbeatInterval] = useState(60);
  const [heartbeatGrace, setHeartbeatGrace] = useState(5);
  const [createdHeartbeatToken, setCreatedHeartbeatToken] = useState<string | null>(null);"""
c = c.replace(old_state, new_state)

# 1-3. handleClose에 reset 추가
old_close_reset = "    setKeywordPresent(true);\n    setUseRegex(false);\n    setCheckResult(null);\n    setShowAdvanced(false);\n    onClose();"
new_close_reset = """    setKeywordPresent(true);
    setUseRegex(false);
    setCheckResult(null);
    setShowAdvanced(false);
    setMonitorType('http');
    setHeartbeatInterval(60);
    setHeartbeatGrace(5);
    setCreatedHeartbeatToken(null);
    onClose();"""
c = c.replace(old_close_reset, new_close_reset)

# 1-4. handleSubmit에서 heartbeat 처리 추가
old_submit_start = """  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setCheckResult(null);
    try {
      const monitor = await monitorsAPI.create({
        name: generateName(url),
        url,
        method,
        interval: 300, // Free plan default
        timeout: 30,
        expected_status: expectedStatus,
        ...(keyword ? { keyword, keyword_present: keywordPresent, use_regex: useRegex } : {}),
      });"""

new_submit_start = """  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setCheckResult(null);
    try {
      if (monitorType === 'heartbeat') {
        const monitor = await monitorsAPI.create({
          name: url || 'Heartbeat Monitor',
          url: 'heartbeat',
          method: 'GET',
          interval: heartbeatInterval * 60,
          timeout: 30,
          expected_status: 200,
          monitor_type: 'heartbeat',
          heartbeat_interval: heartbeatInterval,
          heartbeat_grace: heartbeatGrace,
        } as any);
        setCreatedHeartbeatToken((monitor as any).heartbeat_token);
        toast.success('Heartbeat monitor created!');
        onSuccess();
        setIsLoading(false);
        return;
      }
      const monitor = await monitorsAPI.create({
        name: generateName(url),
        url,
        method,
        interval: 300,
        timeout: 30,
        expected_status: expectedStatus,
        ...(keyword ? { keyword, keyword_present: keywordPresent, use_regex: useRegex } : {}),
      });"""

c = c.replace(old_submit_start, new_submit_start)

# 1-5. 모달 헤더 아래에 타입 선택 탭 추가
old_url_label = """            {/* URL */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                API URL *
              </label>"""

new_url_label = """            {/* Monitor Type Tabs */}
            <div className="flex gap-2 p-1 bg-gray-100 dark:bg-gray-900 rounded-lg">
              {[
                { type: 'http', label: '🌐 HTTP Monitor', desc: 'Check URL uptime' },
                { type: 'heartbeat', label: '💓 Heartbeat / Cron', desc: 'Cron job monitoring' },
              ].map((t) => (
                <button
                  key={t.type}
                  type="button"
                  onClick={() => setMonitorType(t.type as 'http' | 'heartbeat')}
                  className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition text-left ${
                    monitorType === t.type
                      ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  <div>{t.label}</div>
                  <div className="text-xs font-normal opacity-60">{t.desc}</div>
                </button>
              ))}
            </div>

            {/* Heartbeat UI */}
            {monitorType === 'heartbeat' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Monitor Name *</label>
                  <input
                    type="text"
                    required
                    value={url}
                    onChange={e => setUrl(e.target.value)}
                    placeholder="e.g. Daily Backup Job"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Expected every (min)</label>
                    <input
                      type="number"
                      min={1}
                      max={10080}
                      value={heartbeatInterval}
                      onChange={e => setHeartbeatInterval(Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Grace period (min)</label>
                    <input
                      type="number"
                      min={1}
                      max={1440}
                      value={heartbeatGrace}
                      onChange={e => setHeartbeatGrace(Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                    />
                  </div>
                </div>
                <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-3 text-sm text-blue-700 dark:text-blue-300">
                  Alert fires if no ping received within <strong>{heartbeatInterval + heartbeatGrace} minutes</strong> ({heartbeatInterval}m interval + {heartbeatGrace}m grace).
                </div>
              </div>
            )}

            {/* URL — only for HTTP */}
            {monitorType === 'http' && <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                API URL *
              </label>"""

c = c.replace(old_url_label, new_url_label)

# URL 입력 div 닫는 태그 뒤에 조건부 닫기 추가
old_url_close = """              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                placeholder="https://api.example.com/health"
              />
            </div>"""

new_url_close = """              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent text-gray-900 dark:text-white bg-white dark:bg-gray-700"
                placeholder="https://api.example.com/health"
              />
            </div>}"""

c = c.replace(old_url_close, new_url_close)

# Check Result, Advanced options도 HTTP 전용으로
old_check_result = "            {/* Check Result */}\n            {checkResult && ("
new_check_result = "            {/* Check Result */}\n            {monitorType === 'http' && checkResult && ("
c = c.replace(old_check_result, new_check_result)

old_advanced = "            {/* Advanced toggle */}"
new_advanced = "            {/* Advanced toggle — HTTP only */}\n            {monitorType === 'http' && <>"
c = c.replace(old_advanced, new_advanced)

# Submit 버튼 앞에서 advanced 닫기
old_submit_btn = """            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}"""

new_submit_btn = """            {monitorType === 'http' && </>}

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}"""

c = c.replace(old_submit_btn, new_submit_btn)

# Submit 버튼 텍스트 조건부
old_btn_text = "              'Start Monitoring'"
new_btn_text = "              monitorType === 'heartbeat' ? 'Create Heartbeat Monitor' : 'Start Monitoring'"
c = c.replace(old_btn_text, new_btn_text)

with open(FILE_MODAL, 'w', encoding='utf-8') as f:
    f.write(c)
print("CreateMonitorModal done!", "heartbeat" in c)


# ── 2. api.ts monitorsAPI.create에 monitor_type 추가 ─────────────────────────
FILE_API = r"C:\home\jeon\api-health-monitor\frontend\lib\api.ts"

with open(FILE_API, 'r', encoding='utf-8') as f:
    c = f.read()

old_create = """  create: (data: {
    name: string;
    url: string;
    method?: string;"""

new_create = """  create: (data: {
    name: string;
    url: string;
    method?: string;
    monitor_type?: string;"""

c = c.replace(old_create, new_create)

with open(FILE_API, 'w', encoding='utf-8') as f:
    f.write(c)
print("api.ts done!")


# ── 3. 대시보드 모니터 목록에 heartbeat 배지 추가 ────────────────────────────
FILE_DASHBOARD = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\page.tsx"

with open(FILE_DASHBOARD, 'r', encoding='utf-8') as f:
    c = f.read()

# pending 상태 색상 추가
old_status = "    up: { bg: 'bg-green-100 dark:bg-green-900', dot: 'bg-green-500', text: 'text-green-700 dark:text-green-300' },"
if old_status in c:
    new_status = """    up: { bg: 'bg-green-100 dark:bg-green-900', dot: 'bg-green-500', text: 'text-green-700 dark:text-green-300' },
    pending: { bg: 'bg-gray-100 dark:bg-gray-800', dot: 'bg-gray-400', text: 'text-gray-600 dark:text-gray-400' },"""
    c = c.replace(old_status, new_status)
    print("Dashboard pending status added!")

with open(FILE_DASHBOARD, 'w', encoding='utf-8') as f:
    f.write(c)
print("Dashboard done!")
