import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free API Health Checker — Test Any API Endpoint Instantly | CheckAPI',
  description: 'Check your API status code, response time, and response body right now. Free online API checker — no account required. Monitor APIs automatically with CheckAPI.',
  openGraph: {
    title: 'Free API Health Checker — Test Any API Endpoint Instantly',
    description: 'Check your API status code, response time, and response body right now. Free, no account required.',
    url: 'https://checkapi.io/api-checker',
    siteName: 'CheckAPI',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Free API Health Checker — Test Any API Endpoint Instantly',
    description: 'Check your API status code, response time, and response body right now. Free, no account required.',
    creator: '@imwon_dev',
  },
  alternates: {
    canonical: 'https://checkapi.io/api-checker',
  },
};

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What does this API checker do?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'It sends a real HTTP request to your API URL and returns the status code, response time, response headers, and a preview of the response body — immediately, no sign-up required.',
      },
    },
    {
      '@type': 'Question',
      name: 'Which HTTP methods are supported?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'GET, POST, PUT, DELETE, PATCH, HEAD, and OPTIONS.',
      },
    },
    {
      '@type': 'Question',
      name: 'What is the difference between this tool and CheckAPI monitoring?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'This tool checks your API once, right now. CheckAPI monitoring checks it automatically every 5 minutes and sends alerts via Slack, Email, or Telegram when something breaks.',
      },
    },
    {
      '@type': 'Question',
      name: 'How do I get alerted when my API goes down?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: "Create a free CheckAPI account, add your API as a monitor, and connect an alert channel. You'll be notified within minutes of any failure.",
      },
    },
  ],
};

export default function ApiCheckerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      {children}
    </>
  );
}
