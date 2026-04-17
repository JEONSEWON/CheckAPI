file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# PlanCard props에 billing 추가
old_card = "PlanCard key={plan.name} plan={plan} currentPlan={user?.plan || 'free'} onUpgrade={handleUpgrade} />"
new_card = "PlanCard key={plan.name} plan={plan} currentPlan={user?.plan || 'free'} onUpgrade={handleUpgrade} billing={billing} />"

if old_card in content:
    content = content.replace(old_card, new_card)
    print("✅ PlanCard props 완료!")
else:
    print("❌ PlanCard props 못 찾음")

# PlanCard 컴포넌트 찾기
idx = content.find('function PlanCard(')
end = content.find('\nfunction InfoRow(', idx)
old_component = content[idx:end]
print("현재 PlanCard:")
print(old_component[:300])

new_component = """function PlanCard({ plan, currentPlan, onUpgrade, billing }: any) {
  const isCurrent = plan.name.toLowerCase() === currentPlan;
  const isAnnual = billing === 'annual';
  const isFree = plan.name === 'Free';
  const displayPrice = isAnnual && !isFree ? plan.annualMonthly : plan.monthlyPrice;

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border-2 p-6 ${plan.popular ? 'border-green-600 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>
      {plan.popular && (
        <span className="bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full">POPULAR</span>
      )}
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mt-4">{plan.name}</h3>
      <div className="mt-4 mb-1">
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
      {(!isAnnual || isFree) && <div className="mb-4" />}
      <ul className="space-y-3 mb-6">
        {plan.features.map((feature: string, i: number) => (
          <li key={i} className="flex items-center text-gray-700 dark:text-gray-300">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2 flex-shrink-0" />
            {feature}
          </li>
        ))}
      </ul>
      {isCurrent ? (
        <button disabled className="w-full py-2 border-2 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 rounded-lg font-medium">
          Current Plan
        </button>
      ) : (
        <button
          onClick={() => onUpgrade(plan.name.toLowerCase())}
          className={`w-full py-2 rounded-lg font-medium transition ${plan.popular ? 'bg-green-600 text-white hover:bg-green-700' : 'border-2 border-green-600 text-green-600 hover:bg-green-50 dark:hover:bg-green-900'}`}
        >
          {currentPlan === 'free' ? 'Upgrade' : 'Switch Plan'}
        </button>
      )}
    </div>
  );
}

"""

content = content[:idx] + new_component + content[end:]

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("✅ PlanCard 컴포넌트 완료!")
