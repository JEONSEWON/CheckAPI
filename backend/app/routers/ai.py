"""
AI endpoints: analyze-endpoint for the Monitor Setup Wizard
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import get_current_user
from app.models import User
from app.ai.analyzer import analyze_endpoint

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


class AnalyzeRequest(BaseModel):
    url: str


@router.post("/analyze-endpoint")
async def analyze_endpoint_route(
    body: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        result = await analyze_endpoint(body.url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
