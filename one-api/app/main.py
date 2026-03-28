from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.db import init_db
from app.core.exceptions import AppException
from app.core.responses import error_response

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.on_event("startup")
def on_startup() -> None:
    """Initialise the SQLite database on application startup."""
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()

    print("=== REQUEST DEBUG ===")
    print("URL:", request.url)
    # print("METHOD:", request.method)
    # print("HEADERS:", dict(request.headers))
    print("BODY:", body.decode("utf-8"))
    print("RAW_BODY", body)
    print("=====================")

    response = await call_next(request)
    return response

@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    """Convert domain errors into standardized API responses."""
    payload = error_response(code=exc.code, message=exc.message)
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Convert validation errors into ErrorResponse envelope."""
    payload = error_response(code="VALIDATION_ERROR", message=str(exc))
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(HTTPException)
async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
    """Normalize FastAPI HTTPException output to standard error schema."""
    payload = error_response(code="HTTP_ERROR", message=str(exc.detail))
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


app.include_router(api_v1_router)
