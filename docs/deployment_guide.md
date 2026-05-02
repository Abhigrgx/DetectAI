# Deployment Guide (Docker + Cloud)

## Local Docker
1. Build and start:
```bash
docker compose up --build
```
2. Endpoints:
- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

## Environment Variables
Backend:
- `DATABASE_URL` (default: `sqlite:///./authentitext.db`)

Frontend:
- `VITE_API_BASE` (default: `http://localhost:8000`)

## Cloud Pattern
- Frontend static assets -> CDN/object storage
- FastAPI service -> container platform (AKS/EKS/Cloud Run/App Service)
- PostgreSQL managed service
- Centralized logs + metrics (OpenTelemetry compatible)

## Production Recommendations
- Restrict CORS origins.
- Enforce HTTPS and WAF.
- Add authentication and RBAC for analyst/admin actions.
- Add background queue for large file processing.
- Add model versioning and drift monitoring.
