# ONE API Instructions


## Project context/purpose

- This is a REST API built with Python + FastAPI + SQLite
API Services will serve to a typical AI Agent naming ONE
- The AI AGENT targets to fetch automatically RSS Feeds from particular e-news and summarize insights
- No authentication required. Focus on business logic correctness.
- Bypass test components for MVP purpose

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