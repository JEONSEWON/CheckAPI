file_path = "frontend/app/dashboard/settings/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = """  const plans = [
    { name: 'Free', price: '$0', features: ['10 monitors','5-minute checks','All alert channels','Public status page','Keyword validation','SSL monitoring','7-day history'] },
    { name: 'Starter', price: '$5', features: ['20 monitors','1-minute checks','All alert channels','Analytics','Keyword validation','SSL monitoring','30-day history'], popular: true },
    { name: 'Pro', price: '$15', features: ['100 monitors','30-second checks','All alert channels','Analytics','Team sharing (5 members)','Keyword validation','SSL monitoring','90-day history'] },
    { name: 'Business', price: '$49', features: ['Unlimited monitors','10-second checks','All alert channels','Analytics','Team sharing (unlimited)','Keyword validation','SSL monitoring','1-year history'] },
  ];"""

new = """  const plans = [
    {
      name: 'Free',
      monthlyPrice: '$0',
      annualPrice: '$0',
      annualMonthly: '$0',
      features: ['10 monitors','5-minute checks','All alert channels','Public status page','Keyword validation','SSL monitoring','30-day history'],
    },
    {
      name: 'Starter',
      monthlyPrice: '$5',
      annualPrice: '$48',
      annualMonthly: '$4',
      features: ['20 monitors','1-minute checks','All alert channels','Analytics','Keyword validation','SSL monitoring','30-day history'],
      popular: true,
    },
    {
      name: 'Pro',
      monthlyPrice: '$15',
      annualPrice: '$144',
      annualMonthly: '$12',
      features: ['100 monitors','30-second checks','All alert channels','Analytics','Team sharing (5 members)','Keyword validation','SSL monitoring','90-day history'],
    },
    {
      name: 'Business',
      monthlyPrice: '$49',
      annualPrice: '$470',
      annualMonthly: '$39',
      features: ['Unlimited monitors','10-second checks','All alert channels','Analytics','Team sharing (unlimited)','Keyword validation','SSL monitoring','1-year history'],
    },
  ];"""

if old in content:
    content = content.replace(old, new)
    print("✅ plans 수정 완료!")
else:
    print("❌ plans 못 찾음")

# PlanCard에 billing prop 추가 + 가격 표시 수정
old_plancard = """          {plans.map((plan) => (
              <PlanCard
                key={plan.name}
                plan={plan}
                currentPlan={user?.plan || 'free'}
                onUpgrade={handleUpgrade}
              />"""

new_plancard = """          {plans.map((plan) => (
              <PlanCard
                key={plan.name}
                plan={plan}
                currentPlan={user?.plan || 'free'}
                onUpgrade={handleUpgrade}
                billing={billing}
              />"""

if old_plancard in content:
    content = content.replace(old_plancard, new_plancard)
    print("✅ PlanCard props 수정 완료!")
else:
    print("❌ PlanCard props 못 찾음")

# PlanCard 컴포넌트 수정
old_component = """function PlanCard({ plan, currentPlan, onUpgrade }: any) {
  const isCurrent = plan.name.toLowerCase() === currentPlan;
  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border-2 p-6 ${plan.popular ? 'border-green-600 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>
      {plan.popular && (
        <span className="bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full">POPULAR</span>
      )}
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mt-4">{plan.name}</h3>
      <div className="mt-4 mb-6">
        <span className="text-4xl font-bold text-gray-900 dark:text-white">{plan.price}</span>
        <span className="text-gray-600 dark:text-gray-400">/month</span>
      </div>"""

new_component = """function PlanCard({ plan, currentPlan, onUpgrade, billing }: any) {
  const isCurrent = plan.name.toLowerCase() === currentPlan;
  const isAnnual = billing === 'annual';
  const displayPrice = isAnnual ? plan.annualMonthly : plan.monthlyPrice;
  const isFree = plan.name === 'Free';

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border-2 p-6 ${plan.popular ? 'border-green-600 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>
      {plan.popular && (
        <span className="bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full">POPULAR</span>
      )}
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mt-4">{plan.name}</h3>
      <div className="mt-4 mb-1">
        <span className="text-4xl font-bold text-gray-900 dark:text-white">{displayPrice}</span>
        <span className="text-gray-600 dark:text-gray-400">/month</span>
      </div>
      {isAnnual && !isFree && (
        <div className="mb-4 flex items-center gap-2">
          <span className="text-sm text-gray-400 line-through">{plan.monthlyPrice}/mo</span>
          <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full font-medium">Save 20%</span>
          <span className="text-xs text-gray-500 dark:text-gray-400">({plan.annualPrice}/yr)</span>
        </div>
      )}"""

if old_component in content:
    content = content.replace(old_component, new_component)
    print("✅ PlanCard 컴포넌트 수정 완료!")
else:
    print("❌ PlanCard 컴포넌트 못 찾음")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n완료!")
