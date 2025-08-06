"""FastAPI reverse proxy for forwarding API requests to the service."""

import os

import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


def get_service_base_url() -> str:
    base_url = os.getenv("SERVICE_BASE_URL")
    if not base_url:
        raise RuntimeError(
            "SERVICE_BASE_URL environment variable is not set. Please set it to the deployed service base URL."
        )
    return base_url.rstrip("/")


SERVICE_BASE_URL = get_service_base_url()

app = FastAPI(title="Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico")
async def favicon() -> Response:
    return Response(status_code=204)

@app.get("/", summary="Gateway and service health")
async def root() -> Response:
    """Return gateway status and proxy the service health check."""
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            # call service root health
            resp = await client.get(f"{SERVICE_BASE_URL}/")
            try:
                service_data = resp.json()
            except Exception:
                service_data = {"error": "Invalid response from service"}
            return JSONResponse(
                status_code=resp.status_code if resp.status_code < 500 else 500,
                content={"gateway": "ok", "service": service_data},
            )
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={
                    "gateway": "ok",
                    "service": {"db": "error", "detail": str(exc)},
                },
            )

@app.api_route(
    "/api/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    summary="Proxy API requests to the service",
)
async def proxy_api(full_path: str, request: Request) -> Response:
    """
    Forward any request starting with `/api/` to the service while preserving
    method, query parameters, headers and body.
    """
    target_url = f"{SERVICE_BASE_URL}/{full_path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                headers=headers,
                content=body,
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error forwarding request to service: {exc}",
            )
    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {
        k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers
    }
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
        media_type=resp.headers.get("content-type"),
    )
