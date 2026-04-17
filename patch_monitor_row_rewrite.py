FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# MonitorRow 시작/끝 라인 찾기
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if 'function MonitorRow({ monitor }: any)' in line:
        start_idx = i
    if start_idx is not None and i > start_idx and line.strip() == '}' and end_idx is None:
        # 마지막 닫는 중괄호 찾기 - 중첩 카운트
        pass

# 중첩 카운트로 끝 찾기
if start_idx is not None:
    depth = 0
    for i in range(start_idx, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth == 0 and i > start_idx:
            end_idx = i
            break

print(f"MonitorRow: lines {start_idx+1} to {end_idx+1}")

new_monitor_row = """function MonitorRow({ monitor }: any) {
  const router = useRouter();
  const isHeartbeat = monitor.monitor_type === 'heartbeat';

  const statusColors: any = {
    up: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300',
    down: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300',
    degraded: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-300',
    pending: 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400',
  };
  const statusIcons: any = {
    up: <CheckCircle className="h-4 w-4" />,
    down: <AlertCircle className="h-4 w-4" />,
    degraded: <AlertCircle className="h-4 w-4" />,
    pending: <Clock className="h-4 w-4" />,
  };

  const formatLastPing = (lastPingAt: string | null) => {
    if (!lastPingAt) return 'No ping yet';
    const diff = Math.floor((Date.now() - new Date(lastPingAt + 'Z').getTime()) / 1000 / 60);
    if (diff < 1) return 'Just now';
    if (diff < 60) return `${diff}m ago`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`;
    return `${Math.floor(diff / 1440)}d ago`;
  };

  return (
    <div
      onClick={() => router.push(`/dashboard/monitors/${monitor.id}`)}
      className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition cursor-pointer"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white">
              {monitor.name}
            </h3>
            {isHeartbeat && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400 text-xs font-medium rounded-full">
                💓 Heartbeat
              </span>
            )}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {isHeartbeat
              ? `Last ping: ${formatLastPing(monitor.last_ping_at)} · Every ${monitor.heartbeat_interval ?? '?'}m`
              : monitor.url
            }
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {monitor.last_status ? (
            <span className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${statusColors[monitor.last_status] || statusColors.pending}`}>
              {statusIcons[monitor.last_status] || statusIcons.pending}
              <span className="capitalize ml-1">{monitor.last_status}</span>
            </span>
          ) : (
            <span className="flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              <Clock className="h-4 w-4" />
              <span>No ping yet</span>
            </span>
          )}
          {!isHeartbeat && (
            <span className="text-xs text-gray-500 dark:text-gray-400">
              Every {monitor.interval}s
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
"""

# 교체
lines[start_idx:end_idx+1] = [new_monitor_row]

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

content = ''.join(lines)

# Clock import 확인 및 추가
if 'Clock' not in content.split('import')[1].split('from')[0] if 'lucide-react' in content else True:
    print("Clock import check needed")

print("Done!")
print("Heartbeat badge:", "Heartbeat" in content)
print("pending status:", "pending" in content)
print("formatLastPing:", "formatLastPing" in content)
