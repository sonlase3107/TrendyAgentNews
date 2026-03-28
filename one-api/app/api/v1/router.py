from fastapi import APIRouter

from app.api.v1.endpoints import calculation, health, rss

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(calculation.router)
api_v1_router.include_router(rss.router)
