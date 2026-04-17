file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_length = len(content)

# 1. API import 추가
old_import = "import { subscriptionAPI } from '@/lib/api';"
new_import = "import { subscriptionAPI } from '@/lib/api';\nimport { getAccessToken } from '@/lib/api';"
content = content.replace(old_import, new_import)

# 2. state 추가
old_state = "  const [loading, setLoading] = useState(true);\n  const [billing, setBilling] = useState<'monthly' | 'annual'>('monthly');"
new_state = "  const [loading, setLoading] = useState(true);\n  const [billing, setBilling] = useState<'monthly' | 'annual'>('monthly');\n  const [apiKeys, setApiKeys] = useState<any[]>([]);\n  const [newKeyName, setNewKeyName] = useState('');\n  const [createdKey, setCreatedKey] = useState<string | null>(null);\n  const [apiKeyLoading, setApiKeyLoading] = useState(false);"
content = content.replace(old_state, new_state)

# 3. API Keys 핸들러 추가
old_handler = "  const handleCancel = async () => {"
new_handler = """  const loadApiKeys = async () => {
    try {
      const token = getAccessToken();
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app'}/api/v1/api-keys/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) setApiKeys(await res.json());
    } catch {}
  };

  const handleCreateApiKey = async () => {
    if (!newKeyName.trim()) return;
    setApiKeyLoading(true);
    try {
      const token = getAccessToken();
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app'}/api/v1/api-keys/?name=${encodeURIComponent(newKeyName)}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (res.ok) {
        setCreatedKey(data.key);
        setNewKeyName('');
        loadApiKeys();
        toast.success('API key created!');
      } else {
        toast.error(data.detail || 'Failed to create key');
      }
    } catch {
      toast.error('Failed to create key');
    } finally {
      setApiKeyLoading(false);
    }
  };

  const handleDeleteApiKey = async (keyId: string) => {
    if (!confirm('Delete this API key? This cannot be undone.')) return;
    try {
      const token = getAccessToken();
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://api-health-monitor-production.up.railway.app'}/api/v1/api-keys/${keyId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      loadApiKeys();
      toast.success('API key deleted');
    } catch {
      toast.error('Failed to delete key');
    }
  };

  const handleCancel = async () => {"""
content = content.replace(old_handler, new_handler)

# 4. useEffect에 loadApiKeys 추가
old_effect = "  useEffect(() => {\n    loadSubscription();\n  }, []);"
new_effect = "  useEffect(() => {\n    loadSubscription();\n    if (user?.plan === 'business') loadApiKeys();\n  }, [user?.plan]);"
content = content.replace(old_effect, new_effect)

# 5. API Keys 섹션 추가 (Account Info 섹션 다음에)
old_end = "      </div>\n    </DashboardLayout>"
new_end = """      </div>

        {/* API Access - Business Plan */}
        {user?.plan === 'business' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">API Access</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Use API keys to access your monitor data programmatically.</p>

            {/* 생성된 키 표시 */}
            {createdKey && (
              <div className="mb-4 p-4 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
                <p className="text-sm font-semibold text-green-700 dark:text-green-400 mb-2">⚠️ Save this key — it won't be shown again!</p>
                <div className="flex items-center gap-2">
                  <code className="flex-1 text-xs bg-white dark:bg-gray-900 px-3 py-2 rounded border border-green-200 dark:border-green-700 text-gray-900 dark:text-white font-mono break-all">{createdKey}</code>
                  <button
                    onClick={() => { navigator.clipboard.writeText(createdKey); toast.success('Copied!'); }}
                    className="px-3 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition"
                  >
                    Copy
                  </button>
                </div>
                <button onClick={() => setCreatedKey(null)} className="mt-2 text-xs text-gray-500 hover:text-gray-700">Dismiss</button>
              </div>
            )}

            {/* 기존 키 목록 */}
            {apiKeys.length > 0 && (
              <div className="mb-4 space-y-2">
                {apiKeys.map((key: any) => (
                  <div key={key.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">{key.name}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{key.key_prefix}... · Created {new Date(key.created_at).toLocaleDateString()}</p>
                    </div>
                    <button
                      onClick={() => handleDeleteApiKey(key.id)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* 새 키 생성 */}
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Key name (e.g. Production)"
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm text-gray-900 dark:text-white bg-white dark:bg-gray-700"
              />
              <button
                onClick={handleCreateApiKey}
                disabled={apiKeyLoading || !newKeyName.trim()}
                className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition disabled:opacity-50"
              >
                {apiKeyLoading ? 'Creating...' : 'Create Key'}
              </button>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>"""

content = content.replace(old_end, new_end)

if len(content) >= original_length:
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ settings.tsx 완료! ({len(content) - original_length}자 추가)")
else:
    print("❌ 파일 잘림 감지 — 저장 안 함")
