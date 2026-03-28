# ONE API Instructions

## Scope
These instructions apply to all code under one-api.

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

## API Rules
- Async endpoints by default.
- Type hints required on all function signatures.
- Service methods include docstrings.
- Router decorators use explicit response_model values.
- Return schema objects, not raw dict payloads.

## MVP Constraints
- No authentication.
- Focus on correctness of domain logic.
- Skip test implementation for now.
