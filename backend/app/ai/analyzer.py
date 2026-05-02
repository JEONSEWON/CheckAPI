import json
from typing import Optional

from app.ai.client import get_client


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
            model="claude-haiku-4-5-20251001",
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
