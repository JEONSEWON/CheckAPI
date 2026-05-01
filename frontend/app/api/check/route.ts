import { NextRequest, NextResponse } from 'next/server';

const BLOCKED_HOSTS = ['localhost', '127.0.0.1', '::1', '0.0.0.0'];
const BLOCKED_IP_PATTERNS = [
  /^10\./,
  /^192\.168\./,
  /^172\.(1[6-9]|2[0-9]|3[0-1])\./,
  /^127\./,
  /^169\.254\./,
];

function isBlockedUrl(urlStr: string): boolean {
  try {
    const url = new URL(urlStr);
    if (!['http:', 'https:'].includes(url.protocol)) return true;
    const hostname = url.hostname;
    if (BLOCKED_HOSTS.includes(hostname.toLowerCase())) return true;
    if (BLOCKED_IP_PATTERNS.some(p => p.test(hostname))) return true;
    return false;
  } catch {
    return true;
  }
}

// Simple in-memory rate limit: max 20 req/min per IP
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const entry = rateLimitMap.get(ip);
  if (!entry || now > entry.resetAt) {
    rateLimitMap.set(ip, { count: 1, resetAt: now + 60_000 });
    return false;
  }
  if (entry.count >= 20) return true;
  entry.count++;
  return false;
}

export async function POST(req: NextRequest) {
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0] ?? 'unknown';

  if (isRateLimited(ip)) {
    return NextResponse.json({ error: 'Too many requests. Please wait a minute.' }, { status: 429 });
  }

  let body: { url?: string; method?: string; headers?: Record<string, string> };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  const { url, method = 'GET', headers = {} } = body;

  if (!url || typeof url !== 'string') {
    return NextResponse.json({ error: 'URL is required' }, { status: 400 });
  }

  if (isBlockedUrl(url)) {
    return NextResponse.json({ error: 'URL not allowed' }, { status: 400 });
  }

  const TIMEOUT_MS = 10_000;
  const start = Date.now();

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const res = await fetch(url, {
      method: method.toUpperCase(),
      headers: {
        'User-Agent': 'CheckAPI-Checker/1.0 (+https://checkapi.io)',
        ...headers,
      },
      signal: controller.signal,
      redirect: 'follow',
    });

    clearTimeout(timer);

    const responseTime = Date.now() - start;
    const contentType = res.headers.get('content-type') ?? '';
    const rawBody = await res.text();
    const truncated = rawBody.length > 2000;
    const bodyPreview = rawBody.slice(0, 2000);

    // Try to pretty-print JSON
    let formattedBody = bodyPreview;
    if (contentType.includes('application/json')) {
      try {
        formattedBody = JSON.stringify(JSON.parse(bodyPreview), null, 2);
      } catch {
        // leave as-is
      }
    }

    const relevantHeaders: Record<string, string> = {};
    ['content-type', 'server', 'x-powered-by', 'cache-control', 'cf-ray'].forEach(h => {
      const v = res.headers.get(h);
      if (v) relevantHeaders[h] = v;
    });

    return NextResponse.json({
      status_code: res.status,
      status_text: res.statusText,
      response_time_ms: responseTime,
      content_type: contentType,
      body: formattedBody,
      body_truncated: truncated,
      headers: relevantHeaders,
    });
  } catch (err: unknown) {
    const responseTime = Date.now() - start;
    const isTimeout = err instanceof Error && err.name === 'AbortError';
    return NextResponse.json(
      {
        error: isTimeout
          ? `Request timed out after ${TIMEOUT_MS / 1000} seconds`
          : err instanceof Error
          ? err.message
          : 'Connection failed',
        response_time_ms: responseTime,
      },
      { status: isTimeout ? 408 : 502 }
    );
  }
}
