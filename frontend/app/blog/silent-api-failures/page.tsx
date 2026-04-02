import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock } from 'lucide-react';

export const metadata = {
  title: 'What is a Silent API Failure? (And How to Detect It) | CheckAPI',
  description: 'Your API returns 200 OK but the response body is broken or empty. This is a silent failure — and most monitoring tools miss it. Here\'s how to catch it.',
};

export default function BlogPostSilentFailure() {
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
          <span className="flex items-center gap-1"><Calendar className="h-4 w-4" />Mar 15, 2026</span>
          <span className="flex items-center gap-1"><Clock className="h-4 w-4" />5 min read</span>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
          What is a Silent API Failure? (And How to Detect It)
        </h1>

        <div className="prose prose-lg max-w-none text-gray-700 dark:text-gray-200 space-y-6">
          <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
            Your API returns <code className="bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded text-green-600 font-mono">200 OK</code>. Your monitoring tool says everything is fine. But your users are getting empty data, error messages, or broken responses. This is a <strong>silent failure</strong> — and it's one of the hardest bugs to catch.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">What Makes a Failure "Silent"?</h2>
          <p>
            A traditional API failure is obvious: the server returns a 500, a 404, or times out. Your monitoring tool catches it immediately and fires an alert.
          </p>
          <p>
            A silent failure is different. The server responds successfully at the HTTP level — status 200, fast response time — but the actual content of the response is wrong. Examples:
          </p>
          <ul className="space-y-2 list-none pl-0">
            {[
              'Your payment API returns 200 OK with {"error": "insufficient_funds"} in the body',
              'Your data API returns 200 OK with an empty array [] instead of actual data',
              'Your auth API returns 200 OK but the token field is null',
              'A third-party API you depend on returns 200 OK with a deprecation notice instead of data',
            ].map((item, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-orange-500 mt-1 flex-shrink-0">⚠️</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <p>
            In every case, your standard uptime monitor would report the API as "up" — because technically, it is. The HTTP handshake succeeded. But your users are experiencing real failures.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">Why Most Monitoring Tools Miss This</h2>
          <p>
            Most uptime monitors work by checking two things: did the server respond, and what was the HTTP status code? If both look good, the check passes.
          </p>
          <p>
            This made sense in the early web, when a 200 response reliably meant the page loaded correctly. Modern APIs are different. A 200 response just means the request was received and processed — not that the result is correct.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">How to Detect Silent Failures</h2>
          <p>There are three levels of response body validation, from simple to advanced:</p>

          <div className="space-y-4">
            <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-5 bg-white dark:bg-gray-800">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">1. Keyword Check</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Check if a specific string is present or absent in the response body.</p>
              <code className="block mt-2 bg-gray-100 dark:bg-gray-700 px-3 py-2 rounded text-sm font-mono text-gray-800 dark:text-gray-200">
                Keyword: "status" must be present<br />
                Fails if: body does not contain "status"
              </code>
            </div>
            <div className="border border-orange-200 dark:border-orange-800 rounded-xl p-5 bg-orange-50 dark:bg-orange-950">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">2. Regex Pattern ⚡ More powerful</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Use a regular expression to validate the response body with precision.</p>
              <code className="block mt-2 bg-white dark:bg-gray-800 px-3 py-2 rounded text-sm font-mono text-gray-800 dark:text-gray-200">
                Pattern: "status":\s*"ok"<br />
                Matches: {'"status": "ok"'} and {'"status":"ok"'}
              </code>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">Real-World Examples</h2>

          <div className="space-y-4">
            <div className="border-l-4 border-green-500 pl-4">
              <p className="font-semibold text-gray-900 dark:text-white">Payment API</p>
              <p className="text-sm text-gray-600 dark:text-gray-300">Regex: <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">"status":\s*"success"</code> — Fails if payment processing is broken even though the endpoint responds.</p>
            </div>
            <div className="border-l-4 border-green-500 pl-4">
              <p className="font-semibold text-gray-900 dark:text-white">Data API</p>
              <p className="text-sm text-gray-600 dark:text-gray-300">Keyword: <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">"data"</code> must be present — Fails if response is empty or error-only.</p>
            </div>
            <div className="border-l-4 border-green-500 pl-4">
              <p className="font-semibold text-gray-900 dark:text-white">Auth API</p>
              <p className="text-sm text-gray-600 dark:text-gray-300">Keyword: <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">"error"</code> must be absent — Fails if any error appears in the response.</p>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">How CheckAPI Handles This</h2>
          <p>
            CheckAPI's Silent Failure Detection runs after the HTTP status check. If your API returns 200 OK, CheckAPI then validates the response body against your keyword or regex pattern. If the validation fails, the monitor is marked as <strong>degraded</strong> — not "up" — and your alert channels fire immediately.
          </p>
          <p>
            This is the core reason CheckAPI exists. Standard uptime monitors are a solved problem. Silent failure detection isn't — and it's where real incidents hide.
          </p>
        </div>

        <div className="mt-12 p-6 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-xl">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Start catching silent failures today</h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm">Free plan includes keyword and regex validation. No credit card required.</p>
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
