FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# activeTab state 추가
old_state = "  const [showEditModal, setShowEditModal] = useState(false);"
new_state = """  const [showEditModal, setShowEditModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'assertions' | 'alerts' | 'history'>('overview');"""
c = c.replace(old_state, new_state)

# Status Badge 이후 전체 섹션을 탭으로 교체
old_sections = """        {/* Stats */}
        {analytics && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Uptime (7 days)"
              value={`${analytics.uptime_percentage}%`}
              icon={<CheckCircle className="h-6 w-6 text-green-600" />}
            />
            <StatCard
              title="Avg Response Time"
              value={`${analytics.avg_response_time}ms`}
              icon={<Clock className="h-6 w-6 text-blue-600" />}
            />
            <StatCard
              title="Total Checks"
              value={analytics.total_checks}
              icon={<Activity className="h-6 w-6 text-purple-600" />}
            />
            <StatCard
              title="Incidents"
              value={analytics.incidents}
              icon={<AlertCircle className="h-6 w-6 text-red-600" />}
            />
          </div>
        )}

        {/* Configuration */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Configuration</h2>
          </div>
          <div className="px-6 py-4 grid grid-cols-2 gap-4 dark:bg-gray-800">
            <ConfigItem label="Method" value={monitor.method} />
            <ConfigItem label="Interval" value={`${monitor.interval}s`} />
            <ConfigItem label="Timeout" value={`${monitor.timeout}s`} />
            <ConfigItem label="Expected Status" value={monitor.expected_status} />
          </div>
        </div>

        {/* Alert Channels */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-gray-500 dark:text-gray-400" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Alert Channels</h2>
            </div>
            <span className="text-sm text-gray-500 dark:text-gray-400">{linkedChannels.length} connected</span>
          </div>
          <div className="px-6 py-4 space-y-3">
            {/* 연결된 채널 */}
            {linkedChannels.length === 0 ? (
              <p className="text-sm text-gray-500 dark:text-gray-400">No alert channels connected yet.</p>
            ) : (
              linkedChannels.map((ch: any) => (
                <div key={ch.id} className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Bell className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">{ch.type}</span>
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {ch.config?.email || ch.config?.webhook_url || ''}
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => handleTestChannel(ch.id)}
                      className="px-2 py-1 text-xs border border-gray-200 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition text-gray-600 dark:text-gray-400"
                    >
                      Test
                    </button>
                    <button
                      onClick={() => handleUnlinkChannel(ch.id)}
                      className="p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded transition text-red-500"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
            {/* 연결 가능한 채널 */}
            {allChannels.filter(ch => !linkedChannels.find((l: any) => l.id === ch.id)).length > 0 && (
              <div className="pt-2">
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Add channel:</p>
                <div className="flex flex-wrap gap-2">
                  {allChannels
                    .filter(ch => !linkedChannels.find((l: any) => l.id === ch.id))
                    .map((ch: any) => (
                      <button
                        key={ch.id}
                        onClick={() => handleLinkChannel(ch.id)}
                        className="flex items-center gap-1 px-3 py-1.5 border border-gray-200 dark:border-gray-600 rounded-lg text-sm hover:border-green-500 transition text-gray-700 dark:text-gray-300"
                      >
                        <Plus className="h-3 w-3" />
                        {ch.type} {ch.config?.email ? `(${ch.config.email})` : ''}
                      </button>
                    ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Assertions */}
        <AssertionsPanel monitorId={monitorId} />

        {/* Regex Live Tester */}
        <RegexTestPanel
          initialPattern={monitor.keyword || ''}
          initialPresent={monitor.keyword_present ?? true}
        />

        {/* Recent Checks */}
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

new_sections = """        {/* Tabs */}
        <div className="flex gap-1 border-b border-gray-200 dark:border-gray-700">
          {[
            { key: 'overview', label: 'Overview' },
            { key: 'assertions', label: 'Assertions' },
            { key: 'alerts', label: `Alerts${linkedChannels.length > 0 ? ` (${linkedChannels.length})` : ''}` },
            { key: 'history', label: `History (${checksTotal})` },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`px-4 py-2.5 text-sm font-medium border-b-2 transition -mb-px ${
                activeTab === tab.key
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* ── OVERVIEW TAB ── */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {analytics && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <StatCard
                  title="Uptime (7 days)"
                  value={`${analytics.uptime_percentage}%`}
                  icon={<CheckCircle className="h-6 w-6 text-green-600" />}
                />
                <StatCard
                  title="Avg Response Time"
                  value={`${analytics.avg_response_time}ms`}
                  icon={<Clock className="h-6 w-6 text-blue-600" />}
                />
                <StatCard
                  title="Total Checks"
                  value={analytics.total_checks}
                  icon={<Activity className="h-6 w-6 text-purple-600" />}
                />
                <StatCard
                  title="Incidents"
                  value={analytics.incidents}
                  icon={<AlertCircle className="h-6 w-6 text-red-600" />}
                />
              </div>
            )}

            {/* Response Time Percentiles */}
            {percentiles && percentiles.sample_size > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Response Time Percentiles</h2>
                  <span className="text-xs text-gray-500 dark:text-gray-400">Last 24h · {percentiles.sample_size} samples</span>
                </div>
                <div className="px-6 py-4 grid grid-cols-3 gap-4">
                  {[
                    { label: 'p50 (Median)', value: percentiles.p50, color: 'text-green-600 dark:text-green-400' },
                    { label: 'p95', value: percentiles.p95, color: 'text-yellow-600 dark:text-yellow-400' },
                    { label: 'p99', value: percentiles.p99, color: 'text-red-500 dark:text-red-400' },
                  ].map((p) => (
                    <div key={p.label} className="text-center p-4 bg-gray-50 dark:bg-gray-900 rounded-xl">
                      <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{p.label}</p>
                      <p className={`text-2xl font-bold ${p.color}`}>{p.value}<span className="text-sm font-normal text-gray-400 ml-1">ms</span></p>
                    </div>
                  ))}
                </div>
                <div className="px-6 pb-4 flex gap-6 text-xs text-gray-500 dark:text-gray-400">
                  <span>Min: <strong className="text-gray-700 dark:text-gray-300">{percentiles.min}ms</strong></span>
                  <span>Avg: <strong className="text-gray-700 dark:text-gray-300">{percentiles.avg}ms</strong></span>
                  <span>Max: <strong className="text-gray-700 dark:text-gray-300">{percentiles.max}ms</strong></span>
                </div>
              </div>
            )}

            {/* Configuration */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Configuration</h2>
              </div>
              <div className="px-6 py-4 grid grid-cols-2 gap-4 dark:bg-gray-800">
                <ConfigItem label="Method" value={monitor.method} />
                <ConfigItem label="Interval" value={`${monitor.interval}s`} />
                <ConfigItem label="Timeout" value={`${monitor.timeout}s`} />
                <ConfigItem label="Expected Status" value={monitor.expected_status} />
              </div>
            </div>
          </div>
        )}

        {/* ── ASSERTIONS TAB ── */}
        {activeTab === 'assertions' && (
          <div className="space-y-6">
            <AssertionsPanel monitorId={monitorId} />
            <RegexTestPanel
              initialPattern={monitor.keyword || ''}
              initialPresent={monitor.keyword_present ?? true}
            />
          </div>
        )}

        {/* ── ALERTS TAB ── */}
        {activeTab === 'alerts' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-gray-500 dark:text-gray-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Alert Channels</h2>
              </div>
              <span className="text-sm text-gray-500 dark:text-gray-400">{linkedChannels.length} connected</span>
            </div>
            <div className="px-6 py-4 space-y-3">
              {linkedChannels.length === 0 ? (
                <p className="text-sm text-gray-500 dark:text-gray-400">No alert channels connected yet.</p>
              ) : (
                linkedChannels.map((ch: any) => (
                  <div key={ch.id} className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
                    <div className="flex items-center gap-2">
                      <Bell className="h-4 w-4 text-green-600 dark:text-green-400" />
                      <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">{ch.type}</span>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        {ch.config?.email || ch.config?.webhook_url || ''}
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => handleTestChannel(ch.id)}
                        className="px-2 py-1 text-xs border border-gray-200 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition text-gray-600 dark:text-gray-400"
                      >
                        Test
                      </button>
                      <button
                        onClick={() => handleUnlinkChannel(ch.id)}
                        className="p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded transition text-red-500"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))
              )}
              {allChannels.filter(ch => !linkedChannels.find((l: any) => l.id === ch.id)).length > 0 && (
                <div className="pt-2">
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Add channel:</p>
                  <div className="flex flex-wrap gap-2">
                    {allChannels
                      .filter(ch => !linkedChannels.find((l: any) => l.id === ch.id))
                      .map((ch: any) => (
                        <button
                          key={ch.id}
                          onClick={() => handleLinkChannel(ch.id)}
                          className="flex items-center gap-1 px-3 py-1.5 border border-gray-200 dark:border-gray-600 rounded-lg text-sm hover:border-green-500 transition text-gray-700 dark:text-gray-300"
                        >
                          <Plus className="h-3 w-3" />
                          {ch.type} {ch.config?.email ? `(${ch.config.email})` : ''}
                        </button>
                      ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── HISTORY TAB ── */}
        {activeTab === 'history' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Check History</h2>
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
          </div>
        )}"""

# percentiles 섹션 중복 제거 (기존에 있으면)
old_percentiles = """        {/* Response Time Percentiles */}
        {percentiles && percentiles.sample_size > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Response Time Percentiles</h2>
              <span className="text-xs text-gray-500 dark:text-gray-400">Last 24h · {percentiles.sample_size} samples</span>
            </div>
            <div className="px-6 py-4 grid grid-cols-3 gap-4">
              {[
                { label: 'p50 (Median)', value: percentiles.p50, color: 'text-green-600 dark:text-green-400' },
                { label: 'p95', value: percentiles.p95, color: 'text-yellow-600 dark:text-yellow-400' },
                { label: 'p99', value: percentiles.p99, color: 'text-red-500 dark:text-red-400' },
              ].map((p) => (
                <div key={p.label} className="text-center p-4 bg-gray-50 dark:bg-gray-900 rounded-xl">
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{p.label}</p>
                  <p className={`text-2xl font-bold ${p.color}`}>{p.value}<span className="text-sm font-normal text-gray-400 ml-1">ms</span></p>
                </div>
              ))}
            </div>
            <div className="px-6 pb-4 flex gap-6 text-xs text-gray-500 dark:text-gray-400">
              <span>Min: <strong className="text-gray-700 dark:text-gray-300">{percentiles.min}ms</strong></span>
              <span>Avg: <strong className="text-gray-700 dark:text-gray-300">{percentiles.avg}ms</strong></span>
              <span>Max: <strong className="text-gray-700 dark:text-gray-300">{percentiles.max}ms</strong></span>
            </div>
          </div>
        )}

        {/* Configuration */}"""

if old_percentiles in c:
    c = c.replace(old_percentiles, "        {/* Configuration */}")

c = c.replace(old_sections, new_sections)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
print("Tabs:", "activeTab" in c)
print("Overview tab:", "OVERVIEW TAB" in c)
print("Assertions tab:", "ASSERTIONS TAB" in c)
print("Alerts tab:", "ALERTS TAB" in c)
print("History tab:", "HISTORY TAB" in c)
