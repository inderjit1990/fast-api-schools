from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import groups , owner
from app.auth.password import verify_password
from app.auth.jwt import create_access_token


def authenticate_group(db: Session, username: str, password: str) -> str:
    group = (
        db.query(groups.Group.group)
        .filter(groups.Group.mobile == username)
        .first()
    )

    if not group or not verify_password(password, group.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token({
        "sub": str(group.id),
        "type": "group"
    })


def authenticate_admin(db: Session, phone: str, password: str) -> str:
    ownerRec = (
        db.query(owner.Owner)
        .filter(owner.Owner.phone == phone)
        .first()
    )

    if not ownerRec or not verify_password(password, ownerRec.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token({
        "sub": str(ownerRec.id),
        "type": "owner",
        "role": ownerRec.role.value
    })
