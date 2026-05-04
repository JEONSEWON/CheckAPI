import PublicAuthButtons from '@/components/PublicAuthButtons';
import Link from 'next/link';

export const metadata = {
  title: 'Documentation – CheckAPI',
  description: 'Complete documentation for CheckAPI — Silent Failure Detection, Regex patterns, JSON Path assertions, Heartbeat monitoring, and more.',
};

const sections = [
  {
    id: 'getting-started',
    title: 'Getting Started',
    items: [
      { id: 'quick-start', label: 'Quick Start' },
      { id: 'create-monitor', label: 'Create Your First Monitor' },
    ],
  },
  {
    id: 'silent-failure',
    title: 'Silent Failure Detection',
    items: [
      { id: 'keyword-validation', label: 'Keyword Validation' },
      { id: 'regex-matching', label: 'Regex Pattern Matching' },
      { id: 'json-path', label: 'JSON Path Assertions' },
      { id: 'header-assertion', label: 'Header Assertions' },
    ],
  },
  {
    id: 'monitors',
    title: 'Monitors',
    items: [
      { id: 'monitor-config', label: 'Monitor Configuration' },
      { id: 'http-methods', label: 'HTTP Methods' },
      { id: 'check-intervals', label: 'Check Intervals' },
      { id: 'alert-threshold', label: 'Alert Threshold' },
      { id: 'ssl-monitoring', label: 'SSL Certificate Monitoring' },
    ],
  },
  {
    id: 'heartbeat',
    title: 'Heartbeat Monitoring',
    items: [
      { id: 'heartbeat-overview', label: 'How It Works' },
      { id: 'heartbeat-setup', label: 'Setting Up Heartbeats' },
    ],
  },
  {
    id: 'alerts',
    title: 'Alert Channels',
    items: [
      { id: 'email', label: 'Email' },
      { id: 'slack', label: 'Slack' },
      { id: 'telegram', label: 'Telegram' },
      { id: 'discord', label: 'Discord' },
      { id: 'webhook', label: 'Custom Webhook' },
    ],
  },
  {
    id: 'advanced',
    title: 'Advanced Features',
    items: [
      { id: 'maintenance-windows', label: 'Maintenance Windows' },
      { id: 'status-page', label: 'Public Status Page' },
      { id: 'status-badge', label: 'Status Badge' },
      { id: 'team-management', label: 'Team Management' },
      { id: 'sla-reports', label: 'SLA Reports' },
      { id: 'api-keys', label: 'REST API & API Keys' },
    ],
  },
  {
    id: 'ai-features',
    title: 'AI Features',
    items: [
      { id: 'ai-incident-analysis', label: 'AI Incident Analysis' },
      { id: 'ai-auto-detect', label: 'AI Auto-detect' },
    ],
  },
  {
    id: 'plans',
    title: 'Plans & Limits',
    items: [
      { id: 'free-plan', label: 'Free Plan' },
      { id: 'paid-plans', label: 'Paid Plans' },
      { id: 'data-retention', label: 'Data Retention' },
    ],
  },
];

