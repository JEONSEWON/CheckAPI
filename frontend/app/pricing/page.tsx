import Link from 'next/link';
import Image from 'next/image';
import { CheckCircle, X } from 'lucide-react';
import PricingSection from '@/components/PricingSection';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Pricing — CheckAPI',
  description: 'Simple, transparent pricing for API monitoring. Free for commercial use. No hidden fees. Upgrade when you grow.',
  openGraph: {
    title: 'Pricing — CheckAPI',
    description: 'Simple, transparent pricing for API monitoring. Free forever for commercial use.',
    url: 'https://checkapi.io/pricing',
  },
};

export default function PricingPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center gap-2">
              <Image src="/logo.png" alt="CheckAPI" width={40} height={40} className="h-10 w-10 rounded-xl object-contain" style={{ filter: 'drop-shadow(0 0 6px rgba(0,229,180,0.5))' }} priority />
            </Link>
            <nav className="hidden md:flex space-x-8">
              <Link href="/#features" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition text-sm">Features</Link>
              <Link href="/pricing" className="text-green-600 font-medium text-sm">Pricing</Link>
              <Link href="/docs" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition text-sm">Docs</Link>
            </nav>
            <div className="flex items-center gap-3">
              <Link href="/login" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition text-sm">Log in</Link>
              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium">Get Started</Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-4 text-center">
        <div className="inline-flex items-center gap-2 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 text-sm font-medium px-4 py-2 rounded-full mb-6">
          <CheckCircle className="h-4 w-4" />
          Free for Commercial Use — No restrictions
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4 tracking-tight">
          Simple, transparent pricing
        </h1>
        <p className="text-xl text-gray-500 dark:text-gray-400 max-w-xl mx-auto">
          Start free. Upgrade when you grow. No hidden fees, no credit card required.
        </p>
      </section>

      {/* Pricing Section (reuse existing component) */}
      <PricingSection />

      {/* Feature Comparison Table */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-10">Full Feature Comparison</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 pr-6 text-gray-500 dark:text-gray-400 font-medium w-1/3">Feature</th>
                {['Free', 'Starter', 'Pro', 'Business'].map(plan => (
                  <th key={plan} className="text-center py-3 px-4 text-gray-900 dark:text-white font-semibold">{plan}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
              {[
                { feature: 'Monitors', values: ['10', '20', '100', 'Unlimited'] },
                { feature: 'Check interval', values: ['5 min', '1 min', '30 sec', '10 sec'] },
                { feature: 'Check history', values: ['30 days', '30 days', '90 days', '365 days'] },
                { feature: 'Alert channels', values: [true, true, true, true] },
                { feature: 'Email alerts', values: [true, true, true, true] },
                { feature: 'Slack / Telegram / Discord', values: [true, true, true, true] },
                { feature: 'Custom webhook', values: [true, true, true, true] },
                { feature: 'Public status page', values: [true, true, true, true] },
                { feature: 'Silent Failure Detection', values: [true, true, true, true] },
                { feature: 'Regex validation', values: [true, true, true, true] },
                { feature: 'JSON Path assertions', values: [true, true, true, true] },
                { feature: 'Heartbeat / Cron monitoring', values: [true, true, true, true] },
                { feature: 'Maintenance windows', values: [true, true, true, true] },
                { feature: 'Analytics & SLA reports', values: [false, true, true, true] },
                { feature: 'REST API access', values: [false, false, false, true] },
                { feature: 'Commercial use', values: [true, true, true, true] },
              ].map((row) => (
                <tr key={row.feature} className="hover:bg-gray-50 dark:hover:bg-gray-900 transition">
                  <td className="py-3 pr-6 text-gray-700 dark:text-gray-300">{row.feature}</td>
                  {row.values.map((val, i) => (
                    <td key={i} className="py-3 px-4 text-center">
                      {typeof val === 'boolean' ? (
                        val
                          ? <CheckCircle className="h-4 w-4 text-green-500 mx-auto" />
                          : <X className="h-4 w-4 text-gray-300 dark:text-gray-600 mx-auto" />
                      ) : (
                        <span className="text-gray-700 dark:text-gray-300 font-medium">{val}</span>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Fair Usage Policy */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl p-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Fair Usage Policy</h2>
          <div className="space-y-4 text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
            <p>
              CheckAPI's free plan is designed for real projects — personal, commercial, or anything in between.
              There are no restrictions on how you use your monitors.
            </p>
            <p>
              That said, we ask that you use the service in good faith:
            </p>
            <ul className="space-y-2 pl-4">
              {[
                'Do not use CheckAPI to deliberately generate excessive load on third-party servers.',
                'Do not create automated scripts that register and delete monitors at high volume.',
                'Do not attempt to use the free plan as a substitute for a paid plan by creating multiple accounts.',
                'Monitors pointing to localhost, private IPs, or non-public endpoints may not function as expected.',
              ].map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-gray-400 mt-0.5">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
            <p>
              Accounts that appear to violate these guidelines may be subject to a soft limit or contacted directly.
              We will always reach out before taking any action.
            </p>
            <p className="text-gray-500 dark:text-gray-500 text-xs mt-4">
              Last updated: April 2026 · Questions? <a href="/contact" className="text-green-600 hover:underline">Contact us</a>
            </p>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">Frequently Asked Questions</h2>
        <div className="space-y-6">
          {[
            {
              q: 'Is the free plan really free for commercial use?',
              a: 'Yes. Unlike UptimeRobot (which restricted commercial use in late 2024), CheckAPI has no restrictions on commercial use across all plans. Use it for your SaaS, agency clients, or any business project.'
            },
            {
              q: 'What happens when I reach my monitor limit?',
              a: 'You\'ll see an upgrade prompt when you try to add a monitor beyond your plan\'s limit. Your existing monitors keep running — nothing breaks.'
            },
            {
              q: 'Can I cancel anytime?',
              a: 'Yes. Cancel anytime from your billing settings. Your plan stays active until the end of the billing period.'
            },
            {
              q: 'Do you offer refunds?',
              a: 'If you\'re not satisfied within 7 days of upgrading, contact us and we\'ll issue a full refund.'
            },
            {
              q: 'Where are checks run from?',
              a: 'Checks are currently run from US West. Multi-region monitoring is on our roadmap.'
            },
          ].map((item, i) => (
            <div key={i} className="border-b border-gray-100 dark:border-gray-800 pb-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{item.q}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{item.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Start monitoring for free</h2>
        <p className="text-gray-500 dark:text-gray-400 mb-8">No credit card required. 10 monitors free forever.</p>
        <Link href="/register" className="inline-flex items-center gap-2 bg-green-600 text-white px-8 py-4 rounded-xl hover:bg-green-700 transition font-semibold text-lg">
          Get Started Free
        </Link>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
        © 2026 Axiom Technologies.
        <Link href="/privacy" className="ml-4 hover:text-green-600">Privacy</Link>
        <Link href="/terms" className="ml-4 hover:text-green-600">Terms</Link>
        <Link href="/contact" className="ml-4 hover:text-green-600">Contact</Link>
      </footer>
    </div>
  );
}
