import os

# ── 1. PricingSection 컴포넌트 생성 ─────────────────────────────────────────
COMP_FILE = r"C:\home\jeon\api-health-monitor\frontend\components\PricingSection.tsx"

component = r"""'use client';

import { useState } from 'react';
import { CheckCircle } from 'lucide-react';
import PricingCTA from '@/components/PricingCTA';

const plans = [
  {
    name: 'Free', price: '$0', annualPrice: '$0', annualMonthly: '$0',
    badge: null, highlight: false, ctaHref: '/register', cta: 'Start Free',
    features: ['10 monitors','5-minute checks','All alert channels','Public status page','30-day history','Commercial use allowed'],
  },
  {
    name: 'Starter', price: '$5', annualPrice: '$48', annualMonthly: '$4',
    badge: 'POPULAR', highlight: true, ctaHref: '/register', cta: 'Get Started',
    features: ['20 monitors','1-minute checks','All alert channels','Analytics','30-day history','Commercial use allowed'],
  },
  {
    name: 'Pro', price: '$15', annualPrice: '$144', annualMonthly: '$12',
    badge: 'Best for growing startups', highlight: false, ctaHref: '/register', cta: 'Get Started',
    features: ['100 monitors','30-second checks','Team sharing','Priority support','90-day history','Commercial use allowed'],
  },
  {
    name: 'Business', price: '$49', annualPrice: '$470', annualMonthly: '$39',
    badge: null, highlight: false, ctaHref: '/register', cta: 'Get Started',
    features: ['Unlimited monitors','10-second checks','REST API access (API keys)','Custom features','SLA','1-year history'],
  },
];

export default function PricingSection() {
  const [isAnnual, setIsAnnual] = useState(false);

  return (
    <section id="pricing" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-10">
        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">Simple, transparent pricing</h2>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">Start free, upgrade when you grow</p>

        {/* Toggle */}
        <div className="inline-flex items-center gap-3 bg-gray-100 dark:bg-gray-800 rounded-full p-1">
          <button
            onClick={() => setIsAnnual(false)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition ${!isAnnual ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow' : 'text-gray-500 dark:text-gray-400'}`}
          >
            Monthly
          </button>
          <button
            onClick={() => setIsAnnual(true)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition flex items-center gap-1.5 ${isAnnual ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow' : 'text-gray-500 dark:text-gray-400'}`}
          >
            Annual
            <span className="text-xs bg-green-500 text-white px-1.5 py-0.5 rounded-full">-20%</span>
          </button>
        </div>
      </div>

      <div className="grid md:grid-cols-4 gap-6">
        {plans.map((plan) => {
          const displayPrice = isAnnual && plan.annualMonthly !== '$0' ? plan.annualMonthly : plan.price;
          const showAnnualTotal = isAnnual && plan.annualPrice !== '$0';

          return (
            <div key={plan.name} className={`bg-white dark:bg-gray-900 rounded-2xl border-2 p-6 flex flex-col ${plan.highlight ? 'border-green-500 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>
              {plan.badge && (
                <span className={`inline-block text-xs font-bold px-3 py-1 rounded-full mb-3 ${plan.badge === 'POPULAR' ? 'bg-green-500 text-white' : 'bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-800'}`}>
                  {plan.badge}
                </span>
              )}
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">{plan.name}</h3>
              <div className="mb-4 min-h-[3.5rem]">
                <span className="text-3xl font-bold text-gray-900 dark:text-white">{displayPrice}</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
                {showAnnualTotal && (
                  <div className="mt-0.5 text-xs text-green-600 dark:text-green-400 font-medium">
                    {plan.annualPrice}/yr — billed annually
                  </div>
                )}
                {!isAnnual && plan.annualPrice !== '$0' && (
                  <div className="mt-0.5 text-xs text-gray-400 dark:text-gray-500">
                    or {plan.annualPrice}/yr (save 20%)
                  </div>
                )}
              </div>
              <ul className="space-y-2 mb-6 flex-1">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                    <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />{f}
                  </li>
                ))}
              </ul>
              <PricingCTA planName={plan.name} ctaHref={plan.ctaHref} highlight={plan.highlight} />
            </div>
          );
        })}
      </div>
      <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-6">All plans include commercial use. No hidden fees. Cancel anytime.</p>
    </section>
  );
}
"""

