file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. billing state 추가
old_state = "  const [loading, setLoading] = useState(true);"
new_state = "  const [loading, setLoading] = useState(true);\n  const [billing, setBilling] = useState<'monthly' | 'annual'>('monthly');"
content = content.replace(old_state, new_state)

# 2. handleUpgrade에 billing 파라미터 추가
old_upgrade = """  const handleUpgrade = async (plan: string) => {
    try {
      const response = await subscriptionAPI.checkout(plan);
      window.location.href = response.checkout_url;
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create checkout');
    }
  };"""

new_upgrade = """  const handleUpgrade = async (plan: string) => {
    try {
      const response = await subscriptionAPI.checkout(plan, billing);
      window.location.href = response.checkout_url;
    } catch (error: any) {
      toast.error(error.message || 'Failed to create checkout');
    }
  };"""

content = content.replace(old_upgrade, new_upgrade)

# 3. Upgrade Your Plan 헤딩 아래에 토글 추가
old_heading = '          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Upgrade Your Plan</h2>\n          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">'
new_heading = '''          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Upgrade Your Plan</h2>
            <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
              <button
                onClick={() => setBilling('monthly')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${billing === 'monthly' ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 dark:text-gray-400'}`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBilling('annual')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${billing === 'annual' ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 dark:text-gray-400'}`}
              >
                Annual
                <span className="ml-1.5 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-1.5 py-0.5 rounded-full">-20%</span>
              </button>
            </div>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">'''

content = content.replace(old_heading, new_heading)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("✅ settings page 완료!")
