import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock } from 'lucide-react';

const posts = [
  {
    title: 'Best Free UptimeRobot Alternatives in 2026',
    excerpt: 'UptimeRobot recently restricted commercial use on free plans. Here are the best alternatives that still offer genuinely free monitoring — no strings attached.',
    date: 'Feb 20, 2026',
    readTime: '5 min read',
    slug: '/blog/uptimerobot-alternatives',
  },
  {
    title: 'How to Monitor Your API for Free (And Actually Get Alerted)',
    excerpt: 'Free API monitoring sounds great until you realize most tools either limit you to 1 monitor or charge for alerts. Here\'s how to do it properly without paying a cent.',
    date: 'Feb 10, 2026',
    readTime: '4 min read',
    slug: '/blog/free-api-monitoring',
  },
  {
    title: 'How to Set Up Slack Alerts for API Downtime in 5 Minutes',
    excerpt: 'Step-by-step guide to getting instant Slack notifications the moment your API goes down. No code required.',
    date: 'Jan 28, 2026',
    readTime: '3 min read',
    slug: '/blog/slack-api-alerts',
  },
];

export default function BlogPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 dark:bg-gray-900/80 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                CheckAPI
              </span>
            </Link>
            <nav className="hidden md:flex space-x-8">
              <a href="/#features" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Features</a>
              <a href="/#pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Pricing</a>
              <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Docs</Link>
            </nav>
            <div className="flex items-center space-x-4">
              <PublicAuthButtons />
            </div>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
          The CheckAPI
          <br />
          <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            Blog
          </span>
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Guides, tips, and best practices for API monitoring and reliability.
        </p>
      </section>

      {/* Posts */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24">
        <div className="space-y-6">
          {posts.map((post, i) => (
            <article key={i} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8 hover:border-green-300 hover:shadow-lg transition">
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-3">
                <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />{post.date}</span>
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" />{post.readTime}</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3 hover:text-green-600 transition">
                <Link href={post.slug}>{post.title}</Link>
              </h2>
              <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">{post.excerpt}</p>
              <Link href={post.slug} className="inline-flex items-center text-green-600 font-medium hover:text-green-700 transition">
                Read more <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </article>
            {/* New posts */}
            <article className="border-b border-gray-200 dark:border-gray-700 pb-10">
              <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-200 dark:text-gray-400 mb-3">
                <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />Mar 15, 2026</span>
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" />5 min read</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                <Link href="/blog/silent-api-failures" className="hover:text-green-600 transition">
                  What is a Silent API Failure? (And How to Detect It)
                </Link>
              </h2>
              <p className="text-gray-600 dark:text-gray-200 dark:text-gray-400 mb-4">
                Your API returns 200 OK — but the response body is empty, broken, or contains an error message. This is a silent failure, and most monitoring tools miss it entirely.
              </p>
              <Link href="/blog/silent-api-failures" className="text-green-600 hover:text-green-700 font-medium flex items-center gap-1">
                Read more <ArrowRight className="h-4 w-4" />
              </Link>
            </article>

            <article className="border-b border-gray-200 dark:border-gray-700 pb-10">
              <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-200 dark:text-gray-400 mb-3">
                <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />Mar 25, 2026</span>
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" />4 min read</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                <Link href="/blog/api-monitoring-checklist" className="hover:text-green-600 transition">
                  API Monitoring Checklist for Solo Founders
                </Link>
              </h2>
              <p className="text-gray-600 dark:text-gray-200 dark:text-gray-400 mb-4">
                A practical checklist of what to monitor, how often, and what to do when things go wrong — written for indie hackers and solo founders running production APIs.
              </p>
              <Link href="/blog/api-monitoring-checklist" className="text-green-600 hover:text-green-700 font-medium flex items-center gap-1">
                Read more <ArrowRight className="h-4 w-4" />
              </Link>
            </article>

            <article className="border-b border-gray-200 dark:border-gray-700 pb-10">
              <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-200 dark:text-gray-400 mb-3">
                <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />Apr 1, 2026</span>
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" />4 min read</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                <Link href="/blog/public-status-page" className="hover:text-green-600 transition">
                  How to Set Up a Free Public Status Page for Your API
                </Link>
              </h2>
              <p className="text-gray-600 dark:text-gray-200 dark:text-gray-400 mb-4">
                A public status page reduces support tickets, builds user trust, and takes 2 minutes to set up. Here&apos;s how to do it for free.
              </p>
              <Link href="/blog/public-status-page" className="text-green-600 hover:text-green-700 font-medium flex items-center gap-1">
                Read more <ArrowRight className="h-4 w-4" />
              </Link>
            </article>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-green-600 to-emerald-600 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">Start monitoring your APIs today</h2>
          <p className="text-xl text-green-100 mb-8">Free plan available. No credit card required.</p>
          <Link href="/register" className="inline-flex items-center justify-center bg-white text-green-600 px-8 py-3 rounded-lg hover:bg-gray-50 transition text-lg font-medium">
            Get Started Free
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white dark:bg-gray-900 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-gray-900 dark:text-white mb-4">CheckAPI</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">Simple, reliable API monitoring for developers and teams.</p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><a href="/#features" className="hover:text-green-600">Features</a></li>
                <li><a href="/#pricing" className="hover:text-green-600">Pricing</a></li>
                <li><Link href="/docs" className="hover:text-green-600">Documentation</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><Link href="/about" className="hover:text-green-600">About</Link></li>
                <li><Link href="/blog" className="hover:text-green-600">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-green-600">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><Link href="/privacy" className="hover:text-green-600">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-green-600">Terms</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t mt-8 pt-8 text-center text-sm text-gray-600 dark:text-gray-400 dark:border-gray-800">
            © 2026 CheckAPI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
