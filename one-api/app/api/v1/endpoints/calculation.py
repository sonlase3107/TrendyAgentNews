from fastapi import APIRouter, Body

from app.schemas.calculation import (
    CalculationRequest,
    CalculationResponse,
    ExtractArticlesResponse,
    ExtractRequest,
)
from app.services.calculation import CalculationService

router = APIRouter(prefix="/calculation", tags=["calculation"])
service = CalculationService()

@router.post("/extract_article", response_model=ExtractArticlesResponse)
async def extract_article(
    payload: ExtractRequest = Body(..., media_type="text/plain")
) -> ExtractArticlesResponse:
    """Parse a raw XML RSS feed string and return a list of ArticleItem objects."""
    articles = service.extract_articles(payload.root)
    return ExtractArticlesResponse(
        success=True,
        message=f"{len(articles)} article(s) extracted",
        data=articles,
    )
