import Link from 'next/link';

export default function TermsPage() {
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
              <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition"><Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-green-600 transition">Log in</Link>
              <Link href="/register" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-10 text-center">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
          Terms of{' '}
          <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            Service
          </span>
        </h1>
        <p className="text-gray-500 dark:text-gray-400">Last updated: February 1, 2026</p>
      </section>

      {/* Content */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10 pb-24">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-10 shadow-sm space-y-10 text-gray-600 dark:text-gray-400 leading-relaxed">

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">1. Acceptance of Terms</h2>
            <p>By accessing or using CheckAPI ("the Service"), you agree to be bound by these Terms of Service. If you do not agree, please do not use the Service.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">2. Use of the Service</h2>
            <p>You may use CheckAPI to monitor URLs and APIs that you own or have permission to monitor. You may not use the Service to conduct unauthorized scans, attacks, or probes against third-party systems. We reserve the right to suspend accounts that violate this policy.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">3. Free Plan</h2>
            <p>The free plan is available for personal and commercial use with no restrictions. You may use CheckAPI to monitor your production services on the free tier without requiring a paid subscription.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">4. Paid Plans & Billing</h2>
            <p>Paid plans are billed monthly. You may cancel at any time, and your subscription will remain active until the end of the current billing period. We do not offer refunds for partial months.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">5. Service Availability</h2>
            <p>We aim for maximum uptime but do not guarantee 100% availability. Scheduled maintenance will be communicated in advance where possible. Business plan customers are covered by an SLA as outlined in their plan details.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">6. Limitation of Liability</h2>
            <p>CheckAPI is provided "as is." We are not liable for any damages resulting from missed alerts, downtime, or data loss. Our liability is limited to the amount paid for the Service in the past 3 months.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">7. Changes to Terms</h2>
            <p>We may update these terms from time to time. Continued use of the Service after changes constitutes acceptance of the new terms. We will notify users of significant changes by email.</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">8. Contact</h2>
            <p>For questions about these terms, contact us at <a href="mailto:support@checkapi.io" className="text-green-600 hover:text-green-700">support@checkapi.io</a>.</p>
          </div>

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
