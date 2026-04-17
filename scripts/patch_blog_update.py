import os

# ── 1. uptimerobot-alternatives 수정 (3 monitors → 10 monitors) ──────────────
FILE1 = r"C:\home\jeon\api-health-monitor\frontend\app\blog\uptimerobot-alternatives\page.tsx"

with open(FILE1, 'r', encoding='utf-8') as f:
    c = f.read()

# 비교표 및 본문의 "3" monitors 수정
c = c.replace('Free monitors: 3', 'Free monitors: 10')
c = c.replace('>3<', '>10<')
c = c.replace('"free_monitors": 3', '"free_monitors": 10')

# 비교표 텍스트 수정 (다양한 형태로 있을 수 있음)
import re
# "CheckAPI← This site | 3 | ..." 패턴
c = re.sub(r'(CheckAPI[^|]*\|)\s*3\s*(\|)', r'\g<1> 10 \g<2>', c)

with open(FILE1, 'w', encoding='utf-8') as f:
    f.write(c)

print("uptimerobot-alternatives fixed!")
print("10 monitors:", "10" in c)


# ── 2. 블로그 페이지 목록 업데이트 ───────────────────────────────────────────
BLOG_INDEX = r"C:\home\jeon\api-health-monitor\frontend\app\blog\page.tsx"

with open(BLOG_INDEX, 'r', encoding='utf-8') as f:
    blog_index = f.read()

# 새 글 목록 추가 (기존 글 목록 뒤에)
new_posts = '''            {/* New posts */}
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
            </article>'''

# 기존 마지막 article 닫는 태그 뒤에 삽입
old_marker = "            {/* Jan 28 post - Slack */}"
if old_marker not in blog_index:
    # 다른 방법으로 찾기
    old_marker2 = "Jan 28, 2026"
    if old_marker2 in blog_index:
        # Jan 28 글 블록 끝 찾기
        idx = blog_index.rfind('</article>', 0, blog_index.find('Start monitoring') )
        if idx > 0:
            blog_index = blog_index[:idx+10] + '\n' + new_posts + blog_index[idx+10:]
            print("Blog index updated via position!")
else:
    print("marker found")

with open(BLOG_INDEX, 'w', encoding='utf-8') as f:
    f.write(blog_index)


# ── 3. silent-api-failures 글 생성 ───────────────────────────────────────────
dir1 = r"C:\home\jeon\api-health-monitor\frontend\app\blog\silent-api-failures"
os.makedirs(dir1, exist_ok=True)

post1 = r"""import PublicAuthButtons from '@/components/PublicAuthButtons';
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
"""

with open(os.path.join(dir1, "page.tsx"), 'w', encoding='utf-8') as f:
    f.write(post1)
print("silent-api-failures created!")


# ── 4. api-monitoring-checklist 글 생성 ──────────────────────────────────────
dir2 = r"C:\home\jeon\api-health-monitor\frontend\app\blog\api-monitoring-checklist"
os.makedirs(dir2, exist_ok=True)

post2 = r"""import PublicAuthButtons from '@/components/PublicAuthButtons';
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
"""

with open(os.path.join(dir2, "page.tsx"), 'w', encoding='utf-8') as f:
    f.write(post2)
print("api-monitoring-checklist created!")


# ── 5. public-status-page 글 생성 ────────────────────────────────────────────
dir3 = r"C:\home\jeon\api-health-monitor\frontend\app\blog\public-status-page"
os.makedirs(dir3, exist_ok=True)

post3 = r"""import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';
import { ArrowRight, Calendar, Clock } from 'lucide-react';

export const metadata = {
  title: 'How to Set Up a Free Public Status Page for Your API | CheckAPI',
  description: 'A public status page reduces support tickets, builds user trust, and takes 2 minutes to set up. Here\'s how to do it for free with CheckAPI.',
};

export default function BlogPostStatusPage() {
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

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">How to Set It Up with CheckAPI</h2>

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

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">What the Status Page Shows</h2>
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

          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-10">Where to Link Your Status Page</h2>
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
"""

with open(os.path.join(dir3, "page.tsx"), 'w', encoding='utf-8') as f:
    f.write(post3)
print("public-status-page created!")
print("\nAll done!")
