"""FastAPI reverse proxy for forwarding API requests to the service."""

import os
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import the new router for company-specific endpoints
from app.api import company_routes


# 환경변수에서 서비스 주소 가져오기
def get_service_base_url() -> str:
    base_url = os.getenv("SERVICE_BASE_URL")
    if not base_url:
        raise RuntimeError("SERVICE_BASE_URL is not set.")
    return base_url.rstrip("/")  # 슬래시 제거


SERVICE_BASE_URL = get_service_base_url()

app = FastAPI(title="Gateway")

# === Register Routers ===
# The new company-specific router is included first to ensure its routes
# are matched before the generic proxy catch-all route.
app.include_router(company_routes.router)


# === Middleware ===
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트 주소로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# favicon 방지
@app.get("/favicon.ico")
async def favicon() -> Response:
    return Response(status_code=204)

# 헬스 체크
@app.get("/", summary="Gateway and service health")
async def root() -> Response:
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(f"{SERVICE_BASE_URL}/")
            try:
                service_data = resp.json()
            except Exception:
                service_data = {"status": "fail", "detail": "Invalid JSON from service"}
            return JSONResponse(
                status_code=200,
                content={"gateway": "ok", "service": service_data},
            )
    except Exception as exc:
        return JSONResponse(
            status_code=200,
            content={"gateway": "ok", "service": {"status": "fail", "detail": str(exc)}},
        )


# 프록시 라우터: /api/ 이하 모든 요청 전달
@app.api_route(
    "/api/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    summary="Proxy API requests to the service",
)
async def proxy_api(full_path: str, request: Request) -> Response:
    target_url = f"{SERVICE_BASE_URL.rstrip('/')}/{full_path.lstrip('/')}"  # 중복 슬래시 방지

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
            return JSONResponse(
                status_code=200,
                content={"status": "fail", "detail": f"Error forwarding request: {exc}"},
            )

    # 제외할 응답 헤더
    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
        media_type=resp.headers.get("content-type"),
    )
