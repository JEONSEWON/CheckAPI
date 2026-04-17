file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 'use client' 또는 LandingBillingToggle 필요 - page.tsx가 Server Component이므로
# PricingSection을 별도 client component로 분리하는 대신
# billing 상태를 PricingCTA에서 자체적으로 관리하도록 처리

# 가격 데이터에 연간 가격 추가
old_plans = """{ name: 'Free', price: '$0', period: '/month', badge: null, features: ['10 monitors','5-minute checks','All alert channels','Public status page','30-day history','Commercial use allowed'], cta: 'Start Free', ctaHref: '/register', highlight: false },
            { name: 'Starter', price: '$5', period: '/month', badge: 'POPULAR', features: ['20 monitors','1-minute checks','All alert channels','Analytics','30-day history','Commercial use allowed'], cta: 'Get Started', ctaHref: '/register', highlight: true },
            { name: 'Pro', price: '$15', period: '/month', badge: 'Best for growing startups', features: ['100 monitors','30-second checks','Team sharing','Priority support','90-day history','Commercial use allowed'], cta: 'Get Started', ctaHref: '/register', highlight: false },
            { name: 'Business', price: '$49', period: '/month', badge: null, features: ['Unlimited monitors','10-second checks','API access','Custom features','SLA','1-year history'], cta: 'Get Started', ctaHref: '/register', highlight: false },"""

new_plans = """{ name: 'Free', price: '$0', annualPrice: '$0', annualMonthly: '$0', period: '/month', badge: null, features: ['10 monitors','5-minute checks','All alert channels','Public status page','30-day history','Commercial use allowed'], cta: 'Start Free', ctaHref: '/register', highlight: false },
            { name: 'Starter', price: '$5', annualPrice: '$48', annualMonthly: '$4', period: '/month', badge: 'POPULAR', features: ['20 monitors','1-minute checks','All alert channels','Analytics','30-day history','Commercial use allowed'], cta: 'Get Started', ctaHref: '/register', highlight: true },
            { name: 'Pro', price: '$15', annualPrice: '$144', annualMonthly: '$12', period: '/month', badge: 'Best for growing startups', features: ['100 monitors','30-second checks','Team sharing','Priority support','90-day history','Commercial use allowed'], cta: 'Get Started', ctaHref: '/register', highlight: false },
            { name: 'Business', price: '$49', annualPrice: '$470', annualMonthly: '$39', period: '/month', badge: null, features: ['Unlimited monitors','10-second checks','API access','Custom features','SLA','1-year history'], cta: 'Get Started', ctaHref: '/register', highlight: false },"""

if old_plans in content:
    content = content.replace(old_plans, new_plans)
    print("✅ 가격 데이터 업데이트 완료!")
else:
    print("❌ 가격 데이터 못 찾음")

# 2. PricingCTA에 billing prop 전달 (현재는 plan.billing 없으니 'monthly' 기본값 유지)
# billing 토글은 PricingSection client component로 분리 필요
# 일단 PricingCTA 자체에서 토글 포함하도록

# 3. 가격 표시 부분 수정 - 현재 고정 price 표시를 PricingCTA로 통합
old_price = """<span className="text-3xl font-bold text-gray-900 dark:text-white">{plan.price}</span>
                <span className="text-gray-500 dark:text-gray-400">{plan.period}</span>"""

new_price = """<span className="text-3xl font-bold text-gray-900 dark:text-white">{plan.price}</span>
                <span className="text-gray-500 dark:text-gray-400">{plan.period}</span>
                {plan.annualPrice !== '$0' && (
                  <span className="ml-2 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full">or {plan.annualPrice}/yr</span>
                )}"""

if old_price in content:
    content = content.replace(old_price, new_price)
    print("✅ 가격 표시 업데이트 완료!")
else:
    print("❌ 가격 표시 못 찾음")

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("완료!")
