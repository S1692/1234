"""FastAPI reverse proxy for forwarding API requests to the service."""

import os
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import the new router for company-specific endpoints
from app.api import company_routes


# The base URL for the downstream backend service (e.g., the actual 'service' microservice)
# This is configured via an environment variable in the Railway deployment settings.
SERVICE_BASE_URL = os.getenv("SERVICE_BASE_URL")
if not SERVICE_BASE_URL:
    raise RuntimeError("SERVICE_BASE_URL environment variable is not set.")
SERVICE_BASE_URL = SERVICE_BASE_URL.rstrip("/")


app = FastAPI(title="Gateway")

# A list of allowed origins for CORS.
# This should include your frontend's production URL and local development URL.
allowed_origins = [
    "http://localhost:3000",  # Next.js local dev server
    "https://gateway-service-production-dcfc.up.railway.app", # The gateway itself
    # TODO: Add your Vercel frontend's production URL here
    # "https://your-app-name.vercel.app",
]


# === Middleware ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Register Routers ===
# The new company-specific router is included first to ensure its routes
# are matched before the generic proxy catch-all route.
app.include_router(company_routes.router)


# === Health & Favicon Routes ===

# The Next.js dev server might request this. Returning 204 No Content is a clean way to handle it.
@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)

# Health check for the gateway itself and the downstream service it connects to.
@app.get("/", summary="Gateway and service health")
async def root() -> Response:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{SERVICE_BASE_URL}/") # Checks if the downstream service is reachable
            service_data = resp.json() if resp.status_code == 200 else {"status": "fail", "detail": resp.text}
            return JSONResponse(
                status_code=200,
                content={"gateway": "ok", "service": service_data},
            )
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"gateway": "ok", "service": {"status": "fail", "detail": str(exc)}},
        )


# === Generic Proxy Route ===
# This route acts as a general-purpose reverse proxy.
# It catches all requests under /api/ that haven't been matched by a more specific router.
@app.api_route(
    "/api/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    summary="Generic proxy for all other API requests",
    include_in_schema=False, # Hide from OpenAPI docs if it's just a proxy
)
async def proxy_api(full_path: str, request: Request) -> Response:
    """
    Proxies requests from /api/{full_path} to {SERVICE_BASE_URL}/{full_path}.
    For example, a request to /api/items will be forwarded to http://service/items.
    """
    target_url = f"{SERVICE_BASE_URL}/{full_path.lstrip('/')}"

    headers = dict(request.headers)
    headers.pop("host", None) # The host header should be for the target service.

    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                headers=headers,
                content=body,
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                status_code=503,
                content={"status": "fail", "detail": f"Error forwarding request: {exc}"},
            )

    # Clean up response headers before sending back to the client
    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
        media_type=resp.headers.get("content-type"),
    )
