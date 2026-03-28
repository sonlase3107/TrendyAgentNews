from fastapi import APIRouter

from app.schemas.rss import FetchRSSRequest, FetchRSSResponse, ListTopicsResponse
from app.services.rss import RSSService

router = APIRouter(prefix="/rss", tags=["rss"])
service = RSSService()


@router.get("/list_topics", response_model=ListTopicsResponse)
async def list_topics() -> ListTopicsResponse:
    """Return all active RSS topics stored in the database."""
    topics = service.list_topics()
    return ListTopicsResponse(
        success=True,
        message=f"{len(topics)} topic(s) available",
        data=topics,
    )


@router.post("/fetch_rss", response_model=FetchRSSResponse)
async def fetch_rss(payload: FetchRSSRequest) -> FetchRSSResponse:
    """Fetch and parse RSS feeds for the requested topics.

    Returns a merged list of articles sorted by ``pub_date`` descending, plus
    per-topic error details for any feed that could not be fetched or parsed.
    ``success`` is ``true`` when at least one topic was fetched successfully.
    """
    items, errors = service.fetch_rss(payload)
    success = len(errors) == 0 or len(items) > 0
    message = f"{len(items)} article(s) fetched"
    if errors:
        message += f", {len(errors)} topic(s) failed"
    return FetchRSSResponse(
        success=success,
        message=message,
        data=items,
        errors=errors,
    )
