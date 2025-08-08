"""FastAPI application entry point for the service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, items
from .core.db import init_db


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Service API")

    # CORS configuration – allow all origins (modify as needed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router)
    app.include_router(items.router)

    # Startup event to initialize the database
    @app.on_event("startup")
    async def on_startup() -> None:
        await init_db()

    return app


app = create_app()
