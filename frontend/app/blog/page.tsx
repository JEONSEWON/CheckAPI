import Link from 'next/link';
import { ArrowRight, Calendar, Clock } from 'lucide-react';

const posts = [
  {
    title: 'Why API Monitoring Matters for Every Developer',
    excerpt: 'Your API going down at 3am without you knowing is not a hypothetical — it happens. Here\'s why monitoring should be the first thing you set up after deploying.',
    date: 'Feb 20, 2026',
    readTime: '4 min read',
    slug: '#',
  },
  {
    title: 'How to Set Up Slack Alerts for Your API in 5 Minutes',
    excerpt: 'Step-by-step guide to connecting CheckAPI with your Slack workspace so your team gets instant alerts the moment something goes wrong.',
    date: 'Feb 10, 2026',
    readTime: '3 min read',
    slug: '#',
  },
  {
    title: 'Free API Monitoring: What to Look For',
    excerpt: 'Not all free monitoring plans are equal. Here\'s a breakdown of what actually matters when choosing a free tier — and what to watch out for.',
    date: 'Jan 28, 2026',
    readTime: '5 min read',
    slug: '#',
  },
];

export default function BlogPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                CheckAPI
              </span>
            </Link>
            <nav className="hidden md:flex space-x-8">
              <a href="/#features" className="text-gray-700 hover:text-green-600 transition">Features</a>
              <a href="/#pricing" className="text-gray-700 hover:text-green-600 transition">Pricing</a>
              <Link href="/docs" className="text-gray-700 hover:text-green-600 transition">Docs</Link>
            </nav>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-700 hover:text-green-600 transition">Log in</Link>
              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          The CheckAPI
          <br />
          <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            Blog
          </span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Guides, tips, and best practices for API monitoring and reliability.
        </p>
      </section>

      {/* Posts */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24">
        <div className="space-y-6">
          {posts.map((post, i) => (
            <article key={i} className="bg-white rounded-xl border border-gray-200 p-8 hover:border-green-300 hover:shadow-lg transition">
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />{post.date}</span>
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" />{post.readTime}</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3 hover:text-green-600 transition">
                <a href={post.slug}>{post.title}</a>
              </h2>
              <p className="text-gray-600 leading-relaxed mb-4">{post.excerpt}</p>
              <a href={post.slug} className="inline-flex items-center text-green-600 font-medium hover:text-green-700 transition">
                Read more <ArrowRight className="ml-1 h-4 w-4" />
              </a>
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
      <footer className="border-t bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-gray-900 mb-4">CheckAPI</h3>
              <p className="text-gray-600 text-sm">Simple, reliable API monitoring for developers and teams.</p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><a href="/#features" className="hover:text-green-600">Features</a></li>
                <li><a href="/#pricing" className="hover:text-green-600">Pricing</a></li>
                <li><Link href="/docs" className="hover:text-green-600">Documentation</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><Link href="/about" className="hover:text-green-600">About</Link></li>
                <li><Link href="/blog" className="hover:text-green-600">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-green-600">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><Link href="/privacy" className="hover:text-green-600">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-green-600">Terms</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t mt-8 pt-8 text-center text-sm text-gray-600">
            © 2026 CheckAPI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
