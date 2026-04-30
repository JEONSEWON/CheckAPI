import Link from 'next/link';
import PublicAuthButtons from '@/components/PublicAuthButtons';
import { ArrowLeft, ArrowRight } from 'lucide-react';

export const metadata = {
  title: 'JSON Path Assertions: Validate Nested API Responses – CheckAPI',
  description: 'Go beyond status codes. Use JSON Path assertions to validate specific fields inside your API response — catch null data, wrong values, and broken logic automatically.',
};

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is a JSON Path assertion?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'A JSON Path assertion is a rule that points to a specific field inside a JSON response body and validates its value. Instead of scanning the entire body for a pattern (regex), you target exactly the field you care about using a path like $.data.status.',
      },
    },
    {
      '@type': 'Question',
      name: 'Which operators does CheckAPI support for JSON Path assertions?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'CheckAPI supports 11 operators: == (exact match), != (must not equal), > >= < <= (numeric ranges), contains (string contains substring), not_contains (must not contain), is_null (field must be null), is_not_null (field must not be null), and exists (field key must exist).',
      },
    },
    {
      '@type': 'Question',
      name: 'Should you use AND or OR logic for JSON Path assertions?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'By default, all assertions use AND logic — every assertion must pass for the check to be green. You can switch individual assertions to OR logic, which means the check passes if at least one assertion is true.',
      },
    },
    {
      '@type': 'Question',
      name: 'How many JSON Path assertions can you set per monitor?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'CheckAPI supports up to 10 JSON Path assertions per monitor. This is enough to comprehensively validate the critical fields of any API response in a single check — no code required.',
      },
    },
    {
      '@type': 'Question',
      name: 'Can you combine JSON Path assertions with regex?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. A common pattern is to use Regex for a quick top-level sanity check (e.g. error field is null) and JSON Path for precise field-level validation (e.g. balance is positive, user_id exists). Both run on every check.',
      },
    },
  ],
};

export default function JsonPathAssertionsPost() {
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
          <span>Apr 22, 2026</span>
          <span>·</span>
          <span>5 min read</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
          JSON Path Assertions: Validate Nested API Responses
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-10 leading-relaxed">
          Your API returns 200 OK. The body looks like JSON. But is <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded text-lg">$.data.user_id</code> actually populated? Is the balance positive? Is the error field null? JSON Path assertions tell you.
        </p>

        <div className="prose prose-lg dark:prose-invert max-w-none space-y-8 text-gray-700 dark:text-gray-300">

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What is a JSON Path assertion?</h2>
          <p>
            A JSON Path assertion is a rule that points to a specific field inside a JSON response body and validates its value. Instead of scanning the entire body for a pattern (regex), you target exactly the field you care about.
          </p>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-5 text-sm overflow-x-auto leading-relaxed">{`// Response:
{
  "status": "ok",
  "data": {
    "user_id": 42,
    "balance": 1500,
    "plan": "pro"
  },
  "error": null
}

// Assertions:
$.status          ==       "ok"       ✓ passes
$.data.balance    >=       100        ✓ passes
$.error           is_null             ✓ passes
$.data.plan       ==       "free"     ✗ fails → alert fires`}</pre>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Which Operators Does CheckAPI Support for JSON Path Assertions?</h2>
          <p>CheckAPI supports 11 operators for JSON Path assertions:</p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Operator</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Use case</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700 text-sm">
                {[
                  ['==', 'Exact match — status must be "ok"'],
                  ['!=', 'Must not equal — code must not be 0'],
                  ['>', '>= < <=', 'Numeric ranges — balance must be > 0'],
                  ['contains', 'String contains a substring'],
                  ['not_contains', 'String must not contain a substring'],
                  ['is_null', 'Field must be null'],
                  ['is_not_null', 'Field must not be null — data must be populated'],
                  ['exists', 'Field key must exist in the response'],
                ].map(([op, desc]) => (
                  <tr key={op} className="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900 dark:even:bg-gray-800">
                    <td className="px-4 py-2 font-mono text-green-700 dark:text-green-400">{op}</td>
                    <td className="px-4 py-2">{desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">What Are Real-World JSON Path Assertion Examples?</h2>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Health check endpoint</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`// GET /health
{
  "status": "ok",
  "db": "connected",
  "cache": "connected",
  "version": "2.4.1"
}

// Assertions:
$.status    ==           "ok"
$.db        ==           "connected"
$.cache     ==           "connected"
$.version   is_not_null`}</pre>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Payment API</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`// POST /payments/process
{
  "success": true,
  "transaction_id": "txn_abc123",
  "amount_charged": 4999,
  "error": null
}

// Assertions:
$.success           ==         true
$.transaction_id    exists
$.amount_charged    >          0
$.error             is_null`}</pre>

          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">List endpoint (data must not be empty)</h3>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`// GET /api/products
{
  "data": [...],
  "total": 142,
  "page": 1
}

// Assertions:
$.total     >     0
$.data      is_not_null`}</pre>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Should You Use AND or OR Logic for JSON Path Assertions?</h2>
          <p>
            By default, all assertions are evaluated with AND logic — every assertion must pass for the check to be green. You can switch individual assertions to OR in the Assertions tab, which means the check passes if at least one assertion is true.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How Many JSON Path Assertions Can You Set Per Monitor?</h2>
          <p>
            CheckAPI supports up to 10 JSON Path assertions per monitor. This is enough to comprehensively validate the critical fields of any API response in a single check — no code required.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Can You Combine JSON Path Assertions with Regex?</h2>
          <p>
            JSON Path and Regex aren't mutually exclusive. A common pattern is to use Regex for a quick top-level sanity check (e.g. error field is null) and JSON Path for precise field-level validation (e.g. balance is positive, user_id exists). Both run on every check.
          </p>

          <div className="bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-xl p-6">
            <h3 className="font-bold text-gray-900 dark:text-white mb-2">Set up JSON Path assertions</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Available on all plans including Free. Create your first monitor with JSON Path assertions in under 2 minutes.
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
