import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock } from 'lucide-react';

export const metadata = {
  title: 'How to Set Up a Free Public Status Page for Your API | CheckAPI',
  description: 'A public status page reduces support tickets, builds user trust, and takes 2 minutes to set up. Here\'s how to do it for free with CheckAPI.',
};

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'Why should you set up a public status page?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Three reasons: fewer support tickets (users who can self-diagnose do not email you), more trust (transparency during incidents builds credibility), and professionalism (enterprise tools all have status pages, having one signals you take reliability seriously).',
      },
    },
    {
      '@type': 'Question',
      name: 'How do you set up a public status page with CheckAPI?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Four steps: (1) Create a monitor for your API endpoint. (2) Open the monitor detail page. (3) Copy the public status page URL — it looks like checkapi.io/status/your-monitor-id. (4) Share it in your app footer or help docs. The page updates automatically.',
      },
    },
    {
      '@type': 'Question',
      name: 'What does a CheckAPI public status page show?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: "CheckAPI's public status page shows: current status (Operational / Degraded / Outage), 90-day uptime history bar chart, 24h/7d/30d uptime percentages, average response time, and recent incidents with timestamps. No login required to view.",
      },
    },
    {
      '@type': 'Question',
      name: 'Is a CheckAPI public status page free?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: "Yes. Public status pages are included on CheckAPI's free plan. You get one status page per monitor, and the free plan includes up to 10 monitors. Most standalone status page tools like Statuspage by Atlassian charge $29/month separately.",
      },
    },
    {
      '@type': 'Question',
      name: 'Where should you share your public status page URL?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Best places to link your status page: footer of your web app, help center or FAQ page, GitHub repository README, Twitter/X bio, and auto-response for support emails.',
      },
    },
  ],
};

export default function BlogPostStatusPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 dark:bg-gray-900/80 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">CheckAPI</span>
            </Link>
            <nav className="hidden md:flex space-x-8">
              <a href="/#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Features</a>
              <a href="/pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Pricing</a>
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
          <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />Apr 1, 2026</span>
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />4 min read</span>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
          How to Set Up a Free Public Status Page for Your API
        </h1>

        <div className="text-gray-700 dark:text-gray-200 space-y-6">
          <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
            Every time your API goes down, some percentage of your users will email support instead of waiting. A public status page cuts that in half — users check it, see the issue is known, and wait. Here's how to set one up for free in 2 minutes.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">Why Bother with a Status Page?</h2>
          <p>Three reasons:</p>
          <ul className="space-y-2 pl-4 list-disc text-gray-600 dark:text-gray-300">
            <li><strong className="text-gray-900 dark:text-white">Fewer support tickets.</strong> Users who can self-diagnose don't email you.</li>
            <li><strong className="text-gray-900 dark:text-white">More trust.</strong> Transparency during incidents builds credibility, not destroys it.</li>
            <li><strong className="text-gray-900 dark:text-white">Professionalism.</strong> Enterprise tools all have status pages. Having one signals you take reliability seriously.</li>
          </ul>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">How Do You Set Up a Public Status Page with CheckAPI?</h2>

          <div className="space-y-4">
            {[
              { step: '1', title: 'Create a monitor', desc: 'Go to your CheckAPI dashboard and add a monitor for your API endpoint. If you already have one, skip this step.' },
              { step: '2', title: 'Go to the monitor detail page', desc: 'Click on your monitor to open the detail view. You\'ll see a "Status Page" button in the top right.' },
              { step: '3', title: 'Copy the status page URL', desc: 'Click "Status Page" to copy the public URL. It looks like checkapi.io/status/your-monitor-id.' },
              { step: '4', title: 'Share it', desc: 'Add the link to your app\'s footer, help docs, or README. That\'s it — the page updates automatically in real time.' },
            ].map((item) => (
              <div key={item.step} className="flex gap-4 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl">
                <div className="w-8 h-8 bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center font-bold flex-shrink-0">{item.step}</div>
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{item.title}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">What Does a CheckAPI Public Status Page Show?</h2>
          <p>CheckAPI's public status page includes:</p>
          <ul className="space-y-1 pl-4 list-disc text-gray-600 dark:text-gray-300">
            <li>Current status (Operational / Degraded / Outage)</li>
            <li>90-day uptime history bar chart</li>
            <li>24h, 7d, and 30d uptime percentages</li>
            <li>Average response time</li>
            <li>Recent incidents with timestamps</li>
          </ul>
          <p>No login required. Anyone with the link can view it.</p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">Is It Really Free?</h2>
          <p>
            Yes. Public status pages are included on CheckAPI's free plan. No upgrade required. You get one status page per monitor, and the free plan includes up to 10 monitors.
          </p>
          <p>
            Most status page tools charge separately — Statuspage by Atlassian starts at $29/month just for the status page. CheckAPI includes it as part of the monitoring package, because a status page without real monitoring data isn't very useful anyway.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">Where Should You Share Your Public Status Page URL?</h2>
          <ul className="space-y-1 pl-4 list-disc text-gray-600 dark:text-gray-300">
            <li>Footer of your web app</li>
            <li>Help center or FAQ page</li>
            <li>GitHub repository README</li>
            <li>Twitter/X bio</li>
            <li>Auto-response for support emails</li>
          </ul>
        </div>

        <div className="mt-12 p-6 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-xl">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Set up your status page in 2 minutes</h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm">Free plan. No credit card. Status pages included on all plans.</p>
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
