FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

old_monitor_row = """function MonitorRow({ monitor }: any) {
  const router = useRouter();
  const statusColors = {
    up: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300',
    down: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300',
    degraded: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-300',
  };
  const statusIcons = {
    up: <CheckCircle className="h-4 w-4" />,
    down: <AlertCircle className="h-4 w-4" />,
    degraded: <AlertCircle className="h-4 w-4" />,
  };
  return (
    <div
      onClick={() => router.push(`/dashboard/monitors/${monitor.id}`)}
      className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition cursor-pointer"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-1">
            {monitor.name}
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400">{monitor.url}</p>
        </div>
        <div className="flex items-center space-x-4">
          {monitor.last_status && (
            <span className={`
              flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium
              ${statusColors[monitor.last_status as keyof typeof statusColors]}
            `}>
              {statusIcons[monitor.last_status as keyof typeof statusIcons]}
              <span className="capitalize">{monitor.last_status}</span>
            </span>
          )}
          <span className="text-xs text-gray-500 dark:text-gray-400">
            Every {monitor.interval}s
          </span>
        </div>
      </div>
    </div>
  );
}"""

new_monitor_row = """function MonitorRow({ monitor }: any) {
  const router = useRouter();
  const isHeartbeat = monitor.monitor_type === 'heartbeat';

  const statusColors = {
    up: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300',
    down: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300',
    degraded: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-300',
    pending: 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400',
  };
  const statusIcons = {
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
            <span className={`
              flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium
              ${statusColors[monitor.last_status as keyof typeof statusColors] || statusColors.pending}
            `}>
              {statusIcons[monitor.last_status as keyof typeof statusIcons] || statusIcons.pending}
              <span className="capitalize ml-1">{monitor.last_status}</span>
            </span>
          ) : (
            <span className="flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              <Clock className="h-4 w-4" />
              <span className="ml-1">No ping yet</span>
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
}"""

c = c.replace(old_monitor_row, new_monitor_row)

# Clock import 추가
if 'Clock' not in c:
    c = c.replace(
        "import { Activity, AlertCircle, CheckCircle, Clock }",
        "import { Activity, AlertCircle, CheckCircle, Clock }"
    )
    # 이미 있는지 확인
    if 'Clock' not in c:
        c = c.replace(
            "import { Activity, AlertCircle, CheckCircle,",
            "import { Activity, AlertCircle, CheckCircle, Clock,"
        )

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
print("Heartbeat badge:", "Heartbeat" in c)
print("pending status:", "pending" in c)
print("formatLastPing:", "formatLastPing" in c)
