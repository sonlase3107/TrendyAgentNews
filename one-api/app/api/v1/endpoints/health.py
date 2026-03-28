from pydantic import BaseModel
from fastapi import APIRouter

from app.schemas.base import BaseResponse

router = APIRouter(tags=["health"])


class HealthData(BaseModel):
    """Payload returned by health endpoint."""

    status: str


@router.get("/health", response_model=BaseResponse[HealthData])
async def health_check() -> BaseResponse[HealthData]:
    """Return service liveness status."""
    return BaseResponse[HealthData](
        success=True,
        message="service is healthy",
        data=HealthData(status="ok"),
    )
