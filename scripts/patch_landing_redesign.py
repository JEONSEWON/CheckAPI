FILE = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"

content = r"""import Link from 'next/link';
import { ArrowRight, CheckCircle, Zap, Shield, BarChart3, Bell, Globe, Code2, Terminal, Lock } from 'lucide-react';
import ClientHeader from '@/components/ClientHeader';
import PricingSection from '@/components/PricingSection';
import LiveUserCount from '@/components/LiveUserCount';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'CheckAPI — APIs that never lie to you.',
  description: 'Silent Failure Detection with Regex + JSON Path. Free forever for commercial use. Know when your API breaks before your users do.',
  openGraph: {
    title: 'CheckAPI — APIs that never lie to you.',
    description: 'Silent Failure Detection with Regex. Free forever for commercial use.',
    url: 'https://checkapi.io',
    siteName: 'CheckAPI',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CheckAPI — APIs that never lie to you.',
    description: 'Silent Failure Detection with Regex. Free forever for commercial use.',
    creator: '@imwon_dev',
  },
};

export default function HomePage() {
  return (
    <div className="min-h-screen" style={{ background: '#080d1a', color: '#e2e8f0', fontFamily: "'DM Sans', 'Inter', sans-serif" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

        :root {
          --teal: #00e5b4;
          --teal-dim: #00b890;
          --navy: #080d1a;
          --navy-2: #0d1424;
          --navy-3: #111827;
          --glass: rgba(255,255,255,0.04);
          --glass-border: rgba(255,255,255,0.08);
          --text: #e2e8f0;
          --muted: #64748b;
        }

        .teal { color: var(--teal); }
        .btn-primary {
          background: var(--teal);
          color: #080d1a;
          font-weight: 700;
          padding: 14px 28px;
          border-radius: 12px;
          display: inline-flex;
          align-items: center;
          gap: 8px;
          font-size: 15px;
          transition: all 0.2s;
          text-decoration: none;
          letter-spacing: -0.01em;
        }
        .btn-primary:hover { background: #00ffca; transform: translateY(-1px); box-shadow: 0 0 30px rgba(0,229,180,0.3); }
        .btn-ghost {
          color: #94a3b8;
          padding: 14px 24px;
          border-radius: 12px;
          display: inline-flex;
          align-items: center;
          gap: 8px;
          font-size: 15px;
          transition: color 0.2s;
          text-decoration: none;
          border: 1px solid rgba(255,255,255,0.08);
        }
        .btn-ghost:hover { color: var(--teal); border-color: var(--teal); }

        .glass-card {
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 16px;
          backdrop-filter: blur(12px);
        }
        .glass-card-bright {
          background: rgba(0,229,180,0.04);
          border: 1px solid rgba(0,229,180,0.15);
          border-radius: 16px;
        }

        .floating-tag {
          position: absolute;
          background: rgba(0,229,180,0.08);
          border: 1px solid rgba(0,229,180,0.2);
          color: var(--teal);
          padding: 8px 14px;
          border-radius: 10px;
          font-family: 'DM Mono', monospace;
          font-size: 13px;
          white-space: nowrap;
          opacity: 0.6;
          pointer-events: none;
        }

        .glow-text {
          text-shadow: 0 0 40px rgba(0,229,180,0.3);
        }

        .section-label {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          background: rgba(0,229,180,0.08);
          border: 1px solid rgba(0,229,180,0.2);
          color: var(--teal);
          font-size: 12px;
          font-weight: 600;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          padding: 6px 14px;
          border-radius: 999px;
          margin-bottom: 20px;
        }

        .code-block {
          background: #0d1424;
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 12px;
          padding: 20px;
          font-family: 'DM Mono', monospace;
          font-size: 13px;
          line-height: 1.8;
        }
        .code-block .key { color: #60a5fa; }
        .code-block .val-ok { color: #34d399; }
        .code-block .val-err { color: #f87171; }
        .code-block .val-str { color: #fbbf24; }
        .code-block .comment { color: #475569; }
        .code-block .highlight-line {
          background: rgba(248,113,113,0.1);
          border-left: 2px solid #f87171;
          margin: 0 -20px;
          padding: 2px 20px;
          display: block;
        }
        .code-block .detect-line {
          background: rgba(0,229,180,0.08);
          border-left: 2px solid var(--teal);
          margin: 0 -20px;
          padding: 2px 20px;
          display: block;
        }

        .feature-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 16px;
        }

        .monitor-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 14px 20px;
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.05);
          border-radius: 12px;
          margin-bottom: 8px;
        }
        .monitor-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--teal); box-shadow: 0 0 8px var(--teal); }

        .stat-pill {
          background: rgba(0,229,180,0.08);
          border: 1px solid rgba(0,229,180,0.15);
          color: var(--teal);
          padding: 4px 10px;
          border-radius: 999px;
          font-size: 12px;
          font-weight: 600;
          font-family: 'DM Mono', monospace;
        }

        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 8px var(--teal); }
          50% { box-shadow: 0 0 20px var(--teal), 0 0 40px rgba(0,229,180,0.3); }
        }
        .pulse-dot { animation: pulse-glow 2s ease-in-out infinite; }

        @keyframes float-1 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
        @keyframes float-2 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
        @keyframes float-3 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-16px)} }
        .float-1 { animation: float-1 6s ease-in-out infinite; }
        .float-2 { animation: float-2 8s ease-in-out infinite; }
        .float-3 { animation: float-3 5s ease-in-out infinite; }

        .grid-bg {
          background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
          background-size: 60px 60px;
        }

        .bar-chart-bar { border-radius: 3px 3px 0 0; transition: all 0.3s; }
      `}</style>

      <ClientHeader />

      {/* ── HERO ── */}
      <section className="grid-bg relative overflow-hidden" style={{ paddingTop: '100px', paddingBottom: '80px', minHeight: '100vh', display: 'flex', alignItems: 'center' }}>
        {/* Radial glow */}
        <div style={{ position: 'absolute', top: '20%', left: '50%', transform: 'translateX(-50%)', width: '600px', height: '600px', background: 'radial-gradient(circle, rgba(0,229,180,0.06) 0%, transparent 70%)', pointerEvents: 'none' }} />

        {/* Floating tags */}
        <div className="float-1 floating-tag" style={{ top: '18%', left: '8%' }}>API regex&gt;</div>
        <div className="float-2 floating-tag" style={{ top: '40%', left: '4%' }}>API &lt;&lt;&gt;&gt;</div>
        <div className="float-3 floating-tag" style={{ top: '65%', left: '9%' }}>Regex</div>
        <div className="float-2 floating-tag" style={{ top: '18%', right: '6%' }}>Regex&gt;</div>
        <div className="float-1 floating-tag" style={{ top: '42%', right: '4%' }}>API you</div>
        <div className="float-3 floating-tag" style={{ top: '68%', right: '8%' }}>API repx&gt;</div>

        <div className="max-w-4xl mx-auto px-4 text-center" style={{ position: 'relative', zIndex: 1, width: '100%' }}>
          <LiveUserCount />
          <div className="section-label" style={{ margin: '16px auto 28px' }}>
            <CheckCircle style={{ width: '12px', height: '12px' }} />
            Free for Commercial Use — No restrictions
          </div>

          <h1 style={{ fontSize: 'clamp(42px, 7vw, 76px)', fontWeight: 800, lineHeight: 1.08, letterSpacing: '-0.04em', marginBottom: '24px', color: '#f8fafc' }}>
            APIs that never<br />
            <span className="teal glow-text">lie to you.</span>
          </h1>

          <p style={{ fontSize: '18px', color: '#64748b', maxWidth: '520px', margin: '0 auto 40px', lineHeight: 1.7 }}>
            JSON Path + Regex + Silent Failure Detection.<br />
            Free forever for commercial use.
          </p>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '20px' }}>
            <Link href="/register" className="btn-primary">
              Start monitoring free
              <ArrowRight style={{ width: '16px', height: '16px' }} />
            </Link>
            <a href="#features" className="btn-ghost">
              See how it works →
            </a>
          </div>

          <p style={{ fontSize: '13px', color: '#334155' }}>No credit card required · 5-minute setup · 10 monitors free</p>

          {/* Dashboard mockup */}
          <div className="glass-card" style={{ marginTop: '64px', overflow: 'hidden', maxWidth: '820px', margin: '64px auto 0' }}>
            <div style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid rgba(255,255,255,0.06)', padding: '12px 20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444' }} />
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b' }} />
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981' }} />
              <span style={{ marginLeft: '12px', fontSize: '12px', color: '#334155', fontFamily: "'DM Mono', monospace" }}>checkapi.io/dashboard</span>
            </div>
            <div style={{ padding: '28px' }}>
              {/* Stats */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '24px' }}>
                {[
                  { label: 'Total Monitors', value: '8' },
                  { label: 'Online', value: '8', teal: true },
                  { label: 'Offline', value: '0', red: true },
                  { label: 'Avg Uptime', value: '99.9%', teal: true },
                ].map((s) => (
                  <div key={s.label} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '10px', padding: '14px' }}>
                    <p style={{ fontSize: '11px', color: '#475569', marginBottom: '6px' }}>{s.label}</p>
                    <p style={{ fontSize: '22px', fontWeight: 700, color: s.teal ? '#00e5b4' : s.red ? '#f87171' : '#f1f5f9', fontFamily: "'DM Mono', monospace" }}>{s.value}</p>
                  </div>
                ))}
              </div>
              {/* Chart */}
              <div style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px', padding: '20px', marginBottom: '16px', position: 'relative' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                  <span style={{ fontSize: '13px', fontWeight: 600, color: '#94a3b8' }}>Response Time — Last 24h</span>
                  <span style={{ fontSize: '11px', color: '#334155' }}>Updated 30s ago</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'flex-end', gap: '3px', height: '64px' }}>
                  {[40,45,42,38,44,80,120,95,48,42,44,41,39,43,46,42,40,38,44,43,41,45,42,40].map((h, i) => (
                    <div key={i} className="bar-chart-bar" style={{ flex: 1, height: `${(h/120)*100}%`, background: h > 70 ? '#f87171' : '#00e5b4', opacity: h > 70 ? 1 : 0.7 }} />
                  ))}
                </div>
                <div style={{ position: 'absolute', top: '44px', left: '38%', background: '#ef4444', color: 'white', fontSize: '11px', fontWeight: 700, padding: '5px 10px', borderRadius: '6px', boxShadow: '0 4px 12px rgba(239,68,68,0.4)', whiteSpace: 'nowrap' }}>
                  ⚡ Latency spike — Slack alert sent in 1s
                </div>
              </div>
              {/* Monitor list */}
              {[
                { name: 'Production API', url: 'api.yourapp.com', uptime: '99.9%' },
                { name: 'Staging Environment', url: 'staging-api.yourapp.com', uptime: '99.8%' },
                { name: 'Payment Webhook', url: 'hooks.yourapp.com/stripe', uptime: '100%' },
              ].map((m) => (
                <div key={m.name} className="monitor-row">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div className="monitor-dot pulse-dot" />
                    <div>
                      <p style={{ fontSize: '13px', fontWeight: 600, color: '#e2e8f0' }}>{m.name}</p>
                      <p style={{ fontSize: '11px', color: '#334155', fontFamily: "'DM Mono', monospace" }}>{m.url}</p>
                    </div>
                  </div>
                  <span className="stat-pill">{m.uptime} uptime</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── PAIN POINT ── */}
      <section style={{ padding: '100px 24px', maxWidth: '1100px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <div className="section-label" style={{ margin: '0 auto 20px' }}>The Problem</div>
          <h2 style={{ fontSize: 'clamp(30px, 4vw, 48px)', fontWeight: 800, letterSpacing: '-0.03em', color: '#f8fafc', marginBottom: '16px' }}>
            200 OK but<br />something is wrong?
          </h2>
          <p style={{ color: '#64748b', fontSize: '17px', maxWidth: '480px', margin: '0 auto' }}>
            Common API monitoring pain points — the pattern most API monitors and their competitors miss.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          {/* Before */}
          <div className="glass-card" style={{ padding: '28px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#f87171', boxShadow: '0 0 8px #f87171' }} />
              <span style={{ fontSize: '13px', color: '#f87171', fontWeight: 600 }}>Without CheckAPI</span>
            </div>
            <div className="code-block">
              <span className="comment">// HTTP 200 OK — monitor says "UP" ✓</span><br />
              {'{'}<br />
              &nbsp;&nbsp;<span className="key">"status"</span>: <span className="val-str">"ok"</span>,<br />
              <span className="highlight-line">
                &nbsp;&nbsp;<span className="key">"data"</span>: <span className="val-err">null</span>,
              </span>
              <span className="highlight-line">
                &nbsp;&nbsp;<span className="key">"error"</span>: <span className="val-str">"DB_CONN_FAILED"</span>
              </span>
              {'}'}
              <br /><br />
              <span className="comment">// Your users see broken data.</span><br />
              <span className="comment">// You find out at 9AM.</span>
            </div>
          </div>

          {/* After */}
          <div className="glass-card-bright" style={{ padding: '28px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
              <div className="pulse-dot" style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#00e5b4' }} />
              <span style={{ fontSize: '13px', color: '#00e5b4', fontWeight: 600 }}>With CheckAPI Regex</span>
            </div>
            <div className="code-block">
              <span className="comment">// Pattern: "error":\s*"[A-Z]</span><br />
              <span className="comment">// CheckAPI scans response body</span><br /><br />
              {'{'}<br />
              &nbsp;&nbsp;<span className="key">"status"</span>: <span className="val-str">"ok"</span>,<br />
              <span className="detect-line">
                &nbsp;&nbsp;<span className="key">"error"</span>: <span className="val-str">"DB_CONN_FAILED"</span>
              </span>
              {'}'}
              <br /><br />
              <span style={{ color: '#00e5b4' }}>⚡ DEGRADED — alert fired immediately.</span><br />
              <span style={{ color: '#00e5b4' }}>You know before any user does.</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── KILL FEATURES ── */}
      <section id="features" style={{ padding: '60px 24px 100px', maxWidth: '1100px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <div className="section-label" style={{ margin: '0 auto 20px' }}>Features</div>
          <h2 style={{ fontSize: 'clamp(30px, 4vw, 48px)', fontWeight: 800, letterSpacing: '-0.03em', color: '#f8fafc' }}>
            Built to catch what<br />others miss.
          </h2>
        </div>

        {/* Regex hero feature */}
        <div className="glass-card-bright" style={{ padding: '40px', marginBottom: '20px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', alignItems: 'center' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(0,229,180,0.1)', border: '1px solid rgba(0,229,180,0.25)', color: '#00e5b4', padding: '6px 14px', borderRadius: '999px', fontSize: '12px', fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '20px' }}>
              ★ Key Differentiator
            </div>
            <h3 style={{ fontSize: '32px', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.03em', marginBottom: '16px', lineHeight: 1.2 }}>
              Silent Failure<br />Detection
            </h3>
            <p style={{ color: '#64748b', fontSize: '16px', lineHeight: 1.7, marginBottom: '20px' }}>
              Your API returns 200 OK — but the response body contains an error, null data, or broken content. CheckAPI validates the body with <strong style={{ color: '#00e5b4' }}>Regex patterns</strong>, not just status codes.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {['Keyword match (present / absent)', 'Regex pattern matching', 'JSON field assertion (coming soon)'].map((f, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '14px', color: i === 2 ? '#334155' : '#94a3b8' }}>
                  <CheckCircle style={{ width: '14px', height: '14px', color: i === 2 ? '#334155' : '#00e5b4', flexShrink: 0 }} />
                  {f}
                </div>
              ))}
            </div>
          </div>
          <div className="code-block" style={{ fontSize: '13px' }}>
            <span className="comment"># Example patterns</span><br /><br />
            <span className="comment"># Must contain "ok"</span><br />
            <span className="val-ok">keyword:</span> <span className="val-str">"status":"ok"</span><br /><br />
            <span className="comment"># Regex: status field = ok or healthy</span><br />
            <span className="val-ok">regex:</span> <span className="val-str">"status":\s*"(ok|healthy)"</span><br /><br />
            <span className="comment"># Balance must be positive</span><br />
            <span className="val-ok">regex:</span> <span className="val-str">"balance":\s*[1-9]\d*</span><br /><br />
            <span className="comment"># Error field must be null</span><br />
            <span className="val-ok">regex:</span> <span className="val-str">"error":\s*null</span>
          </div>
        </div>

        {/* Other features grid */}
        <div className="feature-grid">
          {[
            { icon: <Zap style={{ width: '20px', height: '20px' }} />, title: 'Instant Alerts', desc: 'Check every minute. Email, Slack, Telegram, Discord, Webhook — all on the free plan.' },
            { icon: <BarChart3 style={{ width: '20px', height: '20px' }} />, title: 'Response Time Analytics', desc: 'Track uptime, response times, incidents. SLA reports for Pro & Business.' },
            { icon: <Globe style={{ width: '20px', height: '20px' }} />, title: 'Public Status Pages', desc: 'Shareable status page per monitor. 90-day uptime chart. No login required.' },
            { icon: <Lock style={{ width: '20px', height: '20px' }} />, title: 'Maintenance Windows', desc: 'Schedule recurring windows. Alerts suppressed, checks still run.' },
            { icon: <Terminal style={{ width: '20px', height: '20px' }} />, title: 'REST API Access', desc: 'Business plan: full API access via API keys for programmatic monitor management.' },
            { icon: <CheckCircle style={{ width: '20px', height: '20px' }} />, title: 'Free for Commercial Use', desc: 'Unlike UptimeRobot, zero commercial restrictions on the free plan. Build your business.' },
          ].map((f) => (
            <div key={f.title} className="glass-card" style={{ padding: '24px' }}>
              <div style={{ width: '40px', height: '40px', background: 'rgba(0,229,180,0.08)', border: '1px solid rgba(0,229,180,0.15)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00e5b4', marginBottom: '14px' }}>
                {f.icon}
              </div>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#e2e8f0', marginBottom: '8px' }}>{f.title}</h3>
              <p style={{ fontSize: '13px', color: '#475569', lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── PRICING ── */}
      <PricingSection />

      {/* ── CTA ── */}
      <section style={{ padding: '80px 24px', maxWidth: '700px', margin: '0 auto', textAlign: 'center' }}>
        <div className="glass-card-bright" style={{ padding: '64px 40px' }}>
          <h2 style={{ fontSize: 'clamp(24px, 3vw, 40px)', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.03em', marginBottom: '16px' }}>
            Start monitoring before<br />your next incident.
          </h2>
          <p style={{ color: '#64748b', fontSize: '16px', marginBottom: '32px' }}>
            Takes 5 minutes to set up. Free forever for commercial use.
          </p>
          <Link href="/register" className="btn-primary" style={{ margin: '0 auto' }}>
            Protect My API for Free
            <ArrowRight style={{ width: '16px', height: '16px' }} />
          </Link>
          <p style={{ fontSize: '12px', color: '#334155', marginTop: '16px' }}>No credit card required · 10 monitors free forever</p>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={{ borderTop: '1px solid rgba(255,255,255,0.05)', padding: '60px 24px' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '40px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
              <img src="/logo.jpg" alt="CheckAPI" style={{ width: '32px', height: '32px', borderRadius: '8px' }} />
              <span style={{ fontSize: '16px', fontWeight: 700, color: '#00e5b4' }}>CheckAPI</span>
            </div>
            <p style={{ fontSize: '12px', color: '#334155', marginBottom: '4px' }}>by Axiom Technologies</p>
            <p style={{ fontSize: '13px', color: '#475569', lineHeight: 1.6, maxWidth: '240px' }}>
              Silent Failure Detection for APIs. Free forever for commercial use.
            </p>
          </div>
          {[
            { title: 'Product', links: [['Features', '#features'], ['Pricing', '#pricing'], ['Docs', '/docs'], ['Blog', '/blog']] },
            { title: 'Company', links: [['About', '/about'], ['Contact', '/contact'], ['Twitter', 'https://x.com/imwon_dev']] },
            { title: 'Legal', links: [['Privacy', '/privacy'], ['Terms', '/terms']] },
          ].map((col) => (
            <div key={col.title}>
              <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#94a3b8', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{col.title}</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {col.links.map(([label, href]) => (
                  <li key={label}>
                    <Link href={href} style={{ fontSize: '13px', color: '#475569', textDecoration: 'none', transition: 'color 0.2s' }}
                      onMouseEnter={e => (e.currentTarget.style.color = '#00e5b4')}
                      onMouseLeave={e => (e.currentTarget.style.color = '#475569')}>
                      {label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div style={{ maxWidth: '1100px', margin: '40px auto 0', paddingTop: '24px', borderTop: '1px solid rgba(255,255,255,0.04)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '12px', color: '#334155' }}>© 2026 Axiom Technologies. All rights reserved.</span>
          <span style={{ fontSize: '12px', color: '#334155' }}>Built by a solo dev from Seoul 🇰🇷</span>
        </div>
      </footer>
    </div>
  );
}
"""

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("File size:", len(content), "chars")
