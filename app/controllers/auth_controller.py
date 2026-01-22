from sqlalchemy.orm import Session

from app.schemas.auth import AdminLoginRequest, GroupLoginRequest
from app.services.auth_service import authenticate_group, authenticate_admin


def auth_login_controller(db: Session, payload: AdminLoginRequest):
    token = authenticate_admin(
        db=db,
        phone=payload.phone,
        password=payload.password,
    )
    return {"access_token": token}


def auth_group_controller(db: Session, payload: GroupLoginRequest):
    token = authenticate_group(
        db=db,
        username=payload.username,
        password=payload.password,
    )
    return {"access_token": token}