export default function DocsPage() {
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
              <Link href="/docs" className="text-green-600 font-medium transition">Docs</Link>
              <Link href="/blog" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Blog</Link>
            </nav>
            <div className="flex items-center space-x-4">
              <PublicAuthButtons />
            </div>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-8 text-center">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
          <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            Documentation
          </span>
        </h1>
        <p className="text-gray-500 dark:text-gray-400 text-lg">Everything you need to monitor your APIs with CheckAPI.</p>
      </section>

      {/* Main Layout */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24 flex gap-10">

        {/* Sidebar */}
        <aside className="hidden lg:block w-56 shrink-0">
          <div className="sticky top-24 space-y-6 max-h-[calc(100vh-7rem)] overflow-y-auto pr-2">
            {sections.map((section) => (
              <div key={section.id}>
                <p className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">{section.title}</p>
                <ul className="space-y-1">
                  {section.items.map((item) => (
                    <li key={item.id}>
                      <a href={`#${item.id}`} className="text-sm text-gray-600 dark:text-gray-400 hover:text-green-600 transition block py-0.5">
                        {item.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </aside>

        {/* Content */}
        <main className="flex-1 max-w-3xl space-y-20 text-gray-600 dark:text-gray-400 leading-relaxed">

          {/* ── Getting Started ── */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">Getting Started</h2>

            <div id="quick-start" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Quick Start</h3>
              <p className="mb-4">CheckAPI monitors your API endpoints 24/7 and alerts you the moment something goes wrong. You can be up and running in under 2 minutes.</p>
              <ol className="list-decimal list-inside space-y-2">
                <li>Create a free account at <Link href="/register" className="text-green-600 hover:text-green-700">checkapi.io/register</Link></li>
                <li>Click <strong className="text-gray-800 dark:text-gray-200">Add Monitor</strong> from your dashboard</li>
                <li>Enter your API endpoint URL and configure check settings</li>
                <li>Add at least one alert channel (Email, Slack, Discord, etc.)</li>
                <li>Save — monitoring starts immediately</li>
              </ol>
            </div>

            <div id="create-monitor">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Create Your First Monitor</h3>
              <p className="mb-4">From your dashboard, click <strong className="text-gray-800 dark:text-gray-200">+ Add Monitor</strong>. Fill in:</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 space-y-3 text-sm">
                {[
                  ['Name', 'A friendly label (e.g. "Production API")'],
                  ['URL', 'Full endpoint URL including protocol (e.g. https://api.example.com/health)'],
                  ['Method', 'HTTP method: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS'],
                  ['Interval', 'How often to check — depends on your plan'],
                  ['Expected Status', 'Expected HTTP response code (default: 200)'],
                  ['Request Headers', 'Optional custom headers (e.g. Authorization, Content-Type)'],
                  ['Request Body', 'Optional JSON body for POST/PUT/PATCH requests'],
                ].map(([label, desc]) => (
                  <div key={label} className="flex gap-3">
                    <span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">{label}</span>
                    <span>{desc}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* ── Silent Failure Detection ── */}
          <section>
            <div className="flex items-center gap-3 mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Silent Failure Detection</h2>
              <span className="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 text-xs font-semibold rounded-full">Core Feature</span>
            </div>
            <p className="mb-8 text-gray-600 dark:text-gray-400">
              HTTP status codes only tell you whether a request completed — not whether the response is actually correct. CheckAPI validates the response body itself, catching errors your API silently hides behind a <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">200 OK</code>.
            </p>

            <div id="keyword-validation" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Keyword Validation</h3>
              <p className="mb-4">Specify a string that must be <strong className="text-gray-800 dark:text-gray-200">present</strong> or <strong className="text-gray-800 dark:text-gray-200">absent</strong> in the response body.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 space-y-3 text-sm mb-4">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-24 shrink-0">Present</span><span>Check fails if keyword is NOT found in the response body</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-24 shrink-0">Absent</span><span>Check fails if keyword IS found in the response body</span></div>
              </div>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`# Keyword present example
keyword: "status":"ok"   → fails if "status":"ok" not in body

# Keyword absent example  
keyword: "error"         → fails if "error" appears in body`}</pre>
            </div>

            <div id="regex-matching" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Regex Pattern Matching</h3>
              <p className="mb-4">
                Enable the <strong className="text-gray-800 dark:text-gray-200">Use Regex</strong> toggle to validate the response body against a regular expression pattern. Regex gives you far more power than simple keyword matching — test field values, formats, ranges, and more.
              </p>
              <div className="bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 text-sm text-yellow-800 dark:text-yellow-200 mb-4">
                <strong>Tip:</strong> Use the <strong>Test Regex</strong> button in the monitor form to preview your pattern against a sample response before saving.
              </div>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`# status field must be "ok" or "healthy"
"status":\s*"(ok|healthy)"

# balance must be a positive number
"balance":\s*[1-9][0-9]*

# error field must be null
"error":\s*null

# version field exists and is not empty
"version":\s*"[^"]+"

# data array must not be empty
"data":\s*\[[^\]]+\]

# No database error string in body
^(?!.*DB_CONN_FAILED).*$`}</pre>
              <p className="mt-4 text-sm">CheckAPI uses Python-compatible regex (re module). Standard regex syntax applies.</p>
            </div>

            <div id="json-path" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">JSON Path Assertions</h3>
              <p className="mb-4">
                Add up to <strong className="text-gray-800 dark:text-gray-200">10 JSON Path assertions</strong> per monitor. Each assertion targets a specific field in the response JSON and validates it against an expected value using an operator.
              </p>

              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-2 mt-6">Supported Operators</h4>
              <div className="overflow-x-auto mb-6">
                <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Operator</th>
                      <th className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">Description</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {[
                      ['==', 'Exact equality'],
                      ['!=', 'Not equal'],
                      ['>', 'Greater than (numeric)'],
                      ['>=', 'Greater than or equal'],
                      ['<', 'Less than (numeric)'],
                      ['<=', 'Less than or equal'],
                      ['contains', 'String contains value'],
                      ['not_contains', 'String does not contain value'],
                      ['is_null', 'Field value is null'],
                      ['is_not_null', 'Field value is not null'],
                      ['exists', 'Field key exists in response'],
                    ].map(([op, desc]) => (
                      <tr key={op} className="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900 dark:even:bg-gray-800">
                        <td className="px-4 py-2 font-mono text-green-700 dark:text-green-400">{op}</td>
                        <td className="px-4 py-2">{desc}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Examples</h4>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`# Response JSON:
{
  "status": "ok",
  "data": { "user_id": 42, "balance": 1500 },
  "error": null
}

# Assertions:
$.status          ==          "ok"
$.data.balance    >=          100
$.error           is_null
$.data.user_id    exists`}</pre>

              <div className="mt-4 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-4 text-sm text-blue-800 dark:text-blue-200">
                <strong>AND / OR Logic:</strong> Multiple assertions default to AND (all must pass). You can switch individual assertions to OR logic in the Assertions tab of the monitor detail page.
              </div>
            </div>

            <div id="header-assertion" className="mb-4">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Header Assertions</h3>
              <p className="mb-4">Validate response headers alongside body content. Useful for checking <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">Content-Type</code>, cache headers, rate-limit headers, or any custom header your API returns.</p>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`# Assert Content-Type is JSON
Header: Content-Type   contains   application/json

# Assert cache header exists
Header: Cache-Control  exists

# Assert custom auth header value
Header: X-Auth-Status  ==   "valid"`}</pre>
            </div>
          </section>

          {/* ── Monitors ── */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">Monitors</h2>

            <div id="monitor-config" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Monitor Configuration</h3>
              <p>Each monitor sends HTTP requests to your endpoint on a schedule and records the result — status code, response time, response body, and headers. If a check fails (wrong status code, failed assertion, timeout), CheckAPI triggers your configured alert channels.</p>
            </div>

            <div id="http-methods" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">HTTP Methods</h3>
              <p className="mb-4">All standard HTTP methods are supported so you can simulate real API requests, not just simple GET pings:</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'].map((m) => (
                  <span key={m} className="px-3 py-1 bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 rounded-full text-sm font-mono font-medium border border-green-200 dark:border-green-800">{m}</span>
                ))}
              </div>
              <p className="text-sm">For POST, PUT, and PATCH — you can include a JSON request body and custom headers to authenticate and simulate real usage.</p>
            </div>

            <div id="check-intervals" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Check Intervals</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      {['Plan', 'Interval', 'Monitors', 'History'].map((h) => (
                        <th key={h} className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {[
                      ['Free', '5 minutes', '10', '30 days'],
                      ['Starter', '1 minute', '20', '30 days'],
                      ['Pro', '30 seconds', '100', '90 days'],
                      ['Business', '10 seconds', 'Unlimited', '365 days'],
                    ].map(([plan, interval, monitors, history], i) => (
                      <tr key={plan} className={i % 2 === 0 ? 'bg-white dark:bg-gray-900' : 'bg-gray-50 dark:bg-gray-800'}>
                        <td className="px-4 py-3 font-medium text-gray-800 dark:text-gray-200">{plan}</td>
                        <td className="px-4 py-3">{interval}</td>
                        <td className="px-4 py-3">{monitors}</td>
                        <td className="px-4 py-3">{history}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div id="alert-threshold" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Alert Threshold</h3>
              <p className="mb-4">
                By default, CheckAPI sends an alert after the <strong className="text-gray-800 dark:text-gray-200">first failed check</strong>. You can increase the threshold to require N consecutive failures before alerting — useful for flaky endpoints that occasionally fail without being truly down.
              </p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">Range</span><span>1 – 10 consecutive failures</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">Default</span><span>1 (alert on first failure)</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">Recovery</span><span>Recovery alerts (→ up) are always sent immediately, regardless of threshold</span></div>
              </div>
            </div>

            <div id="ssl-monitoring">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">SSL Certificate Monitoring</h3>
              <p className="mb-4">CheckAPI automatically monitors SSL certificate expiry for all HTTPS monitors. You'll receive an alert before your certificate expires so you never get caught with a broken HTTPS site.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Check frequency</span><span>Daily at 9:00 AM UTC</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Default alert</span><span>14 days before expiry</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Configurable</span><span>Set your preferred days-before threshold per monitor</span></div>
              </div>
            </div>
          </section>

          {/* ── Heartbeat ── */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">Heartbeat Monitoring</h2>

            <div id="heartbeat-overview" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">How It Works</h3>
              <p className="mb-4">
                Heartbeat monitors work in reverse — instead of CheckAPI pinging your endpoint, <strong className="text-gray-800 dark:text-gray-200">your service pings CheckAPI</strong>. If CheckAPI doesn't receive a ping within the expected interval plus a grace period, it fires an alert.
              </p>
              <p>This is ideal for monitoring cron jobs, scheduled tasks, background workers, and any process that runs on a timer.</p>
            </div>

            <div id="heartbeat-setup">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Setting Up Heartbeats</h3>
              <ol className="list-decimal list-inside space-y-2 mb-6">
                <li>Create a new monitor and select <strong className="text-gray-800 dark:text-gray-200">Heartbeat</strong> as the type</li>
                <li>Set the expected interval (e.g. every 60 minutes) and grace period</li>
                <li>Copy the unique heartbeat URL</li>
                <li>Call that URL from your cron job or scheduled task after it completes</li>
              </ol>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`# Call the heartbeat URL after your cron job succeeds
# GET or POST both work

curl https://checkapi.io/heartbeat/<your-token>

# Example: add to end of cron job script
python my_scheduled_job.py && curl -s https://checkapi.io/heartbeat/<your-token>

# Or in Python
import requests
requests.get("https://checkapi.io/heartbeat/<your-token>")`}</pre>
              <p className="mt-4 text-sm">
                CheckAPI checks heartbeats every minute. If your job hasn't pinged within <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">interval + grace period</code> minutes, the monitor goes down and your alert channels are notified.
              </p>
            </div>
          </section>

          {/* ── Alert Channels ── */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">Alert Channels</h2>
            <p className="mb-8">CheckAPI supports 5 alert channels. All channels are available on every plan including Free. You can connect multiple channels per account and test each one before going live with the <strong className="text-gray-800 dark:text-gray-200">Test</strong> button.</p>

            <div id="email" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Email</h3>
              <p>Enter your email address. CheckAPI will send HTML-formatted alerts whenever a monitor goes down or recovers.</p>
            </div>

            <div id="slack" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Slack</h3>
              <p className="mb-3">Uses Slack Incoming Webhooks. No bot setup required.</p>
              <ol className="list-decimal list-inside space-y-1 text-sm">
                <li>Go to your Slack workspace → <strong>Apps</strong> → search "Incoming Webhooks"</li>
                <li>Add it to a channel and copy the Webhook URL</li>
                <li>Paste the URL (starts with <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">https://hooks.slack.com/...</code>) into CheckAPI</li>
              </ol>
            </div>

            <div id="telegram" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Telegram</h3>
              <p className="mb-3">Requires a Bot Token and a Chat ID.</p>
              <ol className="list-decimal list-inside space-y-1 text-sm">
                <li>Message <strong>@BotFather</strong> on Telegram → create a new bot → copy the token</li>
                <li>Start a chat with your bot, then visit <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded text-xs">https://api.telegram.org/bot&lt;token&gt;/getUpdates</code> to get your Chat ID</li>
                <li>Enter both values in CheckAPI</li>
              </ol>
            </div>

            <div id="discord" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Discord</h3>
              <p className="mb-3">Uses Discord channel webhooks.</p>
              <ol className="list-decimal list-inside space-y-1 text-sm">
                <li>Go to your Discord server → channel Settings → Integrations → Webhooks</li>
                <li>Create a new webhook and copy the URL</li>
                <li>Paste the URL (starts with <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">https://discord.com/api/webhooks/...</code>) into CheckAPI</li>
              </ol>
            </div>

            <div id="webhook">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Custom Webhook</h3>
              <p className="mb-4">CheckAPI sends a POST request to your URL on every status change. You can also add custom headers (e.g. for authentication).</p>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`// POST payload:
{
  "event": "status_changed",
  "monitor": {
    "id": "abc123",
    "name": "Production API",
    "url": "https://api.example.com/health"
  },
  "status": {
    "old": "up",
    "new": "down"
  },
  "timestamp": "2026-04-22T10:00:00Z"
}`}</pre>
            </div>
          </section>

          {/* ── Advanced Features ── */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">Advanced Features</h2>

            <div id="maintenance-windows" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Maintenance Windows</h3>
              <p className="mb-4">Schedule maintenance windows to suppress alerts during planned downtime. Checks continue running (so you get data), but no alerts are sent during the window.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">Repeat types</span><span>Once, Daily, Weekly, Monthly</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">Timezone</span><span>Full timezone support including Asia/Seoul, UTC, and major cities</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">Scope</span><span>Apply to specific monitors or all monitors</span></div>
              </div>
            </div>

            <div id="status-page" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Public Status Page</h3>
              <p className="mb-4">Every monitor gets a public status page — no login required. Share it with your users so they can check service status themselves instead of emailing you.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">URL format</span><span><code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">checkapi.io/status/&#123;monitor_id&#125;</code></span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Shows</span><span>24h / 7d / 30d uptime, 90-day daily status chart, last 7 days of incidents</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Auth required</span><span>None — fully public link</span></div>
              </div>
            </div>

            <div id="status-badge" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Status Badge</h3>
              <p className="mb-4">Embed a live status badge in your README or documentation. The badge updates automatically based on your monitor's current status.</p>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed">{`<!-- Markdown (for README) -->
![Status](https://checkapi.io/badge/{monitor_id})

<!-- HTML -->
<img src="https://checkapi.io/badge/{monitor_id}" alt="API Status" />

<!-- With link to status page -->
[![Status](https://checkapi.io/badge/{monitor_id})](https://checkapi.io/status/{monitor_id})`}</pre>
              <p className="mt-3 text-sm">Find your monitor ID in the monitor detail page URL or in Settings.</p>
            </div>

            <div id="team-management" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Team Management</h3>
              <p className="mb-4">Invite team members to view and manage your monitors. Available on Pro and Business plans.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2 mb-4">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Invite method</span><span>Email invitation with token-based acceptance link</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Team member access</span><span>Full read/write access to owner's monitors and analytics</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Pro plan</span><span>Up to 5 members</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Business plan</span><span>Unlimited members</span></div>
              </div>
              <ol className="list-decimal list-inside space-y-1 text-sm">
                <li>Go to <strong>Dashboard → Settings → Team</strong></li>
                <li>Enter your team member's email address and send the invitation</li>
                <li>They accept via the link in the invitation email</li>
                <li>They can now view and manage all your monitors</li>
              </ol>
            </div>

            <div id="sla-reports" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">SLA Reports</h3>
              <p className="mb-4">Generate monthly SLA reports for your monitors. Available on Pro and Business plans.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Report range</span><span>Select 1 to 12 months</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Per month shows</span><span>Uptime %, total downtime, number of incidents</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Access</span><span>Dashboard → Analytics → SLA Report tab</span></div>
              </div>
            </div>

            <div id="api-keys">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">REST API & API Keys</h3>
              <p className="mb-4">Business plan users get full REST API access to manage monitors programmatically — create, update, delete monitors, retrieve check history, and more.</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2 mb-4">
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Key format</span><span><code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">ck_live_...</code></span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Max keys</span><span>5 API keys per account</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Security</span><span>Keys are shown only once at creation. Stored as SHA-256 hash.</span></div>
                <div className="flex gap-3"><span className="font-semibold text-gray-800 dark:text-gray-200 w-40 shrink-0">Auth header</span><span><code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">X-API-Key: ck_live_...</code></span></div>
              </div>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto">{`curl https://api-health-monitor-production.up.railway.app/api/monitors \\
  -H "X-API-Key: ck_live_your_key_here"`}</pre>
              <p className="mt-3 text-sm">Generate API keys in Dashboard → Settings → API Keys.</p>
            </div>
          </section>

          {/* ── AI Features ── */}
          <section>
            <div className="flex items-center gap-3 mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">AI Features</h2>
              <span className="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 text-xs font-semibold rounded-full">New</span>
            </div>
            <p className="mb-8 text-gray-600 dark:text-gray-400">
              CheckAPI uses AI to help you understand incidents faster and set up monitors without manual configuration. Both features are available on all plans.
            </p>

            <div id="ai-incident-analysis" className="mb-12">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">AI Incident Analysis</h3>
              <p className="mb-4">
                When a monitor goes down, CheckAPI automatically runs an AI analysis on the failed check. The AI examines the response body, status code, headers, and your configured assertions to explain <strong className="text-gray-800 dark:text-gray-200">why the check failed</strong> and suggest what might have caused it.
              </p>

              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-2 mt-6">When it triggers</h4>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2 mb-6">
                {[
                  ['Status code mismatch', 'Your endpoint returned an unexpected HTTP status (e.g. 500, 503, 404)'],
                  ['Assertion failure', 'A keyword, regex, JSON Path, or header assertion did not pass'],
                  ['Timeout', 'The endpoint did not respond within the configured timeout window'],
                  ['Connection error', 'The endpoint was unreachable (DNS failure, refused connection, etc.)'],
                ].map(([trigger, desc]) => (
                  <div key={trigger} className="flex gap-3">
                    <span className="font-semibold text-gray-800 dark:text-gray-200 w-48 shrink-0">{trigger}</span>
                    <span>{desc}</span>
                  </div>
                ))}
              </div>

              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">How to read the analysis</h4>
              <p className="mb-4 text-sm">Open the monitor detail page and click any failed check in the incident history. The AI analysis panel appears below the raw response with three parts:</p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-3 mb-6">
                {[
                  ['Root cause', 'A plain-language explanation of what went wrong — e.g. "The error field contains DB_CONN_FAILED, indicating a database connection failure."'],
                  ['Impact', 'What this failure means for your users or system — e.g. "Users may be unable to log in or see stale data."'],
                  ['Suggested fix', 'Actionable recommendations to resolve the incident — e.g. "Check your database connection pool settings. This pattern typically occurs under high load."'],
                ].map(([label, desc]) => (
                  <div key={label} className="flex gap-3">
                    <span className="font-semibold text-gray-800 dark:text-gray-200 w-36 shrink-0">{label}</span>
                    <span>{desc}</span>
                  </div>
                ))}
              </div>

              <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-4 text-sm text-blue-800 dark:text-blue-200">
                <strong>Note:</strong> AI analysis is performed on the actual response body captured at the time of the failed check. If your endpoint returns sensitive data, be aware that the response is stored and processed. CheckAPI does not train on your data.
              </div>
            </div>

            <div id="ai-auto-detect" className="mb-4">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">AI Auto-detect</h3>
              <p className="mb-4">
                When creating a new monitor, click <strong className="text-gray-800 dark:text-gray-200">Auto-detect</strong> (the sparkle button next to the URL field). CheckAPI will call your endpoint, analyze the real response, and automatically suggest:
              </p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 text-sm space-y-2 mb-6">
                {[
                  ['HTTP method', 'GET vs POST detected from the endpoint behavior'],
                  ['Expected status', 'The status code your endpoint actually returns'],
                  ['JSON Path assertions', 'Up to 5 assertions based on the real response structure — e.g. $.status == "ok", $.error is_null'],
                  ['Keyword suggestion', 'A keyword that should always be present based on the response body'],
                ].map(([label, desc]) => (
                  <div key={label} className="flex gap-3">
                    <span className="font-semibold text-gray-800 dark:text-gray-200 w-44 shrink-0">{label}</span>
                    <span>{desc}</span>
                  </div>
                ))}
              </div>

              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Example</h4>
              <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm overflow-x-auto leading-relaxed mb-4">{`# Your endpoint returns:
{
  "status": "ok",
  "data": { "version": "1.4.2", "db": "connected" },
  "error": null
}

# AI Auto-detect suggests:
Method:           GET
Expected status:  200
Assertions:
  $.status        ==        "ok"
  $.error         is_null
  $.data.db       ==        "connected"
  $.data.version  exists`}</pre>

              <p className="text-sm mb-4">You can accept all suggestions with one click, or deselect individual assertions before saving. Auto-detect is a starting point — you can always add or edit assertions manually afterwards.</p>

              <div className="bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 text-sm text-yellow-800 dark:text-yellow-200">
                <strong>Tip:</strong> Auto-detect works best on JSON endpoints. For endpoints that require authentication, add your <code className="bg-yellow-100 dark:bg-yellow-900 px-1 rounded">Authorization</code> header first, then run Auto-detect — it will use that header when calling your endpoint.
              </div>
            </div>
          </section>

          {/* ── Plans ── */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 pb-3 border-b border-gray-200 dark:border-gray-700">Plans & Limits</h2>

            <div id="free-plan" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Free Plan</h3>
              <p>
                The free plan includes <strong className="text-gray-800 dark:text-gray-200">10 monitors</strong> with 5-minute check intervals, all 5 alert channels, and 30-day data retention — with <strong className="text-gray-800 dark:text-gray-200">no commercial-use restrictions</strong>. No credit card required. Most monitoring tools restrict their free tier to personal projects only. CheckAPI doesn't.
              </p>
            </div>

            <div id="paid-plans" className="mb-10">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Paid Plans</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      {['Plan', 'Price', 'Monitors', 'Interval', 'Team', 'API Access'].map((h) => (
                        <th key={h} className="text-left px-4 py-3 font-semibold text-gray-700 dark:text-gray-300">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {[
                      ['Free', '$0', '10', '5 min', '—', '—'],
                      ['Starter', '$5/mo', '20', '1 min', '—', '—'],
                      ['Pro', '$15/mo', '100', '30 sec', '5 members', '—'],
                      ['Business', '$49/mo', 'Unlimited', '10 sec', 'Unlimited', '✓'],
                    ].map(([plan, price, monitors, interval, team, api], i) => (
                      <tr key={plan} className={i % 2 === 0 ? 'bg-white dark:bg-gray-900' : 'bg-gray-50 dark:bg-gray-800'}>
                        <td className="px-4 py-3 font-medium text-gray-800 dark:text-gray-200">{plan}</td>
                        <td className="px-4 py-3">{price}</td>
                        <td className="px-4 py-3">{monitors}</td>
                        <td className="px-4 py-3">{interval}</td>
                        <td className="px-4 py-3">{team}</td>
                        <td className="px-4 py-3">{api}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="mt-3 text-sm">Annual billing available at 20% discount. All plans allow commercial use.</p>
            </div>

            <div id="data-retention">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Data Retention</h3>
              <p className="mb-3">Check history is retained per plan. Data older than the retention window is automatically cleaned up nightly.</p>
              <ul className="space-y-1 text-sm">
                {[['Free', '30 days'], ['Starter', '30 days'], ['Pro', '90 days'], ['Business', '365 days']].map(([plan, days]) => (
                  <li key={plan}>• <strong className="text-gray-800 dark:text-gray-200">{plan}:</strong> {days}</li>
                ))}
              </ul>
            </div>
          </section>

          {/* Support CTA */}
          <section className="bg-green-50 dark:bg-green-950 rounded-2xl border border-green-100 dark:border-green-900 p-8 text-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Still have questions?</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-5">Happy to help. Reach out and I'll get back to you quickly.</p>
            <Link href="/contact" className="inline-block bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition font-medium">
              Contact Support
            </Link>
          </section>

        </main>
      </div>

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
            © 2026 Axiom Technologies. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
