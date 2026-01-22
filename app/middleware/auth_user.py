# app/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime
from app.core.database import get_db
from app.models import groups, owner
from app.auth.jwt import SECRET_KEY, ALGORITHM

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """JWT dependency - verifies token and returns user/group"""
    try:
        # Decode token
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        token_type: str = payload.get("type")
        user_id: str = payload.get("sub")
        
        if token_type == "group":
            group = db.query(groups.Group).filter(groups.Group.id == int(user_id)).first()
            if not group:
                raise HTTPException(status_code=401, detail="Invalid group token")
            return {"type": "group", "user": group}
        
        elif token_type == "owner":
            owner_rec = db.query(owner.Owner).filter(owner.Owner.id == int(user_id)).first()
            if not owner_rec:
                raise HTTPException(status_code=401, detail="Invalid owner token")
            return {"type": "owner", "user": owner_rec, "role": owner_rec.role.value}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Role-based access
async def require_admin(current_user = Depends(get_current_user)):
    """Only admins can access"""
    if current_user["type"] != "owner" or current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