with open(COMP_FILE, 'w', encoding='utf-8') as f:
    f.write(component)
print("PricingSection component created!")

# ── 2. page.tsx에서 Pricing 섹션 교체 ────────────────────────────────────────
PAGE_FILE = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"

with open(PAGE_FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# import 추가
old_import = "import PricingCTA from '@/components/PricingCTA';"
new_import = "import PricingCTA from '@/components/PricingCTA';\nimport PricingSection from '@/components/PricingSection';"
c = c.replace(old_import, new_import)

# Pricing 섹션 전체 교체
old_section = """      {/* Pricing */}
      <section id="pricing" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">Simple, transparent pricing</h2>
          <p className="text-xl text-gray-600 dark:text-gray-400">Start free, upgrade when you grow</p>
        </div>
        <div className="grid md:grid-cols-4 gap-6">
          {[
            { name: 'Free', price: '$0', annualPrice: '$0', annualMonthly: '$0', period: '/month', badge: null, features: ['10 monitors','5-minute checks','All alert channels','Public status page','30-day history','Commercial use allowed'], cta: 'Start Free', ctaHref: '/register', highlight: false },
            { name: 'Starter', price: '$5', annualPrice: '$48', annualMonthly: '$4', period: '/month', badge: 'POPULAR', features: ['20 monitors','1-minute checks','All alert channels','Analytics','30-day history','Commercial use allowed'], cta: 'Get Started', ctaHref: '/register', highlight: true },
            { name: 'Pro', price: '$15', annualPrice: '$144', annualMonthly: '$12', period: '/month', badge: 'Best for growing startups', features: ['100 monitors','30-second checks','Team sharing','Priority support','90-day history','Commercial use allowed'], cta: 'Get Started', ctaHref: '/register', highlight: false },
            { name: 'Business', price: '$49', annualPrice: '$470', annualMonthly: '$39', period: '/month', badge: null, features: ['Unlimited monitors','10-second checks','REST API access (API keys)','Custom features','SLA','1-year history'], cta: 'Get Started', ctaHref: '/register', highlight: false },
          ].map((plan) => (
            <div key={plan.name} className={`bg-white dark:bg-gray-900 rounded-2xl border-2 p-6 flex flex-col ${plan.highlight ? 'border-green-500 shadow-lg' : 'border-gray-200 dark:border-gray-700'}`}>
              {plan.badge && (
                <span className={`inline-block text-xs font-bold px-3 py-1 rounded-full mb-3 ${plan.badge === 'POPULAR' ? 'bg-green-500 text-white' : 'bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-800'}`}>
                  {plan.badge}
                </span>
              )}
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">{plan.name}</h3>
              <div className="mb-4">
                <span className="text-3xl font-bold text-gray-900 dark:text-white">{plan.price}</span>
                <span className="text-gray-500 dark:text-gray-400">{plan.period}</span>
                {plan.annualPrice !== '$0' && (
                  <span className="ml-2 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full">or {plan.annualPrice}/yr</span>
                )}
              </div>
              <ul className="space-y-2 mb-6 flex-1">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                    <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />{f}
                  </li>
                ))}
              </ul>
              <PricingCTA planName={plan.name} ctaHref={plan.ctaHref} highlight={plan.highlight} />
            </div>
          ))}
        </div>
        <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-6">All plans include commercial use. No hidden fees. Cancel anytime.</p>
      </section>"""

new_section = "      {/* Pricing */}\n      <PricingSection />"

c = c.replace(old_section, new_section)

with open(PAGE_FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("page.tsx updated!")
print("PricingSection import:", "PricingSection" in c)
print("Old section removed:", "annualMonthly" not in c)
