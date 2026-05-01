import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock, CheckCircle, TrendingUp, Zap, Bell, BarChart2 } from 'lucide-react';

export const metadata = {
  title: 'API Uptime Checker: Track Availability, SLA & Uptime Percentage | CheckAPI',
  description: 'An API uptime checker measures your availability over time — 99.9% sounds great until you realize that\'s 8.7 hours of downtime a year. Here\'s how to track and improve it.',
};

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is an API uptime checker?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'An API uptime checker is a tool that continuously monitors your API endpoint and records whether each check succeeds or fails. Over time, it calculates your uptime percentage — the fraction of checks that returned a successful response — and displays it as a chart or report. This lets you track SLA compliance and identify reliability trends.',
      },
    },
    {
      '@type': 'Question',
      name: 'How is API uptime percentage calculated?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Uptime percentage = (number of successful checks / total checks) × 100. A check is considered successful if the API responds within the timeout with the expected status code. CheckAPI calculates uptime over 24-hour, 7-day, and 30-day windows so you can see both recent performance and longer-term trends.',
      },
    },
    {
      '@type': 'Question',
      name: 'What is considered good API uptime?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '99.9% uptime (three nines) is the common baseline for SaaS APIs — that allows 8.7 hours of downtime per year. 99.99% (four nines) means under 53 minutes per year and is expected for payment APIs and other critical services. For internal tools and side projects, 99.5% (43 hours/year) is often acceptable.',
      },
    },
    {
      '@type': 'Question',
      name: 'Is there a free API uptime checker?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. CheckAPI offers a free plan with 10 monitors, 5-minute check intervals, 30-day uptime history, and all alert channels (Email, Slack, Telegram, Discord, Webhook) included. No credit card required, and commercial use is explicitly allowed — unlike UptimeRobot which restricts commercial use on free plans.',
      },
    },
    {
      '@type': 'Question',
      name: 'How do I share my API uptime with customers?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'CheckAPI generates a public status page for each monitor at a unique URL (e.g. checkapi.io/status/your-api). Share this URL in your docs, dashboard, or support emails. It shows a 90-day uptime chart, current status, and incident history — without requiring customers to log in.',
      },
    },
  ],
};

const NINES = [
  { label: '99%', allowed: '3.65 days / year', perMonth: '7.2 hours', typical: 'Acceptable for internal tools' },
  { label: '99.5%', allowed: '1.83 days / year', perMonth: '3.6 hours', typical: 'Side projects, non-critical APIs' },
  { label: '99.9%', allowed: '8.7 hours / year', perMonth: '43 minutes', typical: 'Standard SaaS baseline' },
  { label: '99.95%', allowed: '4.4 hours / year', perMonth: '21 minutes', typical: 'B2B SaaS with paying customers' },
  { label: '99.99%', allowed: '52 min / year', perMonth: '4.4 minutes', typical: 'Payment APIs, critical services' },
];

