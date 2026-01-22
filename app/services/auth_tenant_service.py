from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.tenant.user import User
from app.auth.password import verify_password
from app.auth.jwt import create_access_token


def authenticate_tenant_user(
    db: Session,
    username: str,
    password: str,
    schema: str,
) -> str:
    user = (
        db.query(User)
        .filter(User.username == username, User.is_active == True)
        .first()
    )

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token({
        "sub": str(user.id),
        "role": user.role,
        "schema": schema,
        "type": "tenant",
    })
