import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock, CheckCircle, AlertCircle, Zap, Bell } from 'lucide-react';

export const metadata = {
  title: 'API Downtime Checker: How to Know the Moment Your API Goes Down | CheckAPI',
  description: 'An API downtime checker monitors your API 24/7 and alerts you the moment it fails — before your users notice. Here\'s how to set one up for free.',
};

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is an API downtime checker?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'An API downtime checker is a tool that automatically sends HTTP requests to your API on a schedule and alerts you when it fails to respond correctly. It checks status codes, response times, and optionally validates the response body so you know about failures before your users do.',
      },
    },
    {
      '@type': 'Question',
      name: 'How often should an API downtime checker run?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'For most projects, every 5 minutes is sufficient and is available on free plans. If you have paying customers or handle real-time transactions, every 1 minute (Starter plan) or every 30 seconds (Pro plan) catches issues faster and reduces the mean time to detection.',
      },
    },
    {
      '@type': 'Question',
      name: 'What is the difference between an API downtime checker and a ping monitor?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'A ping monitor only checks if a host is reachable at the network level. An API downtime checker makes a real HTTP request, checks the status code, measures response time, and can validate the response body. This means it catches silent failures — cases where the server responds with 200 OK but returns broken data.',
      },
    },
    {
      '@type': 'Question',
      name: 'Is there a free API downtime checker?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. CheckAPI offers a free plan with 10 monitors, 5-minute check intervals, and all alert channels (Email, Slack, Telegram, Discord, Webhook) included. No credit card required, and commercial use is explicitly allowed.',
      },
    },
    {
      '@type': 'Question',
      name: 'What should I do when my API downtime checker fires an alert?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'First, check the alert details — status code, error message, and whether it is a one-off or repeated failure. If repeated, check your server logs and recent deployments. Update your public status page to inform users. Once resolved, the checker will send a recovery alert automatically.',
      },
    },
  ],
};

