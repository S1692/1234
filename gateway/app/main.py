"""FastAPI reverse proxy for forwarding API requests to the service."""

import os

import httpx
from fastapi import FastAPI, Request, Response
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
    allow_origins=["*"],  # 필요 시 프론트 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Favicon 요청은 무시하여 불필요한 502 로그 방지
@app.get("/favicon.ico")
async def favicon() -> Response:
    return Response(status_code=204)


@app.get("/", summary="Gateway and service health")
async def root() -> Response:
    """
    Return gateway status and service health.
    - 서비스 호출 성공: {"gateway":"ok","service":{"db":"ok"}}
    - 서비스 호출 실패: {"gateway":"ok","service":{"status":"fail","detail":"..."}}
    """
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            # urljoin 대신 단순 문자열 결합 (루트 절대경로 덮어쓰기 이슈 방지)
            resp = await client.get(f"{SERVICE_BASE_URL}/")
            try:
                service_data = resp.json()
            except Exception:
                service_data = {"status": "fail", "detail": "Invalid JSON from service"}
            # 실패여도 200으로 내려 주고 내용에서 상태 확인 가능하게
            return JSONResponse(
                status_code=200,
                content={"gateway": "ok", "service": service_data},
            )
        except Exception as exc:
            return JSONResponse(
                status_code=200,
                content={"gateway": "ok", "service": {"status": "fail", "detail": str(exc)}},
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

    실패 시 200 + JSON으로 반환:
    {"status":"fail","detail":"..."}
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
            return JSONResponse(
                status_code=200,
                content={"status": "fail", "detail": f"Error forwarding request to service: {exc}"},
            )

    # 성공 시에는 원본 응답을 그대로 전달
    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
        media_type=resp.headers.get("content-type"),
    )
