from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.base import BaseResponse
from app.schemas.calculation import ArticleItem


class TopicRecord(BaseModel):
    """A single RSS topic as stored in the database."""

    id: str
    name: str
    category: Optional[str] = None
    is_active: bool
    created_at: str
    url: str
    domain: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class ListTopicsResponse(BaseResponse[list[TopicRecord]]):
    """Response envelope for the list_topics endpoint."""


class TopicRequest(BaseModel):
    """A topic reference sent in the fetch_rss request body."""

    topic_id: str
    topic_name: str

    model_config = ConfigDict(extra="forbid")


class FetchRSSRequest(BaseModel):
    """Request body for the fetch_rss endpoint."""

    topics: list[TopicRequest]

    model_config = ConfigDict(extra="forbid")


class TopicFetchError(BaseModel):
    """Per-topic failure detail returned in a partial-success fetch response."""

    topic_id: str
    topic_name: str
    error: str

    model_config = ConfigDict(extra="forbid")


class FetchRSSResponse(BaseResponse[list[ArticleItem]]):
    """Response envelope for the fetch_rss endpoint.

    ``data`` contains the merged list of articles from all successfully
    fetched topics, ordered by ``pub_date`` descending (unpublished last).
    ``errors`` contains per-topic failure details when one or more topics
    could not be fetched or parsed.
    """

    errors: list[TopicFetchError] = []
