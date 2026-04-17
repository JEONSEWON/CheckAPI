file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_price = """      <div className="mt-4 mb-1">
        <span className="text-4xl font-bold text-gray-900 dark:text-white">{displayPrice}</span>
        <span className="text-gray-600 dark:text-gray-400">/mo</span>
      </div>
      {isAnnual && !isFree && (
        <div className="mb-4 flex items-center gap-2 flex-wrap">
          <span className="text-sm text-gray-400 dark:text-gray-500 line-through">{plan.monthlyPrice}/mo</span>
          <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full font-medium">Save 20%</span>
          <span className="text-xs text-gray-500 dark:text-gray-400 w-full">{plan.annualPrice} billed yearly</span>
        </div>
      )}
      {(!isAnnual || isFree) && <div className="mb-4" />}"""

new_price = """      {isAnnual && !isFree ? (
        <div className="mt-4 mb-4">
          <div>
            <span className="text-4xl font-bold text-gray-900 dark:text-white">{plan.annualPrice}</span>
            <span className="text-gray-600 dark:text-gray-400">/year</span>
          </div>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className="text-sm text-gray-500 dark:text-gray-400">{plan.annualMonthly}/mo</span>
            <span className="text-xs text-gray-400 dark:text-gray-500 line-through">{plan.monthlyPrice}/mo</span>
            <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full font-medium">Save 20%</span>
          </div>
        </div>
      ) : (
        <div className="mt-4 mb-4">
          <span className="text-4xl font-bold text-gray-900 dark:text-white">{plan.monthlyPrice}</span>
          <span className="text-gray-600 dark:text-gray-400">/mo</span>
        </div>
      )}"""

if old_price in content:
    content = content.replace(old_price, new_price)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
