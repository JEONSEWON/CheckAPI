import os
import anthropic

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        _client = anthropic.Anthropic(
            api_key=api_key,
            max_retries=2,
            timeout=anthropic.Timeout(total=40.0, connect=5.0, read=35.0, write=5.0),
        )
    return _client
