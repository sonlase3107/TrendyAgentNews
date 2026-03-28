class AppException(Exception):
    """Base exception for application domain errors."""

    def __init__(self, message: str, code: str = "APP_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class CalculationException(AppException):
    """Raised when calculation business rules fail."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="CALCULATION_ERROR")


class RSSException(AppException):
    """Raised when an RSS operation fails (fetch, parse, or DB lookup)."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="RSS_ERROR")
