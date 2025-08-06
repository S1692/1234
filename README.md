# Full Stack Template Project

이 프로젝트는 **Next.js 14 (App Router)**, **FastAPI**, 그리고 **Supabase PostgreSQL**을 활용한 풀스택 템플릿입니다. 프론트엔드는 Vercel에, 게이트웨이와 서비스는 Railway에 배포하도록 설계되었습니다. 로컬 개발을 위해 `docker-compose.yml`이 제공됩니다.

## 주요 구성

- **frontend/** – Next.js 14 SPA 애플리케이션. 입력창을 통해 아이템을 추가하고 목록을 조회/삭제할 수 있습니다. 상단에는 데이터베이스 상태를 나타내는 뱃지가 표시됩니다.
- **gateway/** – FastAPI 기반 리버스 프록시입니다. `/` 경로로 서비스 헬스체크를 수행하고 `/api/*` 경로의 모든 요청을 서비스에 프록시합니다.
- **service/** – FastAPI + SQLAlchemy(Async) 서비스입니다. `items` 테이블에 대한 생성/조회/삭제 API를 제공합니다. 애플리케이션 시작 시 테이블이 존재하지 않으면 자동으로 생성합니다.

## 환경 변수

모든 환경 변수는 배포 시 반드시 설정해야 합니다. 로컬 개발 시에는 `.env` 파일을 작성하거나 `docker-compose` 실행 시 전달할 수 있습니다.

| 변수명 | 설명 | 사용 위치 |
| --- | --- | --- |
| `DATABASE_URL` | **Supabase IPv4 compatible Session/Transaction Pooler URL**. 반드시 `postgresql+asyncpg://` 스킴을 사용해야 합니다. 필요 시 코드에서 자동으로 `postgresql://` → `postgresql+asyncpg://`로 변환합니다. | service |
| `SERVICE_BASE_URL` | 서비스의 Base URL (예: `https://<service-app>.railway.app`). 게이트웨이가 이 URL로 모든 `/api/*` 요청을 전달합니다. | gateway |
| `NEXT_PUBLIC_API_BASE` | 게이트웨이의 Base URL (예: `https://<gateway-app>.railway.app`). 프론트엔드가 이 URL을 사용해 API를 호출합니다. | frontend |

`.env.example` 파일을 참고하여 `.env` 파일을 만들어 사용할 수 있습니다.

## 로컬 개발

로컬에서 전체 스택을 실행하려면 Docker가 필요합니다. `docker-compose.yml`을 이용해 service와 gateway를 실행할 수 있습니다. 프론트엔드는 Node.js 환경에서 직접 실행합니다.

1. `.env` 파일을 생성하고 `DATABASE_URL`에 로컬 또는 Supabase 세션 풀러 URL을 설정합니다. `SERVICE_BASE_URL`은 도커 네트워크에서 service 컨테이너로 접근하기 위해 `http://service:8000`으로 설정합니다.
2. `docker-compose up --build` 명령으로 gateway와 service를 빌드 및 실행합니다. service는 8001 포트에, gateway는 8000 포트에 매핑됩니다.
3. 프론트엔드 디렉터리에서 `npm install` 후 `npm run dev`를 실행합니다. `.env` 파일에 `NEXT_PUBLIC_API_BASE=http://localhost:8000`을 설정하면 로컬 gateway를 통해 API를 호출합니다.

## 배포 가이드

### 1. GitHub 저장소 준비

모든 소스코드를 GitHub 저장소에 푸시합니다. Railway와 Vercel은 GitHub 연동을 통해 자동 배포를 지원합니다.

### 2. Railway – service 배포

1. Railway에서 새로운 프로젝트를 생성한 후 **service** 디렉터리를 서브 디렉터리로 지정하여 GitHub 저장소와 연동합니다.
2. 환경 변수 `DATABASE_URL`을 **Supabase의 IPv4 compatible Pooler URL**로 설정합니다. **직접 접속(IPv6 전용) URL은 사용하지 않습니다.**
3. Deploy를 실행하면 Railway가 `Dockerfile`을 빌드하고 애플리케이션을 배포합니다.
4. 배포가 완료되면 서비스의 베이스 URL을 확인합니다. `/` 경로를 호출했을 때 `{"db":"ok"}` 형태의 응답이 나오면 정상입니다.

### 3. Railway – gateway 배포

1. 새 Railway 프로젝트를 생성하고 **gateway** 디렉터리를 연동합니다.
2. 환경 변수 `SERVICE_BASE_URL`을 앞서 배포된 service의 URL로 설정합니다.
3. Deploy를 실행합니다. `/` 경로를 호출하면 `{"gateway":"ok","service":{"db":"ok"}}` 형태로 응답해야 합니다.

### 4. Vercel – frontend 배포

1. Vercel에서 새 프로젝트를 만들고 **frontend** 디렉터리를 연동합니다.
2. 환경 변수 `NEXT_PUBLIC_API_BASE`를 앞서 배포된 gateway의 URL로 설정합니다.
3. Vercel이 제공하는 기본 빌드 명령과 설정으로 배포합니다. 배포 완료 후 웹 페이지에서 아이템 추가/조회/삭제 및 DB 상태 뱃지를 확인합니다.

### 중요 사항

- **Supabase Direct Connection(IPv6 전용)** URL은 사용하지 마십시오. Railway는 IPv4만 지원하므로 반드시 IPv4 compatible Pooler URL을 사용해야 합니다.
- `DATABASE_URL`이 `postgresql://` 스킴인 경우 서비스에서는 이를 자동으로 `postgresql+asyncpg://`로 변환하여 asyncpg 드라이버로 연결합니다.
- 서비스와 게이트웨이에서 환경 변수가 누락되면 명확한 에러 메시지를 반환하거나 500 응답을 제공합니다.

## API 요약

### Service

- `GET /` – DB 헬스체크. 데이터베이스에 `SELECT 1` 쿼리를 실행하여 성공하면 `{ "db": "ok" }` 반환, 실패하면 500 오류 JSON.
- `GET /items` – 모든 아이템을 배열로 반환. 각 아이템은 `{ id, name, created_at }` 형식입니다.
- `POST /items` – `{ name }` JSON을 받아 새 아이템을 생성하고 전체 레코드를 반환합니다.
- `DELETE /items/{id}` – 지정한 `id`의 아이템을 삭제합니다. 존재하지 않으면 404 오류를 반환합니다.

### Gateway

- `GET /` – 게이트웨이와 서비스의 상태를 반환. `{ "gateway": "ok", "service": { ... } }` 형식.
- `/*` – 기타 모든 경로는 `/api/*` 패턴으로 서비스에 프록시됩니다. HTTP 메서드, 쿼리, 헤더, 바디를 그대로 전달합니다.

## 검증 체크리스트

이 프로젝트를 배포한 후 다음 사항을 확인합니다:

- Gateway `/` 호출 시 `{"gateway":"ok","service":{"db":"ok"}}` 형태의 응답을 확인.
- Service `/` 호출 시 `{"db":"ok"}` 응답을 확인.
- `/api/items` GET/POST/DELETE 요청이 정상 동작하며 아이템이 적절히 추가/조회/삭제되는지 확인.
- Supabase Direct Connection을 사용하지 않고 IPv4 compatible Pooler URL을 사용했는지 확인.
- GitHub → Railway/Vercel 연동을 통해 자동 배포가 성공했는지 확인.
