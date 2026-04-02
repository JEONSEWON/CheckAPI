import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock, CheckCircle } from 'lucide-react';

export const metadata = {
  title: 'API Monitoring Checklist for Solo Founders | CheckAPI',
  description: 'A practical checklist of what to monitor, how often, and what to do when things go wrong — written for indie hackers and solo founders running production APIs.',
};

export default function BlogPostChecklist() {
  const checks = [
    { category: 'Endpoints to Monitor', items: [
      'Health check endpoint (/health or /ping)',
      'Authentication endpoint (login, token refresh)',
      'Your most critical business endpoint (checkout, core feature)',
      'Third-party API integrations you depend on',
      'Webhook receivers (Stripe, Slack, etc.)',
    ]},
    { category: 'Alert Channels', items: [
      'Email alert set up for all monitors',
      'Slack or Telegram for instant notification',
      'Test alert sent and confirmed working',
      'Alert attached to each monitor (easy to forget)',
    ]},
    { category: 'Response Validation', items: [
      'Expected status code configured (usually 200)',
      'Silent failure detection enabled for critical endpoints',
      'Keyword or regex pattern validates real response content',
    ]},
    { category: 'Status Page', items: [
      'Public status page created for each critical monitor',
      'Status page URL shared in your app\'s footer or help docs',
      'Users can self-check before contacting support',
    ]},
    { category: 'Incident Response', items: [
      'You know what to do when an alert fires at 3am',
      'Runbook or notes for common failure modes',
      'Downtime acknowledged in status page or Twitter',
    ]},
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950">
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 dark:bg-gray-900/80 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">CheckAPI</span>
            </Link>
            <nav className="hidden md:flex space-x-8">
              <a href="/#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Features</a>
              <a href="/#pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Pricing</a>
              <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Docs</Link>
            </nav>
            <div className="flex items-center space-x-4"><PublicAuthButtons /></div>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="mb-4">
          <Link href="/blog" className="text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 transition">← Blog</Link>
        </div>

        <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400 mb-6">
          <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />Mar 25, 2026</span>
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />4 min read</span>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
          API Monitoring Checklist for Solo Founders
        </h1>

        <div className="text-gray-700 dark:text-gray-200 space-y-6">
          <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
            When you're running a production API solo, monitoring is the difference between finding out about downtime from your users and finding out before they do. Here's the complete checklist.
          </p>

          <p>
            Most founders set up one health check monitor and call it done. That's better than nothing — but there are a few more things worth spending 10 minutes on. The goal is to have full visibility with zero ongoing maintenance.
          </p>

          <div className="space-y-8 mt-8">
            {checks.map((section, si) => (
              <div key={si} className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-6">
                <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center text-sm font-bold">{si + 1}</span>
                  {section.category}
                </h2>
                <ul className="space-y-2">
                  {section.items.map((item, ii) => (
                    <li key={ii} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0 mt-0.5" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">The Most Common Mistake</h2>
          <p>
            Creating a monitor but forgetting to attach an alert channel. The monitor runs, catches failures, logs them — and sends no notification because there's no channel connected. Always test your alerts after setup.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-8">What About Third-Party APIs?</h2>
          <p>
            If your app depends on a payment processor, email service, or any external API, monitor it directly. Don't assume their status page will tell you before your users do. Point a monitor at their health endpoint if they have one, or your own integration endpoint.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-8">How Often to Check</h2>
          <p>
            For most solo projects, 5-minute checks (free plan) are fine. If you're doing real-time transactions or have paying customers, 1-minute checks (Starter plan) is worth the $5/month. The math is simple: would you rather find out about downtime 5 minutes in or 1 minute in?
          </p>
        </div>

        <div className="mt-12 p-6 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-xl">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Set up monitoring in 5 minutes</h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm">Free plan includes 10 monitors, all alert channels, and public status pages.</p>
          <Link href="/register" className="inline-flex items-center gap-2 bg-green-600 text-white px-5 py-2.5 rounded-lg hover:bg-green-700 transition font-medium">
            Get Started Free <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </main>

      <footer className="border-t border-gray-200 dark:border-gray-800 mt-16 py-8">
        <div className="max-w-3xl mx-auto px-4 text-center text-sm text-gray-500 dark:text-gray-400">
          © 2026 Axiom Technologies. <Link href="/blog" className="hover:text-green-600">← Back to Blog</Link>
        </div>
      </footer>
    </div>
  );
}
