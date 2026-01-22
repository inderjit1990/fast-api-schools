from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, TokenResponse
from app.controllers.auth_tenant_controller import tenant_login_controller
from app.core.database import get_tenant_db

router = APIRouter(prefix="/auth", tags=["Tenant Auth"])


@router.post("/login", response_model=TokenResponse)
def tenant_login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_tenant_db),
):
    return tenant_login_controller(db, request, payload)
