from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import AdminLoginRequest, TokenResponse ,GroupLoginRequest
from app.controllers.auth_controller import auth_login_controller , auth_group_controller
from app.core.database import get_public_db

router = APIRouter(prefix="/auth", tags=["Group Auth"])


@router.post("/login/owner", response_model=TokenResponse)
def group_login(
    payload: AdminLoginRequest,
    db: Session = Depends(get_public_db),
):
    return auth_login_controller(db, payload)


@router.post("/login/group", response_model=TokenResponse)
def group_login(
    payload: GroupLoginRequest,
    db: Session = Depends(get_public_db),
):
    return auth_group_controller(db, payload)
