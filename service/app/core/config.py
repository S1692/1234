"""Configuration and environment handling for the service application."""

import os
from functools import lru_cache
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise RuntimeError(
                "DATABASE_URL environment variable is not set. Please provide a valid Supabase Session/Transaction Pooler URL."
            )

        # Ensure the scheme is correct for asyncpg
        parsed_url = urlparse(db_url)
        if parsed_url.scheme == "postgresql":
            parsed_url = parsed_url._replace(scheme="postgresql+asyncpg")

        # Enforce SSL mode if not present
        query_params = parse_qs(parsed_url.query)
        if "sslmode" not in query_params:
            query_params["sslmode"] = ["require"]

        # Rebuild the query string and the final URL
        new_query = urlencode(query_params, doseq=True)
        self.database_url = urlunparse(parsed_url._replace(query=new_query))


@lru_cache()
def get_settings() -> Settings:
    """Returns a cached Settings instance."""
    return Settings()
