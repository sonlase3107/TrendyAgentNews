from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Standard success envelope for API responses."""

    success: bool
    message: str
    data: Optional[T] = None

    model_config = ConfigDict(extra="forbid")


class ErrorResponse(BaseModel):
    """Standard error envelope for API responses."""

    success: bool = False
    message: str
    error_code: str

    model_config = ConfigDict(extra="forbid")
