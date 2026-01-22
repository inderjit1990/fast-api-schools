from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.database import SessionLocal
from app.core.tenant import get_tenant_schema

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()
        try:
            schema = get_tenant_schema(request, db)
            request.state.schema_name = schema
        finally:
            db.close()

        response = await call_next(request)
        return response