export default function ApiDowntimeCheckerPost() {
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
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />6 min read</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
          API Downtime Checker: How to Know the Moment Your API Goes Down
        </h1>

        <p className="text-xl text-gray-600 dark:text-gray-400 mb-12 leading-relaxed">
          Your API went down at 2am. You found out at 9am when users started emailing. Every minute of undetected downtime is a minute of lost revenue and user trust. An API downtime checker fixes this — automatically, 24/7.
        </p>

        <div className="prose prose-lg max-w-none text-gray-700 dark:text-gray-300 space-y-10">

          {/* What is it */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Is an API Downtime Checker?</h2>
            <p>
              An API downtime checker is a tool that automatically sends HTTP requests to your API on a fixed schedule — every 5 minutes, every minute, or even every 30 seconds — and alerts you the moment it stops responding correctly.
            </p>
            <p>
              Unlike a manual check (curl, Postman, your browser), a downtime checker runs continuously in the background. You set it up once and forget about it. When something breaks, it finds you — not the other way around.
            </p>

            {/* Quick check CTA */}
            <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-5 flex items-center justify-between gap-4 flex-wrap">
              <div>
                <p className="font-semibold text-gray-900 dark:text-white text-sm">Want to check your API right now?</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Paste any URL and get instant results — no account needed.</p>
              </div>
              <Link
                href="/api-checker"
                className="flex-shrink-0 inline-flex items-center gap-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-semibold px-4 py-2 rounded-lg hover:opacity-90 transition"
              >
                <Zap className="h-4 w-4" /> Check API Now
              </Link>
            </div>
          </section>

          {/* Why APIs go down */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Why Do APIs Go Down Without Warning?</h2>
            <p>APIs fail in predictable and unpredictable ways. The most common causes:</p>
            <div className="space-y-3 mt-4">
              {[
                { cause: 'Deployment gone wrong', detail: 'A new release introduces a bug that crashes the server. The old version was fine; the new one is not.' },
                { cause: 'Database connection exhaustion', detail: 'Too many open connections, a slow query, or a migration that locks tables — your API starts returning 500s while the DB is technically running.' },
                { cause: 'Third-party dependency failure', detail: 'Your payment provider, email service, or auth system goes down and takes your API with it.' },
                { cause: 'Certificate expiry', detail: 'Your SSL certificate expires and every HTTPS request fails with a certificate error.' },
                { cause: 'Memory leak / OOM', detail: 'Your server gradually runs out of memory and stops accepting new requests, often hours or days after the leak started.' },
              ].map(({ cause, detail }) => (
                <div key={cause} className="flex gap-3 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl">
                  <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white text-sm">{cause}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{detail}</p>
                  </div>
                </div>
              ))}
            </div>
            <p className="mt-4">
              None of these failures announce themselves. They just happen — usually at the worst possible time.
            </p>
          </section>

          {/* What a good checker does */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Should a Good API Downtime Checker Do?</h2>
            <p>Not all downtime checkers are equal. Here is what separates a useful tool from a basic ping monitor:</p>

            <div className="mt-6 overflow-x-auto">
              <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Feature</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Basic ping</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Good API checker</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                  {[
                    ['Checks if host is reachable', '✅', '✅'],
                    ['Checks HTTP status code', '❌', '✅'],
                    ['Measures response time', '❌', '✅'],
                    ['Validates response body', '❌', '✅'],
                    ['Alerts on silent failures (200 with error body)', '❌', '✅'],
                    ['Sends alerts via Slack / Email / Telegram', '❌', '✅'],
                    ['SSL certificate expiry alerts', '❌', '✅'],
                    ['Uptime history & incident log', '❌', '✅'],
                  ].map(([feature, basic, good]) => (
                    <tr key={feature} className="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900 dark:even:bg-gray-800">
                      <td className="px-4 py-2.5 text-gray-700 dark:text-gray-300">{feature}</td>
                      <td className="px-4 py-2.5 text-center text-gray-400">{basic}</td>
                      <td className="px-4 py-2.5 text-center text-green-600">{good}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <p className="mt-4">
              The most important gap is <strong>response body validation</strong>. An API can return HTTP 200 while serving broken data — a database error wrapped in a polite status code. A basic ping passes this; a proper downtime checker catches it. This is called a <Link href="/blog/silent-api-failures" className="text-green-600 hover:text-green-700 font-medium">silent failure</Link>.
            </p>
          </section>

          {/* How to set up */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Do You Set Up a Free API Downtime Checker?</h2>
            <p>Setting up CheckAPI takes under 3 minutes:</p>

            <div className="space-y-4 mt-6">
              {[
                {
                  n: '1',
                  title: 'Create a free account',
                  desc: 'Sign up at checkapi.io/register. No credit card required. You get 10 monitors free, forever.',
                },
                {
                  n: '2',
                  title: 'Add your API endpoint',
                  desc: 'Enter your API URL (e.g. https://api.yourapp.com/health), select the HTTP method, and set the check interval. 5 minutes on the free plan.',
                },
                {
                  n: '3',
                  title: 'Set the expected status code',
                  desc: 'Usually 200. If your endpoint returns a different code for healthy responses, set it here.',
                },
                {
                  n: '4',
                  title: 'Add an alert channel',
                  desc: 'Connect Email, Slack, Telegram, Discord, or a custom webhook. All channels are included on the free plan — no upgrade needed.',
                },
                {
                  n: '5',
                  title: 'Send a test alert',
                  desc: 'Click "Test Alert" to confirm you receive a notification. Better to find out now than at 3am.',
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

          {/* How often to check */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Often Should Your API Downtime Checker Run?</h2>
            <p>The right interval depends on what you are monitoring and your tolerance for downtime:</p>

            <div className="grid md:grid-cols-2 gap-4 mt-6">
              {[
                { interval: 'Every 5 minutes', plan: 'Free plan', who: 'Side projects, internal tools, low-traffic APIs. Downtime detected within 5 minutes on average.' },
                { interval: 'Every 1 minute', plan: 'Starter ($5/mo)', who: 'SaaS products with paying users. Downtime detected within 1 minute — acceptable for most B2B products.' },
                { interval: 'Every 30 seconds', plan: 'Pro ($15/mo)', who: 'Consumer apps, checkout flows, real-time APIs. Fast detection before users notice.' },
                { interval: 'Every 10 seconds', plan: 'Business ($49/mo)', who: 'Critical infrastructure, financial APIs, high-traffic services where every second counts.' },
              ].map(({ interval, plan, who }) => (
                <div key={interval} className="p-5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-gray-900 dark:text-white text-sm">{interval}</span>
                    <span className="text-xs text-green-600 font-medium bg-green-50 dark:bg-green-950 px-2 py-0.5 rounded-full">{plan}</span>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{who}</p>
                </div>
              ))}
            </div>
          </section>

          {/* What to do when it fires */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Should You Do When a Downtime Alert Fires?</h2>
            <p>A good downtime checker gives you all the information you need to act fast. When an alert fires:</p>
            <ol className="mt-4 space-y-3 list-none pl-0">
              {[
                { n: '1', text: 'Check the alert details — status code, error message, which endpoint failed.' },
                { n: '2', text: 'Check if it is a one-off or repeated failure. A single blip may not need action; three consecutive failures always do.' },
                { n: '3', text: 'Look at your server logs and recent deployments. Did something change in the last hour?' },
                { n: '4', text: 'Update your public status page so users know you are aware. This cuts support tickets in half.' },
                { n: '5', text: 'Fix the issue. Your checker will send a recovery alert automatically when the API comes back up.' },
              ].map(({ n, text }) => (
                <li key={n} className="flex items-start gap-3 text-gray-700 dark:text-gray-300">
                  <span className="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">{n}</span>
                  {text}
                </li>
              ))}
            </ol>
          </section>

          {/* Alert threshold */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Do You Avoid False Positive Downtime Alerts?</h2>
            <p>
              Network blips happen. A single failed check does not always mean your API is down. A good downtime checker lets you set an <strong>alert threshold</strong> — only fire an alert after N consecutive failures.
            </p>
            <p className="mt-3">
              CheckAPI defaults to alerting after 1 failure (fastest detection), but you can set it to 2 or 3 to filter out transient errors. You will still see the blip in your check history, but your Slack channel will not wake up the team for a 5-second hiccup.
            </p>
          </section>

          {/* Related links */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Related Guides</h2>
            <div className="grid md:grid-cols-2 gap-4 mt-4">
              {[
                { href: '/blog/silent-api-failures', title: 'Silent API Failures', desc: 'Your API returns 200 OK but the response is broken. How to detect it.' },
                { href: '/blog/slack-api-alerts', title: 'Slack API Alerts', desc: 'Set up Slack notifications for API downtime in 5 minutes.' },
                { href: '/blog/free-api-monitoring', title: 'Free API Monitoring', desc: 'Step-by-step guide to monitoring your API for free.' },
                { href: '/blog/public-status-page', title: 'Public Status Page', desc: 'Share your uptime with users. Free, takes 2 minutes to set up.' },
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
          <Bell className="h-8 w-8 text-white mx-auto mb-4 opacity-90" />
          <h3 className="text-2xl font-bold text-white mb-2">Set up your API downtime checker</h3>
          <p className="text-green-100 mb-6 text-sm">Free plan — 10 monitors, all alert channels, 5-minute checks. No credit card required.</p>
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
              <p className="text-gray-500 dark:text-gray-400 text-sm">API downtime checker and uptime monitor. Free for commercial use.</p>
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
