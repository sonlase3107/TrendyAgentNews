from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, RootModel

from app.schemas.base import BaseResponse

Operation = Literal["add", "subtract", "multiply", "divide"]


class CalculationRequest(BaseModel):
    """Input payload for performing a calculation."""

    left: float
    right: float
    operation: Operation

    model_config = ConfigDict(extra="forbid")


class CalculationResult(BaseModel):
    """Result payload of a calculation operation."""

    operation: Operation
    value: float

    model_config = ConfigDict(extra="forbid")


class CalculationResponse(BaseResponse[CalculationResult]):
    """Calculation response envelope."""


# --- Article extraction models ---

class ExtractRequest(RootModel[str]):
    """Raw plain-text request body containing RSS XML content."""


class ArticleItem(BaseModel):
    """Flat output model for a single parsed article."""

    title: str
    url: str
    pub_date: Optional[datetime] = None
    description: Optional[str] = None
    source_name: Optional[str] = None
    guid: Optional[str] = None
    summary: Optional[str] = None
    key_points: list[str] = []
    sentiment: Optional[str] = None
    relevance_score: Optional[float] = None
    media_count: int = 0

    model_config = ConfigDict(extra="forbid")


class ExtractArticlesResponse(BaseResponse[list[ArticleItem]]):
    """Envelope for a list of parsed ArticleItem objects."""
