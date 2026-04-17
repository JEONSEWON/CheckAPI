file_path = "frontend/app/dashboard/monitors/[id]/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# 1. alertChannelsAPI import 추가
old_import = "import { monitorsAPI, analyticsAPI } from '@/lib/api';"
new_import = "import { monitorsAPI, analyticsAPI, alertChannelsAPI } from '@/lib/api';"
content = content.replace(old_import, new_import)

# 2. Bell icon import 추가
old_icons = "import {\n  ArrowLeft,\n  CheckCircle,\n  AlertCircle,\n  Clock,\n  Activity,\n  Trash2,\n  Edit,\n  Pause,\n  Play\n} from 'lucide-react';"
new_icons = "import {\n  ArrowLeft,\n  CheckCircle,\n  AlertCircle,\n  Clock,\n  Activity,\n  Trash2,\n  Edit,\n  Pause,\n  Play,\n  Bell,\n  Plus,\n  X\n} from 'lucide-react';"
content = content.replace(old_icons, new_icons)

# 3. state 추가
old_state = "  const [loading, setLoading] = useState(true);"
new_state = "  const [loading, setLoading] = useState(true);\n  const [allChannels, setAllChannels] = useState<any[]>([]);\n  const [linkedChannels, setLinkedChannels] = useState<any[]>([]);"
content = content.replace(old_state, new_state)

# 4. loadData에 채널 로드 추가
old_load = "      // Get recent checks\n      const checksResponse = await monitorsAPI.checks(monitorId, {"
new_load = """      // Get alert channels
      const [allCh, monitorData] = await Promise.all([
        alertChannelsAPI.list(),
        monitorsAPI.get(monitorId),
      ]);
      setAllChannels(allCh);
      setLinkedChannels(monitorData.alert_channels || []);

      // Get recent checks
      const checksResponse = await monitorsAPI.checks(monitorId, {"""
content = content.replace(old_load, new_load)

# 5. link/unlink 핸들러 추가
old_handler = "  const handleDelete = async () => {"
new_handler = """  const handleLinkChannel = async (channelId: string) => {
    try {
      await alertChannelsAPI.linkToMonitor(monitorId, channelId);
      toast.success('Alert channel linked!');
      loadData();
    } catch (error) {
      toast.error('Failed to link channel');
    }
  };

  const handleUnlinkChannel = async (channelId: string) => {
    try {
      await alertChannelsAPI.unlinkFromMonitor(monitorId, channelId);
      toast.success('Alert channel unlinked');
      loadData();
    } catch (error) {
      toast.error('Failed to unlink channel');
    }
  };

  const handleDelete = async () => {"""
content = content.replace(old_handler, new_handler)

# 6. Alert Channels 섹션 추가 (Configuration 섹션 다음에)
old_section = "        {/* Recent Checks */}"
new_section = """        {/* Alert Channels */}
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
                  <button
                    onClick={() => handleUnlinkChannel(ch.id)}
                    className="p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded transition text-red-500"
                  >
                    <X className="h-4 w-4" />
                  </button>
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

        {/* Recent Checks */}"""
content = content.replace(old_section, new_section)

if len(content) >= original_length:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ 완료! ({len(content) - original_length}자 추가)")
else:
    print("❌ 파일 잘림 감지 — 저장 안 함")