export default function ApiUptimeCheckerPost() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />

      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 dark:bg-gray-900/80 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              CheckAPI
            </Link>
            <nav className="hidden md:flex space-x-8 text-sm">
              <a href="/#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Features</a>
              <Link href="/api-checker" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">API Checker</Link>
              <a href="/pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Pricing</a>
              <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Docs</Link>
              <Link href="/blog" className="text-green-600 font-medium">Blog</Link>
            </nav>
            <div className="flex items-center space-x-4"><PublicAuthButtons /></div>
          </div>
        </div>
      </header>

      {/* Article */}
      <article className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-24">
        <div className="mb-4">
          <Link href="/blog" className="text-sm text-gray-500 dark:text-gray-400 hover:text-green-600 transition">← Blog</Link>
        </div>

        <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400 mb-6">
          <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />May 1, 2026</span>
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />7 min read</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
          API Uptime Checker: Track Availability, SLA & Uptime Percentage
        </h1>

        <p className="text-xl text-gray-600 dark:text-gray-400 mb-12 leading-relaxed">
          99.9% uptime sounds reliable — until you realize it allows 8.7 hours of downtime every year. Knowing your real uptime percentage, not just guessing, is the difference between meeting your SLA and silently breaking it.
        </p>

        <div className="prose prose-lg max-w-none text-gray-700 dark:text-gray-300 space-y-10">

          {/* What is it */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Is an API Uptime Checker?</h2>
            <p>
              An API uptime checker sends automated HTTP requests to your API on a fixed schedule and records the result of each check — success or failure, and how long it took. Over time, it aggregates these results into an <strong>uptime percentage</strong>: the fraction of checks where your API responded correctly.
            </p>
            <p>
              This is different from just knowing when your API went down. Uptime tracking gives you a longitudinal view: Is my API getting more reliable or less reliable over time? Am I hitting my SLA targets? Where are my worst-performing hours of the day?
            </p>

            {/* Quick check CTA */}
            <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-5 flex items-center justify-between gap-4 flex-wrap">
              <div>
                <p className="font-semibold text-gray-900 dark:text-white text-sm">Check if your API is up right now</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Instant test — no account, no setup required.</p>
              </div>
              <Link
                href="/api-checker"
                className="flex-shrink-0 inline-flex items-center gap-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-semibold px-4 py-2 rounded-lg hover:opacity-90 transition"
              >
                <Zap className="h-4 w-4" /> Check API Now
              </Link>
            </div>
          </section>

          {/* How uptime is calculated */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Is API Uptime Percentage Calculated?</h2>
            <p>The formula is straightforward:</p>

            <div className="my-6 bg-gray-900 dark:bg-gray-950 rounded-xl px-6 py-5 text-center">
              <p className="text-green-400 font-mono text-lg font-bold">
                Uptime % = (Successful checks / Total checks) × 100
              </p>
            </div>

            <p>
              A check is <strong>successful</strong> if your API responds before the timeout with the expected HTTP status code. A check is a <strong>failure</strong> if it times out, returns an unexpected status code, or the connection is refused entirely.
            </p>
            <p className="mt-3">
              CheckAPI calculates uptime over three rolling windows — <strong>24 hours, 7 days, and 30 days</strong> — so you can distinguish between a bad day and a chronic reliability problem. You can also drill into the raw check history to see exactly which checks failed and why.
            </p>

            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-xl text-sm text-blue-800 dark:text-blue-300">
              <strong>Example:</strong> If CheckAPI runs 288 checks per day (every 5 minutes) and 284 succeed, your 24-hour uptime is 284/288 × 100 = <strong>98.6%</strong>. That sounds fine — but it means your API was down for about 20 minutes that day.
            </div>
          </section>

          {/* What counts as good uptime */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Counts as Good API Uptime?</h2>
            <p>
              The "nines" system is the industry standard for expressing uptime targets. Here is what each level actually means in real downtime:
            </p>

            <div className="mt-6 overflow-x-auto">
              <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Uptime</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Allowed downtime / year</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Allowed downtime / month</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Typical use case</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                  {NINES.map(({ label, allowed, perMonth, typical }) => (
                    <tr key={label} className="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900 dark:even:bg-gray-800">
                      <td className="px-4 py-3 font-bold text-green-600">{label}</td>
                      <td className="px-4 py-3 text-gray-700 dark:text-gray-300">{allowed}</td>
                      <td className="px-4 py-3 text-gray-700 dark:text-gray-300">{perMonth}</td>
                      <td className="px-4 py-3 text-gray-500 dark:text-gray-400 text-xs">{typical}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <p className="mt-4">
              Most SaaS companies commit to <strong>99.9% (three nines)</strong> in their Terms of Service. If you do not have uptime tracking, you cannot know whether you are actually hitting this target — and neither can your customers.
            </p>
          </section>

          {/* Why uptime tracking matters beyond alerts */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Why Does Uptime Tracking Matter Beyond Just Alerting?</h2>
            <p>Downtime alerts tell you when something broke. Uptime tracking tells you something deeper:</p>

            <div className="space-y-3 mt-4">
              {[
                {
                  icon: <BarChart2 className="h-5 w-5 text-green-500" />,
                  title: 'SLA compliance',
                  desc: 'If you promise 99.9% uptime and you are hitting 98.5%, you are in breach — even if you never missed an alert. Only uptime logs tell you this.',
                },
                {
                  icon: <TrendingUp className="h-5 w-5 text-green-500" />,
                  title: 'Reliability trends',
                  desc: 'Was your uptime better before the last major deployment? Is a specific endpoint degrading over time? Uptime history answers these questions.',
                },
                {
                  icon: <CheckCircle className="h-5 w-5 text-green-500" />,
                  title: 'Customer trust',
                  desc: 'A public status page showing 99.95% uptime over 90 days is a sales asset. Prospects and enterprise customers ask for uptime history before signing contracts.',
                },
                {
                  icon: <Bell className="h-5 w-5 text-green-500" />,
                  title: 'Incident post-mortems',
                  desc: 'When something goes wrong, uptime logs give you the exact timeline: when the API degraded, when it fully failed, and when it recovered.',
                },
              ].map(({ icon, title, desc }) => (
                <div key={title} className="flex gap-3 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl">
                  <span className="flex-shrink-0 mt-0.5">{icon}</span>
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white text-sm">{title}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* How to set up */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Do You Set Up an API Uptime Checker for Free?</h2>
            <p>CheckAPI tracks your uptime automatically once you add a monitor. Setup takes under 3 minutes:</p>

            <div className="space-y-4 mt-6">
              {[
                {
                  n: '1',
                  title: 'Create a free account',
                  desc: 'Sign up at checkapi.io/register — no credit card needed. Free plan includes 10 monitors with 30-day uptime history.',
                },
                {
                  n: '2',
                  title: 'Add your API endpoint',
                  desc: 'Enter the URL, HTTP method, and check interval. CheckAPI immediately starts recording check results and calculating uptime.',
                },
                {
                  n: '3',
                  title: 'Set your expected status code',
                  desc: 'Tell CheckAPI what a healthy response looks like. Usually 200, but can be any code your API uses for success.',
                },
                {
                  n: '4',
                  title: 'Connect an alert channel',
                  desc: 'Slack, Email, Telegram, Discord, or Webhook — all included on the free plan. You will be notified the moment uptime drops.',
                },
                {
                  n: '5',
                  title: 'Share your public status page',
                  desc: 'CheckAPI generates a public uptime page at /status/your-api. Share it with customers so they can check your status without contacting support.',
                },
              ].map((step) => (
                <div key={step.n} className="flex gap-4 p-5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl">
                  <span className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">{step.n}</span>
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white mb-1">{step.title}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Uptime vs downtime */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Is the Difference Between an Uptime Checker and a Downtime Checker?</h2>
            <p>
              These terms are often used interchangeably, but they describe a different emphasis:
            </p>
            <div className="mt-6 overflow-x-auto">
              <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300"> </th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Downtime checker focus</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Uptime checker focus</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                  {[
                    ['Primary goal', 'Alert you the instant something breaks', 'Track availability % over time'],
                    ['Key metric', 'Time to detect (TTD)', 'Uptime percentage (24h / 7d / 30d)'],
                    ['Output', 'Immediate alert notification', 'Uptime chart, SLA report'],
                    ['Customer-facing', 'No', 'Yes — public status page'],
                    ['Use case', 'Operations, incident response', 'SLA compliance, sales, trust'],
                  ].map(([aspect, down, up]) => (
                    <tr key={aspect} className="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900 dark:even:bg-gray-800">
                      <td className="px-4 py-2.5 font-medium text-gray-700 dark:text-gray-300 text-xs">{aspect}</td>
                      <td className="px-4 py-2.5 text-gray-500 dark:text-gray-400 text-xs">{down}</td>
                      <td className="px-4 py-2.5 text-green-600 text-xs font-medium">{up}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="mt-4">
              CheckAPI does both — it alerts you the moment your API fails (<Link href="/blog/api-downtime-checker" className="text-green-600 hover:text-green-700 font-medium">downtime detection</Link>) and tracks your uptime percentage over time. You do not need separate tools.
            </p>
          </section>

          {/* Silent failures and uptime */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Can Your Uptime Checker Miss Failures That Show 100% Uptime?</h2>
            <p>
              Yes — and this is one of the most dangerous gaps in basic uptime monitoring. If your API returns HTTP 200 but the response body contains an error message or broken data, a status-code-only checker will report <strong>100% uptime</strong> while your users are seeing failures.
            </p>
            <p className="mt-3">
              This is called a <Link href="/blog/silent-api-failures" className="text-green-600 hover:text-green-700 font-medium">silent failure</Link>. CheckAPI can detect them using:
            </p>
            <ul className="mt-3 space-y-2 list-none pl-0">
              {[
                { label: 'Keyword assertions', desc: 'Alert if a specific word is absent from the response (e.g. "status":"ok")' },
                { label: 'JSON Path assertions', desc: 'Check that a specific JSON field has an expected value (up to 10 per monitor)' },
                { label: 'Regex matching', desc: 'Validate response body against a regex pattern' },
                { label: 'Header assertions', desc: 'Verify Content-Type, Cache-Control, or any response header' },
              ].map(({ label, desc }) => (
                <li key={label} className="flex items-start gap-3 text-gray-700 dark:text-gray-300 text-sm">
                  <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0 mt-0.5" />
                  <span><strong>{label}</strong> — {desc}</span>
                </li>
              ))}
            </ul>
            <p className="mt-4">
              When one of these assertions fails, CheckAPI counts the check as a failure and includes it in your uptime calculation — giving you an accurate picture of real availability, not just HTTP reachability.
            </p>
          </section>

          {/* How to improve uptime */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Do You Improve Your API Uptime Percentage?</h2>
            <p>Uptime tracking is not just about measurement — it is about finding patterns you can fix. Once you have a few weeks of data, look for:</p>

            <div className="space-y-3 mt-4">
              {[
                { tip: 'Recurring failure windows', action: 'If your API fails at the same hour every day, check scheduled jobs, cron tasks, or database maintenance windows that run at that time.' },
                { tip: 'Failures correlated with deployments', action: 'If uptime drops after every deploy, your deployment process may need health checks before traffic is routed to the new version.' },
                { tip: 'Slow response times before failures', action: 'Response time creeping up before an outage often signals memory exhaustion or connection pool saturation. Set a response time alert threshold.' },
                { tip: 'Third-party dependency failures', action: 'If failures cluster around the same time as your payment provider or auth service outages, add a status page link for those dependencies.' },
              ].map(({ tip, action }) => (
                <div key={tip} className="p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl">
                  <p className="font-semibold text-gray-900 dark:text-white text-sm">{tip}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{action}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Related links */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Related Guides</h2>
            <div className="grid md:grid-cols-2 gap-4 mt-4">
              {[
                { href: '/blog/api-downtime-checker', title: 'API Downtime Checker', desc: 'How to detect and get alerted the moment your API goes down.' },
                { href: '/blog/silent-api-failures', title: 'Silent API Failures', desc: 'Your API returns 200 OK but the response is broken. How to detect it.' },
                { href: '/blog/public-status-page', title: 'Public Status Page', desc: 'Share your uptime history with customers. Free, takes 2 minutes.' },
                { href: '/blog/free-api-monitoring', title: 'Free API Monitoring', desc: 'Step-by-step guide to monitoring your API without paying anything.' },
              ].map(({ href, title, desc }) => (
                <Link key={href} href={href} className="group p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl hover:border-green-400 transition">
                  <p className="font-semibold text-gray-900 dark:text-white text-sm group-hover:text-green-600 transition">{title} →</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{desc}</p>
                </Link>
              ))}
            </div>
          </section>

        </div>

        {/* CTA */}
        <div className="mt-14 bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl p-8 text-center">
          <TrendingUp className="h-8 w-8 text-white mx-auto mb-4 opacity-90" />
          <h3 className="text-2xl font-bold text-white mb-2">Start tracking your API uptime today</h3>
          <p className="text-green-100 mb-6 text-sm">Free plan — 10 monitors, 30-day uptime history, all alert channels. No credit card required.</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              href="/register"
              className="inline-flex items-center gap-2 bg-white text-green-600 font-semibold px-6 py-3 rounded-xl hover:bg-gray-50 transition"
            >
              Start Monitoring Free <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/api-checker"
              className="inline-flex items-center gap-2 bg-green-700 text-white font-semibold px-6 py-3 rounded-xl hover:bg-green-800 transition"
            >
              <Zap className="h-4 w-4" /> Check My API Now
            </Link>
          </div>
        </div>
      </article>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-gray-900 dark:text-white mb-4">CheckAPI</h3>
              <p className="text-gray-500 dark:text-gray-400 text-sm">API uptime checker and downtime monitor. Free for commercial use.</p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Tools</h4>
              <ul className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
                <li><Link href="/api-checker" className="hover:text-green-600">API Checker</Link></li>
                <li><Link href="/dashboard" className="hover:text-green-600">Dashboard</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
                <li><Link href="/pricing" className="hover:text-green-600">Pricing</Link></li>
                <li><Link href="/docs" className="hover:text-green-600">Docs</Link></li>
                <li><Link href="/blog" className="hover:text-green-600">Blog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
                <li><Link href="/privacy" className="hover:text-green-600">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-green-600">Terms</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-200 dark:border-gray-800 pt-8 text-center text-sm text-gray-500 dark:text-gray-400">
            © 2026 CheckAPI by Axiom Technologies. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
