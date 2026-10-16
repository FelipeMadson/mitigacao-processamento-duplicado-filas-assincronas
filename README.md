# QueueGuard — Idempotent Message Queue & Deduplication Platform

Enterprise-grade asynchronous message deduplication platform built with **Angular 22**, **FastAPI**, and **PostgreSQL 18**.

## Architecture Overview

QueueGuard ensures exactly-once semantics across distributed asynchronous processing pipelines through transactional idempotency leases and cryptographic payload hashing.

- **Frontend**: Angular 22 standalone component architecture using `ChangeDetectionStrategy.OnPush`, fine-grained reactive Signals (`signal`, `computed`), WCAG AAA accessibility, responsive CSS (mobile, tablet, desktop).
- **Backend**: FastAPI with async PostgreSQL (Psycopg 3), Bearer token authentication, atomic lease acquisition, deduplication response caching, and isolated multi-tenant execution.
- **Database**: Relational migrations in PostgreSQL tracking `idempotent_keys`, `queue_messages`, and `audit_events`.
- **Testing**: Acceptance suite with Pytest, unit tests with Vitest, and end-to-end multi-viewport browser testing with Playwright (390px, 768px, 1440px).

## Getting Started

### Prerequisites

- Node.js 22+
- Python 3.12+
- PostgreSQL 16+

### Installation & Run

```bash
# Frontend
cd frontend
npm ci
npm run build

# Backend
cd ../backend
python -m pip install -r requirements.txt
uvicorn src.app.main:app --port 8000
```

## License

MIT © Felipe Madison (@FelipeMadson)
