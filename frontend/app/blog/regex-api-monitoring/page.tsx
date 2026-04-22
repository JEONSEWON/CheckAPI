import Link from 'next/link';
import PublicAuthButtons from '@/components/PublicAuthButtons';
import { ArrowLeft, ArrowRight } from 'lucide-react';

export const metadata = {
  title: 'How to Use Regex to Monitor API Response Bodies – CheckAPI',
  description: 'HTTP status codes only tell half the story. Learn how to use regex patterns to validate API response bodies and catch silent failures before your users do.',
};

export default function RegexApiMonitoringPost() {
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
              <a href="/pricing" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Pricing</a>
              <Link href="/docs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Docs</Link>
              <Link href="/blog" className="text-green-600 font-medium transition">Blog</Link>
            </nav>
            <div className="flex items-center space-x-4"><PublicAuthButtons /></div>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-24">
        <Link href="/blog" className="inline-flex items-center text-sm text-gray-500 hover:text-green-600 mb-8 transition">
          <ArrowLeft className="h-4 w-4 mr-1" /> Back to Blog
        </Link>

        <div className="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400 mb-4">
          <span>Apr 15, 2026</span>
          <span>·</span>
          <span>6 min read</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
          How to Use Regex to Monitor API Response Bodies
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-10 leading-relaxed">
          HTTP status codes only tell half the story. A 200 OK means the request completed — not that the response is correct. Here's how regex pattern matching closes that gap.
        </p>

        <div className="prose prose-lg dark:prose-invert max-w-none space-y-8 text-gray-700 dark:text-gray-300">

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">The problem with status-only monitoring</h2>
          <p>
            Most API monitoring tools check exactly one thing: did the server respond with a 200? If yes, the monitor turns green and everyone moves on. But HTTP status codes are a terrible proxy for API health.
          </p>
          <p>Consider this scenario:</p>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-5 text-sm overflow-x-auto leading-relaxed">{`// HTTP 200 OK — your monitor says "UP" ✓
{
  "status": "ok",
  "data": null,
  "error": "DB_CONN_FAILED"
}`}</pre>
          <p>
            Your database connection failed. Your API is returning broken data wrapped in a polite 200 OK. Standard monitors miss this entirely. Your users find out first.
          </p>
          <p>
            This is called a <strong>silent failure</strong> — and regex monitoring is the most effective way to catch them.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What is regex body validation?</h2>
          <p>
            Instead of stopping at the status code, regex validation runs a regular expression pattern against the actual response body text. If the pattern doesn't match (or does match, depending on your rule), the check is marked as <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">degraded</code> and your alert fires.
          </p>
          <p>
            In CheckAPI, enable the <strong>Use Regex</strong> toggle when creating or editing a monitor. Then write your pattern.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Practical regex patterns</h2>
          <p>Here are real-world patterns you can use today:</p>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">1. Status field must be "ok" or "healthy"</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`"status":\s*"(ok|healthy)"`}</pre>
          <p className="text-sm text-gray-600 dark:text-gray-400">Fails if the status field contains any other value — including "error", "degraded", or null.</p>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">2. Error field must be null</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`"error":\s*null`}</pre>
          <p className="text-sm text-gray-600 dark:text-gray-400">Catches APIs that return error strings in the error field while still returning 200.</p>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">3. Data array must not be empty</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`"data":\s*\[[^\]]+\]`}</pre>
          <p className="text-sm text-gray-600 dark:text-gray-400">Fails if <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">data</code> is an empty array. Useful for APIs that should always return at least one result.</p>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">4. Balance is a positive number</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`"balance":\s*[1-9][0-9]*`}</pre>
          <p className="text-sm text-gray-600 dark:text-gray-400">For payment or wallet APIs — validates the balance field is a positive integer.</p>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">5. No database error string anywhere in body</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`^(?!.*DB_CONN_FAILED).*$`}</pre>
          <p className="text-sm text-gray-600 dark:text-gray-400">Negative lookahead — the entire response body must not contain the string <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">DB_CONN_FAILED</code>.</p>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">6. Version field exists and is not empty</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`"version":\s*"[^"]+"`}</pre>
          <p className="text-sm text-gray-600 dark:text-gray-400">Verifies the version field is a non-empty string — useful for health check endpoints.</p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Testing patterns before you save</h2>
          <p>
            CheckAPI has a built-in <strong>Test Regex</strong> button. Paste a sample response body and your pattern — it shows you immediately whether the pattern matches before the monitor goes live. No more regex typos silently making your monitor worthless.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">When to use regex vs JSON Path assertions</h2>
          <p>
            Regex is flexible and fast to write. JSON Path assertions are more precise for deeply nested JSON fields. A good rule of thumb:
          </p>
          <ul className="list-disc list-inside space-y-1">
            <li>Use <strong>regex</strong> for simple string patterns, error detection, and format validation</li>
            <li>Use <strong>JSON Path</strong> for specific field values, numeric comparisons, and null checks on nested fields</li>
            <li>Combine both for maximum coverage</li>
          </ul>

          <div className="bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-xl p-6">
            <h3 className="font-bold text-gray-900 dark:text-white mb-2">Try it in CheckAPI</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Regex validation is available on all plans including Free. Set up your first regex monitor in under 2 minutes.
            </p>
            <Link href="/register" className="inline-flex items-center bg-green-600 text-white px-5 py-2 rounded-lg hover:bg-green-700 transition font-medium">
              Start for Free <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>
      </main>

      <footer className="border-t bg-white dark:bg-gray-900 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
          © 2026 Axiom Technologies. All rights reserved. ·{' '}
          <Link href="/blog" className="hover:text-green-600">Back to Blog</Link>
        </div>
      </footer>
    </div>
  );
}
