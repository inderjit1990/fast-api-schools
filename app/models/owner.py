import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,Enum
from sqlalchemy.sql import func
from app.core.database import Base
from app.auth.password import hash_password


class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
    
class Owner(Base):
    __tablename__ = "owners"
    __table_args__ = {"schema": "public"}

    def generate_hashed_password(self):
        return hash_password(self.password)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True,nullable=False)
    email = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="Pending")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(DateTime(timezone=True), nullable=True)


