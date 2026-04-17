FILE = r"C:\home\jeon\api-health-monitor\frontend\app\dashboard\monitors\[id]\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. handleCopyStatusUrl 앞에 handleTestChannel 추가
old_fn = "  const handleCopyStatusUrl = () => {"
new_fn = """  const handleTestChannel = async (channelId: string) => {
    try {
      await alertChannelsAPI.test(channelId);
      toast.success('Test alert sent!');
    } catch (error) {
      toast.error('Failed to send test alert');
    }
  };

  const handleCopyStatusUrl = () => {"""
content = content.replace(old_fn, new_fn)

# 2. 연결된 채널 X 버튼 옆에 Test 버튼 추가
old_unlink_btn = """                  <button
                    onClick={() => handleUnlinkChannel(ch.id)}
                    className="p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded transition text-red-500"
                  >
                    <X className="h-4 w-4" />
                  </button>"""
new_unlink_btn = """                  <div className="flex items-center gap-1">
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
                  </div>"""
content = content.replace(old_unlink_btn, new_unlink_btn)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("handleTestChannel:", "handleTestChannel" in content)
print("Test button:", ">Test<" in content.replace(" ", "").replace("\n", ""))
