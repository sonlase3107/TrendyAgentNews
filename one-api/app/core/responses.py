from typing import Any

from app.schemas.base import BaseResponse, ErrorResponse


def success_response(data: Any, message: str = "ok") -> BaseResponse[Any]:
    """Build a consistent success envelope for API handlers."""
    return BaseResponse[Any](success=True, message=message, data=data)


def error_response(code: str, message: str) -> ErrorResponse:
    """Build a consistent error envelope for exception handlers."""
    return ErrorResponse(success=False, message=message, error_code=code)
