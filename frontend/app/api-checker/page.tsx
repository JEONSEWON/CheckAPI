'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowRight, CheckCircle, Clock, AlertCircle, Loader2, ChevronDown, Shield, Zap, Bell } from 'lucide-react';
import PublicAuthButtons from '@/components/PublicAuthButtons';

const METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'];

interface CheckResult {
  status_code?: number;
  status_text?: string;
  response_time_ms?: number;
  content_type?: string;
  body?: string;
  body_truncated?: boolean;
  headers?: Record<string, string>;
  error?: string;
}

function statusColor(code: number) {
  if (code >= 200 && code < 300) return { bg: 'bg-green-100', text: 'text-green-700', border: 'border-green-300', dot: 'bg-green-500' };
  if (code >= 300 && code < 400) return { bg: 'bg-blue-100', text: 'text-blue-700', border: 'border-blue-300', dot: 'bg-blue-500' };
  if (code >= 400 && code < 500) return { bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-amber-300', dot: 'bg-amber-500' };
  return { bg: 'bg-red-100', text: 'text-red-700', border: 'border-red-300', dot: 'bg-red-500' };
}

function speedLabel(ms: number) {
  if (ms < 300) return { label: 'Fast', color: 'text-green-600' };
  if (ms < 1000) return { label: 'Moderate', color: 'text-amber-600' };
  return { label: 'Slow', color: 'text-red-600' };
}

export default function ApiCheckerPage() {
  const [url, setUrl] = useState('');
  const [method, setMethod] = useState('GET');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CheckResult | null>(null);
  const [checked, setChecked] = useState(false);

  async function handleCheck(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;

    let normalizedUrl = url.trim();
    if (!/^https?:\/\//i.test(normalizedUrl)) {
      normalizedUrl = 'https://' + normalizedUrl;
    }

    setLoading(true);
    setResult(null);
    setChecked(false);

    try {
      const res = await fetch('/api/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: normalizedUrl, method }),
      });
      const data = await res.json();
      setResult(data);
    } catch {
      setResult({ error: 'Something went wrong. Please try again.' });
    } finally {
      setLoading(false);
      setChecked(true);
    }
  }

  const colors = result?.status_code ? statusColor(result.status_code) : null;
  const speed = result?.response_time_ms != null ? speedLabel(result.response_time_ms) : null;
  const isSuccess = result?.status_code && result.status_code >= 200 && result.status_code < 300;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              CheckAPI
            </Link>
            <nav className="hidden md:flex space-x-8 text-sm">
              <Link href="/#features" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition">Features</Link>
              <Link href="/pricing" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition">Pricing</Link>
              <Link href="/blog" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition">Blog</Link>
              <Link href="/docs" className="text-gray-600 dark:text-gray-400 hover:text-green-600 transition">Docs</Link>
            </nav>
            <div className="flex items-center space-x-4">
              <PublicAuthButtons />
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Hero + Tool */}
        <section className="max-w-3xl mx-auto px-4 sm:px-6 pt-16 pb-10">
          <div className="text-center mb-10">
            <span className="inline-block bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 text-xs font-semibold px-3 py-1 rounded-full mb-4">
              Free API Checker
            </span>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
              Check Your API Health<br />Right Now — Free
            </h1>
            <p className="text-lg text-gray-500 dark:text-gray-400 max-w-xl mx-auto">
              Enter any API URL and instantly see its status code, response time, and response body. No account required.
            </p>
          </div>

          {/* Checker form */}
          <form onSubmit={handleCheck} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm p-6">
            <div className="flex gap-3 mb-4">
              {/* Method selector */}
              <div className="relative">
                <select
                  value={method}
                  onChange={e => setMethod(e.target.value)}
                  className="appearance-none bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-mono text-sm font-bold px-4 py-3 pr-8 rounded-xl border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 cursor-pointer"
                >
                  {METHODS.map(m => <option key={m}>{m}</option>)}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
              </div>

              {/* URL input */}
              <input
                type="text"
                value={url}
                onChange={e => setUrl(e.target.value)}
                placeholder="https://api.example.com/health"
                className="flex-1 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading || !url.trim()}
              className="w-full bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition flex items-center justify-center gap-2"
            >
              {loading ? (
                <><Loader2 className="h-4 w-4 animate-spin" /> Checking…</>
              ) : (
                <><Zap className="h-4 w-4" /> Check Now</>
              )}
            </button>
          </form>

          {/* Results */}
          {checked && result && (
            <div className="mt-6 bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">

              {result.error ? (
                /* Error state */
                <div className="p-6">
                  <div className="flex items-start gap-3">
                    <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0">
                      <AlertCircle className="h-5 w-5 text-red-600" />
                    </div>
                    <div>
                      <p className="font-bold text-gray-900 dark:text-white mb-1">Request Failed</p>
                      <p className="text-sm text-red-600 dark:text-red-400">{result.error}</p>
                      {result.response_time_ms != null && (
                        <p className="text-xs text-gray-400 mt-1">after {result.response_time_ms}ms</p>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <>
                  {/* Status row */}
                  <div className="px-6 py-5 border-b border-gray-100 dark:border-gray-800 flex items-center gap-6 flex-wrap">
                    {/* Status code */}
                    <div className={`flex items-center gap-2 px-4 py-2 rounded-xl border ${colors?.bg} ${colors?.border}`}>
                      <div className={`w-2 h-2 rounded-full ${colors?.dot}`} />
                      <span className={`text-2xl font-bold ${colors?.text}`}>{result.status_code}</span>
                      <span className={`text-sm ${colors?.text} opacity-70`}>{result.status_text}</span>
                    </div>

                    {/* Response time */}
                    {result.response_time_ms != null && (
                      <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                        <Clock className="h-4 w-4" />
                        <span className="font-semibold">{result.response_time_ms}ms</span>
                        <span className={`text-xs font-medium ${speed?.color}`}>({speed?.label})</span>
                      </div>
                    )}

                    {/* Content type */}
                    {result.content_type && (
                      <span className="text-xs bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 px-2 py-1 rounded-lg font-mono">
                        {result.content_type.split(';')[0]}
                      </span>
                    )}
                  </div>

                  {/* Headers */}
                  {result.headers && Object.keys(result.headers).length > 0 && (
                    <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-800">
                      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Response Headers</p>
                      <div className="space-y-1">
                        {Object.entries(result.headers).map(([k, v]) => (
                          <div key={k} className="flex gap-3 text-xs">
                            <span className="font-mono text-gray-400 w-36 flex-shrink-0">{k}</span>
                            <span className="font-mono text-gray-700 dark:text-gray-300 break-all">{v}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Body */}
                  {result.body && (
                    <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-800">
                      <div className="flex justify-between items-center mb-2">
                        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Response Body</p>
                        {result.body_truncated && (
                          <span className="text-xs text-amber-500">Truncated at 2,000 chars</span>
                        )}
                      </div>
                      <pre className="bg-gray-950 text-green-400 rounded-xl p-4 text-xs overflow-x-auto max-h-64 leading-relaxed font-mono whitespace-pre-wrap break-all">
                        {result.body}
                      </pre>
                    </div>
                  )}

                  {/* CTA */}
                  <div className="px-6 py-5 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950 dark:to-emerald-950">
                    <div className="flex items-center justify-between gap-4 flex-wrap">
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white text-sm">
                          {isSuccess ? '✅ API is responding. Want to monitor it automatically?' : '⚠️ Something looks off. Set up an alert to catch this next time.'}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                          Get alerted via Slack, Email, or Telegram when your API goes down. Free plan — no credit card.
                        </p>
                      </div>
                      <Link
                        href="/register"
                        className="flex-shrink-0 inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition"
                      >
                        Monitor Free <ArrowRight className="h-4 w-4" />
                      </Link>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </section>

        {/* How it works */}
        <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16">
          <div className="grid md:grid-cols-3 gap-6 mt-4">
            {[
              { icon: Zap, title: 'Instant check', desc: 'Paste any URL and get results in seconds — status code, response time, and body preview.' },
              { icon: Shield, title: 'No account needed', desc: 'The one-time checker is completely free and requires no sign-up.' },
              { icon: Bell, title: 'Want automatic alerts?', desc: 'Create a free account to monitor every 5 minutes and get Slack/Email alerts when it goes down.' },
            ].map(({ icon: Icon, title, desc }) => (
              <div key={title} className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 p-6">
                <div className="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-xl flex items-center justify-center mb-4">
                  <Icon className="h-5 w-5 text-green-600 dark:text-green-400" />
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* vs Ongoing monitoring */}
        <section className="bg-white dark:bg-gray-900 border-t border-b border-gray-200 dark:border-gray-800">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 py-16">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">One-time check vs automatic monitoring</h2>
            <p className="text-gray-500 dark:text-gray-400 mb-8">This checker tests your API right now. But APIs go down at 3am, on weekends, after deployments — times when you're not looking.</p>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="rounded-2xl border-2 border-gray-200 dark:border-gray-700 p-6">
                <h3 className="font-bold text-gray-900 dark:text-white mb-4">This tool (one-time)</h3>
                <ul className="space-y-3 text-sm text-gray-600 dark:text-gray-400">
                  {['Check now, manually', 'See current status only', 'No alerts', 'No history'].map(item => (
                    <li key={item} className="flex items-center gap-2">
                      <span className="w-4 h-4 text-gray-300">—</span> {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-2xl border-2 border-green-500 p-6 bg-green-50 dark:bg-green-950">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-gray-900 dark:text-white">CheckAPI monitoring (free)</h3>
                  <span className="text-xs bg-green-600 text-white px-2 py-0.5 rounded-full font-medium">Recommended</span>
                </div>
                <ul className="space-y-3 text-sm text-gray-700 dark:text-gray-300">
                  {[
                    'Checks every 5 minutes automatically',
                    'Slack, Email, Telegram alerts on failure',
                    '30-day history & uptime chart',
                    'Silent failure detection (body validation)',
                    'Public status page included',
                  ].map(item => (
                    <li key={item} className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600 flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/register"
                  className="mt-6 inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition w-full justify-center"
                >
                  Start Free — No Credit Card <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="max-w-3xl mx-auto px-4 sm:px-6 py-16">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">FAQ</h2>
          <div className="space-y-6">
            {[
              {
                q: 'What does this API checker do?',
                a: 'It sends a real HTTP request to your API URL and returns the status code, response time, response headers, and a preview of the response body — immediately, no sign-up required.',
              },
              {
                q: 'Which HTTP methods are supported?',
                a: 'GET, POST, PUT, DELETE, PATCH, HEAD, and OPTIONS. Select the method from the dropdown before checking.',
              },
              {
                q: 'Is this different from ping or uptime monitoring?',
                a: 'Yes. A ping only checks if a host is reachable. This checker makes a real HTTP request and shows you the full response — status code, headers, and body — so you can see exactly what your API returns.',
              },
              {
                q: 'What is the difference between this tool and CheckAPI monitoring?',
                a: 'This tool checks your API once, right now. CheckAPI monitoring checks it automatically every 5 minutes (free plan) and sends you an alert via Slack, Email, or Telegram when something breaks — even at 3am.',
              },
              {
                q: 'How do I get alerted when my API goes down?',
                a: 'Create a free CheckAPI account, add your API as a monitor, and connect an alert channel (Email, Slack, Telegram, Discord, or Webhook). You\'ll be notified within minutes of any failure.',
              },
            ].map(({ q, a }) => (
              <div key={q} className="border-b border-gray-200 dark:border-gray-800 pb-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{q}</h3>
                <p className="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">{a}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 text-center text-sm text-gray-500 dark:text-gray-400">
          © 2026 CheckAPI by Axiom Technologies ·{' '}
          <Link href="/blog" className="hover:text-green-600">Blog</Link> ·{' '}
          <Link href="/docs" className="hover:text-green-600">Docs</Link> ·{' '}
          <Link href="/privacy" className="hover:text-green-600">Privacy</Link>
        </div>
      </footer>
    </div>
  );
}
