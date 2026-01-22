from sqlalchemy.orm import Session
from fastapi import Request

from app.schemas.auth import LoginRequest
from app.services.auth_service import authenticate_tenant_user


def tenant_login_controller(
    db: Session,
    request: Request,
    payload: LoginRequest,
):
    token = authenticate_tenant_user(
        db=db,
        username=payload.username,
        password=payload.password,
        schema=request.state.schema,
    )
    return {"access_token": token}
