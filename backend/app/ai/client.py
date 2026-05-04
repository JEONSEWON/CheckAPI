import os
import anthropic

_sync_client: anthropic.Anthropic | None = None
_async_client: anthropic.AsyncAnthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _sync_client
    if _sync_client is None:
        api_key = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        _sync_client = anthropic.Anthropic(
            api_key=api_key,
            max_retries=2,
            timeout=anthropic.Timeout(40.0, connect=5.0, read=35.0, write=5.0),
        )
    return _sync_client


def get_async_client() -> anthropic.AsyncAnthropic:
    global _async_client
    if _async_client is None:
        api_key = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        _async_client = anthropic.AsyncAnthropic(
            api_key=api_key,
            max_retries=2,
            timeout=anthropic.Timeout(40.0, connect=5.0, read=35.0, write=5.0),
        )
    return _async_client
