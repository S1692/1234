"""Health check endpoint for the service."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_session


router = APIRouter()


@router.get("/", summary="Health check", tags=["health"])
async def health_check(session: AsyncSession = Depends(get_session)):
    """
    Executes a simple SELECT 1 to verify the database connection.
    Returns `{ "db": "ok" }` on success or a JSON error object on failure.
    """
    try:
        # Attempt to run a trivial query
        await session.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as exc:
        # Return error details as JSON with 500 status
        return JSONResponse(
            status_code=500,
            content={"db": "error", "detail": str(exc)},
        )
