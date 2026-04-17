file_path = "frontend/app/dashboard/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. alertChannelsAPI import 추가
old_import = "import { authAPI, monitorsAPI, analyticsAPI } from '@/lib/api';"
new_import = "import { authAPI, monitorsAPI, analyticsAPI, alertChannelsAPI } from '@/lib/api';"
content = content.replace(old_import, new_import)

# 2. alertChannels state 추가
old_state = "  const [isModalOpen, setIsModalOpen] = useState(false);"
new_state = "  const [isModalOpen, setIsModalOpen] = useState(false);\n  const [alertChannels, setAlertChannels] = useState<any[]>([]);"
content = content.replace(old_state, new_state)

# 3. loadData에 alertChannels 로드 추가
old_load = "      // Get analytics overview\n      const overviewResponse = await analyticsAPI.overview();\n      setOverview(overviewResponse);"
new_load = "      // Get analytics overview\n      const overviewResponse = await analyticsAPI.overview();\n      setOverview(overviewResponse);\n\n      // Get alert channels for onboarding progress\n      try {\n        const channelsResponse = await alertChannelsAPI.list();\n        setAlertChannels(channelsResponse);\n      } catch {\n        // ignore\n      }"
content = content.replace(old_load, new_load)

# 4. 온보딩 배너 조건 수정 - alertChannels.length >= 1 이면 배너 숨김
old_banner = "              {monitors.length <= 2 && ("
new_banner = "              {monitors.length <= 2 && alertChannels.length === 0 && ("
content = content.replace(old_banner, new_banner)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("✅ 완료!")
