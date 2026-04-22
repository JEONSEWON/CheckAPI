import os

path = r"C:\home\jeon\api-health-monitor\frontend\app\about\page.tsx"

new_content = '''import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, CheckCircle, Zap, Shield, Heart, Code2, Globe } from 'lucide-react';

export const metadata = {
  title: 'About – CheckAPI',
  description: 'CheckAPI is built by a solo developer from Seoul. The story behind building a monitoring tool that catches what others miss.',
};

export default function AboutPage() {
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
              <a href="/pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Pricing</a>
              <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Docs</Link>
              <Link href="/blog" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Blog</Link>
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
          Built by a Developer,
          <br />
          <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            For Developers
          </span>
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          CheckAPI was born from a simple frustration — existing monitoring tools either missed the real failures or cost too much for what they offered.
        </p>
      </section>

      {/* Story */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-10 shadow-sm">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center text-white font-bold text-sm">SW</div>
            <div>
              <p className="font-semibold text-gray-900 dark:text-white">Sewon Jeon</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">Founder · Seoul, South Korea 🇰🇷</p>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">The Story</h2>
          <div className="space-y-4 text-gray-600 dark:text-gray-400 text-lg leading-relaxed">
            <p>
              I was running APIs in production and kept getting surprised by failures my monitoring tool completely missed. The API returned <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded text-sm">200 OK</code> — but the response body was broken. Null data. Silent errors buried in JSON. My monitor said everything was fine. My users knew otherwise.
            </p>
            <p>
              I wanted a tool that validated the actual response body — with regex patterns and JSON path assertions — not just the status code. Something that catches silent failures before users do.
            </p>
            <p>
              The existing options were either too expensive, too limited, or locked real features behind paid tiers. So I built CheckAPI: the monitoring tool I actually wanted to use.
            </p>
            <p>
              CheckAPI is a one-person product, built and maintained by me from Seoul. Every feature request gets read. Every bug gets fixed. No bloat, no committees — just a developer building the tool that works.
            </p>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">What CheckAPI Stands For</h2>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: <Zap className="h-8 w-8 text-green-600" />,
              title: 'Beyond Status Codes',
              description: 'Most monitors stop at HTTP 200. CheckAPI goes deeper — validating response bodies with regex and JSON path assertions to catch silent failures.'
            },
            {
              icon: <Shield className="h-8 w-8 text-green-600" />,
              title: 'Free for Real Work',
              description: "Free means free. No commercial-use restrictions, no credit card required, no 1-monitor limits. 10 monitors, all alert channels, actual production use — on the free plan."
            },
            {
              icon: <Code2 className="h-8 w-8 text-green-600" />,
              title: 'Built by a Developer',
              description: 'Not a VC-backed startup optimizing for growth metrics. A developer building the tool they actually wanted to use. Simpler, faster, more honest.'
            },
          ].map((item, i) => (
            <div key={i} className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-green-300 hover:shadow-lg transition">
              <div className="mb-4">{item.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{item.title}</h3>
              <p className="text-gray-600 dark:text-gray-400">{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Built With */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-16">
        <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700 p-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Tech Stack</h2>
          <div className="grid grid-cols-2 gap-3 text-sm text-gray-600 dark:text-gray-400">
            {[
              ['Backend', 'FastAPI + Celery + Redis'],
              ['Database', 'PostgreSQL'],
              ['Frontend', 'Next.js 14 + TypeScript'],
              ['Styling', 'Tailwind CSS'],
              ['Backend Hosting', 'Railway'],
              ['Frontend Hosting', 'Vercel'],
              ['DNS', 'Cloudflare'],
              ['Payments', 'LemonSqueezy'],
            ].map(([label, value]) => (
              <div key={label} className="flex gap-2">
                <span className="font-medium text-gray-800 dark:text-gray-200 w-36 shrink-0">{label}</span>
                <span>{value}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-green-600 to-emerald-600 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">Ready to get started?</h2>
          <p className="text-xl text-green-100 mb-8">Free plan available. No credit card required.</p>
          <Link href="/register" className="inline-flex items-center justify-center bg-white text-green-600 px-8 py-3 rounded-lg hover:bg-gray-50 transition text-lg font-medium">
            Start Monitoring Free
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white dark:bg-gray-900 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">CheckAPI</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">Silent Failure Detection for APIs. Free forever for commercial use.</p>
              <p className="text-gray-500 dark:text-gray-500 text-xs">by Axiom Technologies · Seoul 🇰🇷</p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><a href="/#features" className="hover:text-green-600">Features</a></li>
                <li><a href="/pricing" className="hover:text-green-600">Pricing</a></li>
                <li><Link href="/docs" className="hover:text-green-600">Documentation</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><Link href="/about" className="hover:text-green-600">About</Link></li>
                <li><Link href="/blog" className="hover:text-green-600">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-green-600">Contact</Link></li>
                <li><a href="https://x.com/imwon_dev" target="_blank" rel="noopener" className="hover:text-green-600">Twitter</a></li>
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
            © 2026 Axiom Technologies. All rights reserved. · Built by a solo dev from Seoul 🇰🇷
          </div>
        </div>
      </footer>
    </div>
  );
}
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ about/page.tsx patched — false claims removed, solo founder story added")
