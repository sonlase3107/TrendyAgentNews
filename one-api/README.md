# ONE API

FastAPI-based backend for ONE agent workflows.

## Requirements
- Python 3.11

## Setup
1. Create and activate a Python 3.11 environment.
2. Install dependencies:
   pip install -e .

## Run
From the one-api directory:
uvicorn app.main:app --reload

## Endpoints
- GET /api/v1/health
- POST /api/v1/calculation/evaluate

## Domain Extension Workflow
1. Create app/schemas/{domain}.py
2. Create app/services/{domain}.py
3. Create app/api/v1/endpoints/{domain}.py
4. Register router in app/api/v1/router.py
