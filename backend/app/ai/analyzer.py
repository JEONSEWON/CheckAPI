import json
import re
import socket
import urllib.parse
from typing import Optional

import httpx

from app.ai.client import get_client
from app.config import get_settings

_settings = get_settings()

# ── SSRF Protection ──────────────────────────────────────────────────────────

_BLOCKED_HOSTS = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}
_BLOCKED_IP_PATTERNS = [
    re.compile(r"^10\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^172\.(1[6-9]|2[0-9]|3[01])\."),
    re.compile(r"^127\."),
    re.compile(r"^169\.254\."),
]


def _is_blocked_url(url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return True
        hostname = parsed.hostname or ""
        if hostname.lower() in _BLOCKED_HOSTS:
            return True
        if any(p.match(hostname) for p in _BLOCKED_IP_PATTERNS):
            return True
        # Resolve DNS and re-check resolved IP to prevent DNS rebinding
        try:
            resolved = socket.gethostbyname(hostname)
            if resolved in _BLOCKED_HOSTS:
                return True
            if any(p.match(resolved) for p in _BLOCKED_IP_PATTERNS):
                return True
        except socket.gaierror:
            return True  # Can't resolve → block
        return False
    except Exception:
        return True


def analyze_incident(
    monitor_name: str,
    monitor_url: str,
    status: str,
    status_code: Optional[int],
    response_time: Optional[int],
    error_message: Optional[str],
) -> Optional[dict]:
    """Call Claude Haiku to analyze a failed check. Returns dict or None on error."""
    try:
        client = get_client()

        lines = [
            f"Monitor: {monitor_name}",
            f"URL: {monitor_url}",
            f"Status: {status}",
        ]
        if status_code:
            lines.append(f"HTTP Status Code: {status_code}")
        if response_time:
            lines.append(f"Response Time: {response_time}ms")
        if error_message:
            lines.append(f"Error: {error_message}")

        context = "\n".join(lines)

        message = client.messages.create(
            model=_settings.AI_MODEL,
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": (
                    "You are an API monitoring assistant. Analyze this failed health check.\n\n"
                    f"{context}\n\n"
                    "Respond in JSON with exactly these fields:\n"
                    '- "summary": one sentence plain-language summary (max 100 chars)\n'
                    '- "possible_causes": array of 2-3 short strings\n'
                    '- "recommended_actions": array of 1-2 short action strings\n\n'
                    "JSON only, no markdown."
                ),
            }],
        )

        text = message.content[0].text.strip()
        return json.loads(text)

    except Exception as e:
        print(f"⚠️  AI analysis failed: {e}")
        return None


def analyze_endpoint(url: str) -> dict:
    """
    Call the URL, inspect the response, and ask Claude to recommend
    monitor settings: method, expected_status, keyword, assertions.

    Raises ValueError for blocked/invalid URLs.
    Raises RuntimeError for HTTP/AI failures.
    """
    if _is_blocked_url(url):
        raise ValueError("URL not allowed")

    # ── Fetch the endpoint ────────────────────────────────────────────────
    try:
        with httpx.Client(timeout=10, follow_redirects=True, max_redirects=3) as client:
            response = client.get(
                url,
                headers={"User-Agent": "CheckAPI-Wizard/1.0 (+https://checkapi.io)"},
            )
    except httpx.TimeoutException:
        raise RuntimeError("Request timed out")
    except Exception as e:
        raise RuntimeError(f"Failed to reach URL: {e}")

    status_code = response.status_code
    content_type = response.headers.get("content-type", "")
    raw_body = response.text[:3000]

    # ── Ask Claude ────────────────────────────────────────────────────────
    try:
        ai_client = get_client()

        prompt = (
            "You are an API monitoring configuration assistant.\n\n"
            f"URL: {url}\n"
            f"HTTP Status Code: {status_code}\n"
            f"Content-Type: {content_type}\n"
            f"Response Body (truncated):\n{raw_body}\n\n"
            "Based on this response, recommend the best monitor settings.\n"
            "Respond with JSON only (no markdown) with exactly these fields:\n"
            '- "method": HTTP method string, e.g. "GET"\n'
            '- "expected_status": integer status code to expect, e.g. 200\n'
            '- "keyword": a short string that should be present in the response body to confirm health (null if none makes sense)\n'
            '- "keyword_present": boolean, true if keyword must be present\n'
            '- "assertions": array of up to 3 JSON Path assertion objects, each with:\n'
            '    {"path": "$.field", "operator": "equals"|"contains"|"exists", "expected": "value"}\n'
            '  Only include assertions if the response is JSON. Empty array otherwise.\n'
            '- "reasoning": one sentence explaining your choices (max 120 chars)\n'
        )

        message = ai_client.messages.create(
            model=_settings.AI_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )

        text = message.content[0].text.strip()
        result = json.loads(text)

        # Sanitize fields
        return {
            "method": str(result.get("method", "GET")).upper(),
            "expected_status": int(result.get("expected_status", status_code)),
            "keyword": result.get("keyword") or None,
            "keyword_present": bool(result.get("keyword_present", True)),
            "assertions": result.get("assertions") or [],
            "reasoning": str(result.get("reasoning", ""))[:150],
            "actual_status": status_code,
        }

    except json.JSONDecodeError as e:
        raise RuntimeError(f"AI returned invalid JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"AI analysis failed: {e}")
