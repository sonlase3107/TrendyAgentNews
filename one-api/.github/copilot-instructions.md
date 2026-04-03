# ONE API Instructions


## Project context/purpose

- This is a REST API built with Python + FastAPI + SQLite
API Services will serve to a typical AI Agent naming ONE
- The AI AGENT targets to fetch automatically RSS Feeds from particular e-news and summarize insights
- No authentication required. Focus on business logic correctness.
- Bypass test components for MVP purpose

## Scope
These instructions apply to all code under the one-api FastAPI backend service.

## Stack
- Python 3.11
- FastAPI 0.110+
- Pydantic v2
- SQLite

## Architecture
- Place business logic in app/services.
- Keep API handlers in app/api/v1/endpoints as thin wrappers.
- Define all request and response models in app/schemas.
- Register new endpoint routers in app/api/v1/router.py.

## Architecture Constraints

- All business logics will live in app/services - routers are just thin wrappers
- ALL request/response types defined in app/schemas/ with Pydantic v2
- Routers return schemas directly — no raw dicts
- Async endpoints by default (async def)

## API Rules
- Async endpoints by default.
- Type hints required on all function signatures.
- Service methods include docstrings.
- Router decorators use explicit response_model values.
- Return schema objects, not raw dict payloads.

## Workflow of every domain implementation - Adding a new API domain (ALWAYS follow this sequence)
1. Create app/schemas/{domain}.py — define Request + Response models
2. Create app/services/{domain}.py — implement business logic
3. Create app/api/v1/endpoints/{domain}.py — create router, thin handlers
4. Register in app/api/v1/router.py

## Code conventions
- Type hints required on every function signature
- Docstring required on every service method
- Return explicit response_model in every router decorator
- Raise HTTPException with detail matching ErrorResponse schema
- **Python 3.11** with type hints required on all functions
- **FastAPI 0.110+** with async-by-default endpoints
- **Pydantic v2** (settings and models with `ConfigDict(extra="forbid")`)
- **SQLite** with context-managed connection pooling via `get_connection()`
- **Uvicorn** dev server (reload mode enabled)

## Architecture Overview

### Layered Structure
The codebase follows a **3-layer pattern** enforced across all domains:

1. **Schemas** (`app/schemas/{domain}.py`): Request/response models with Pydantic
2. **Services** (`app/services/{domain}.py`): Pure business logic, no FastAPI dependencies
3. **Endpoints** (`app/api/v1/endpoints/{domain}.py`): HTTP handlers as thin request→service→response wrappers

### Request/Response Envelope Pattern
**All API responses** use a standard envelope defined in `app/schemas/base.py`:
- **Success**: `BaseResponse[T]` with `success=True, message, data: T`
- **Error**: `ErrorResponse` with `success=False, message, error_code`

Use `app/core/responses.py` helpers (`success_response()`, `error_response()`) for consistency.

### Exception Handling
- Raise **domain-specific exceptions** from services (e.g., `CalculationException`, `RSSException`)
- Exceptions inherit from `AppException` with `code` and `message` attributes
- **Exception handlers** in `app/main.py` convert exceptions to standardized `ErrorResponse` envelopes
- HTTP errors, validation errors, and custom app exceptions all normalize to the same schema

### Configuration & Startup
- Settings loaded via `get_settings()` from environment vars with `ONE_API_` prefix (see `app/core/config.py`)
- Database tables created at startup via `init_db()` called in `@app.on_event("startup")`
- SQLite connection pattern: use `get_connection()` context manager to ensure cleanup

## Adding a New Domain

Follow this workflow to add a new API domain (e.g., "notifications"):

1. **Create schema** (`app/schemas/notifications.py`):
   - Define request models (e.g., `NotificationRequest`)
   - Define response/data models (e.g., `NotificationItem`)
   - Extend `BaseResponse[NotificationItem]` for response envelope

2. **Create service** (`app/services/notifications.py`):
   - Define `NotificationService` class with async/sync business methods
   - Include docstrings on all public methods
   - Raise domain exceptions (e.g., `NotificationException`)

3. **Create endpoint** (`app/api/v1/endpoints/notifications.py`):
   - Define `router = APIRouter(prefix="/notifications", tags=["notifications"])`
   - Instantiate service: `service = NotificationService()`
   - Keep handlers thin: validate input → call service → wrap response with `success_response()`

4. **Register router** in `app/api/v1/router.py`:
   - Add `from app.api.v1.endpoints import notifications`
   - Add `api_v1_router.include_router(notifications.router)`

## Key Patterns & Conventions

### Type Hints & Docstrings
- Type hints required on all function signatures (parameters and return types)
- Service methods must include docstrings explaining business logic (see `CalculationService.evaluate()`)
- Use `async def` for endpoint handlers; service methods can be sync if no I/O

### Pydantic Models
- All models use `model_config = ConfigDict(extra="forbid")` to reject unknown fields
- Use `Literal` types for enums (e.g., `Operation = Literal["add", "subtract", "multiply", "divide"]`)
- Use `Optional[T]` with defaults for nullable fields (don't use `|` union syntax)
- For raw text payloads, use `RootModel[str]` (see `ExtractRequest` in `app/schemas/calculation.py`)

### Database & Context Management
- Access SQLite via `get_connection()` context manager (yields `sqlite3.Connection`)
- Set `conn.row_factory = sqlite3.Row` for dict-like row access
- Always `conn.commit()` after write operations
- Connection automatically closes on context exit

### Router Registration
- Router decorators use explicit `response_model=SchemaClass` (not implicit)
- Media type handling: use `Body(..., media_type="text/plain")` for non-JSON payloads (see `extract_article`)
- All endpoints are async-first

## Development Workflow

- **Start dev server**: `uvicorn app.main:app --reload` (reloads on file changes)
- **Endpoints base**: All routes prefixed `/api/v1` (see router registration)
- **Debug middleware**: Request logging middleware in `app.main` logs raw request body for debugging

## MVP Constraints
- No authentication.
- Focus on correctness of domain logic.
- Skip test implementation for now.

## Project Structures
one-api/
├── .github/
│   └── copilot-instructions.md     ← The brain of Copilot Agent
│
├── app/
│   ├── main.py                      ← FastAPI app init, middleware
│   ├── core/
│   │   ├── config.py                ← Settings (pydantic-settings)
│   │   ├── exceptions.py            ← Custom exception classes
│   │   └── responses.py             ← Standard response wrappers
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py            ← Master router (register all sub-routers)
│   │       └── endpoints/
│   │           ├── health.py        ← /health endpoint
│   │           ├── calculation.py   ← Domain: calculations
│   │           └── {domain}.py      ← Add file = new API
│   │
│   ├── services/
│   │   ├── calculation.py           ← Business logic for calculation
│   │   └── {domain}.py              ← Mirror with endpoints/
│   │
│   └── schemas/
│       ├── base.py                  ← BaseResponse, ErrorResponse
│       ├── calculation.py           ← Request/Response models
│       └── {domain}.py              ← Mirror with endpoints/
│
├── pyproject.toml
└── README.md