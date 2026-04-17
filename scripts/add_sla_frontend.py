file_path = "frontend/app/dashboard/analytics/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# 1. analyticsAPI import에 sla 추가
old_import = "import { analyticsAPI } from '@/lib/api';"
new_import = "import { analyticsAPI } from '@/lib/api';\nimport { useAuthStore } from '@/lib/store';"
content = content.replace(old_import, new_import)

# 2. state 추가
old_state = "  const [loading, setLoading] = useState(true);"
new_state = "  const [loading, setLoading] = useState(true);\n  const [slaReport, setSlaReport] = useState<any>(null);\n  const [slaMonths, setSlaMonths] = useState(3);\n  const user = useAuthStore((state) => state.user);"
content = content.replace(old_state, new_state)

# 3. loadData에 SLA 로드 추가
old_load = "    } catch (error) {\n      toast.error('Failed to load analytics');\n    } finally {\n      setLoading(false);\n    }"
new_load = """    } catch (error) {
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const loadSLA = async (months: number) => {
    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app';
      const res = await fetch(`${API_URL}/api/v1/analytics/sla?months=${months}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) setSlaReport(await res.json());
    } catch {}"""
content = content.replace(old_load, new_load)

# 4. useEffect에 SLA 로드 추가
old_effect = "  useEffect(() => {\n    loadData();\n  }, []);"
new_effect = "  useEffect(() => {\n    loadData();\n  }, []);\n\n  useEffect(() => {\n    if (user?.plan === 'pro' || user?.plan === 'business') loadSLA(slaMonths);\n  }, [user?.plan, slaMonths]);"
content = content.replace(old_effect, new_effect)

# 5. SLA 섹션을 인시던트 섹션 앞에 추가
old_incident = "      {/* Incidents */}"
new_incident = """      {/* SLA Report */}
      {(user?.plan === 'pro' || user?.plan === 'business') && slaReport && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">SLA Report</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Monthly uptime & performance summary</p>
            </div>
            <select
              value={slaMonths}
              onChange={(e) => setSlaMonths(Number(e.target.value))}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm text-gray-900 dark:text-white bg-white dark:bg-gray-700"
            >
              <option value={1}>Last 1 month</option>
              <option value={3}>Last 3 months</option>
              <option value={6}>Last 6 months</option>
              <option value={12}>Last 12 months</option>
            </select>
          </div>

          {slaReport.monitors.map((monitor: any) => (
            <div key={monitor.monitor_id} className="mb-6 last:mb-0">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">{monitor.monitor_name}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{monitor.monitor_url}</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {monitor.overall_uptime != null ? `${monitor.overall_uptime}%` : 'N/A'}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Overall uptime</p>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">
                      <th className="pb-2 pr-4">Month</th>
                      <th className="pb-2 pr-4">Uptime</th>
                      <th className="pb-2 pr-4">Downtime</th>
                      <th className="pb-2 pr-4">Incidents</th>
                      <th className="pb-2">Avg Response</th>
                    </tr>
                  </thead>
                  <tbody>
                    {monitor.monthly.map((m: any) => (
                      <tr key={m.month} className="border-b border-gray-100 dark:border-gray-700 last:border-0">
                        <td className="py-2 pr-4 text-gray-900 dark:text-white font-medium">{m.month}</td>
                        <td className="py-2 pr-4">
                          <span className={`font-semibold ${m.uptime_percentage == null ? 'text-gray-400' : m.uptime_percentage >= 99.9 ? 'text-green-600 dark:text-green-400' : m.uptime_percentage >= 99 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'}`}>
                            {m.uptime_percentage != null ? `${m.uptime_percentage}%` : 'No data'}
                          </span>
                        </td>
                        <td className="py-2 pr-4 text-gray-600 dark:text-gray-400">{m.downtime_minutes}m</td>
                        <td className="py-2 pr-4 text-gray-600 dark:text-gray-400">{m.incidents}</td>
                        <td className="py-2 text-gray-600 dark:text-gray-400">{m.avg_response_time}ms</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Incidents */}"""

content = content.replace(old_incident, new_incident)

if len(content) >= original_length:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ analytics page SLA 섹션 추가 완료!")
else:
    print("❌ 파일 잘림")
