"""
AI endpoints: analyze-endpoint for the Monitor Setup Wizard
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import get_current_user
from app.models import User
from app.ai.analyzer import analyze_endpoint

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

_executor = ThreadPoolExecutor(max_workers=4)


class AnalyzeRequest(BaseModel):
    url: str


@router.post("/analyze-endpoint")
async def analyze_endpoint_route(
    body: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
):
    loop = asyncio.get_event_loop()
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(_executor, analyze_endpoint, body.url),
            timeout=45.0,
        )
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Analysis timed out — the URL took too long to respond")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
