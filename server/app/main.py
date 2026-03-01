"""FastAPI application entry point."""

from fastapi import FastAPI

from server.app.api.router import api_router

app = FastAPI(title="GraphLens API", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")
