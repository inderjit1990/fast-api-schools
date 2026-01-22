from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.auth.password import hash_password


class School(Base):
    __tablename__ = "schools"
    __table_args__ = {"schema": "public"}

    def generate_username(self):
        return f"S{self.phone}"
    
    def generate_hashed_password(self):
        return hash_password(self.password)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subdomain = Column(String(50), unique=True, nullable=False)
    custom_domain = Column(String(100), unique=True, nullable=True)
    address = Column(String(255), nullable=False)
    phone = Column(String(15), unique=True,nullable=False)
    email = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="Pending")
    user_name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey("public.groups.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # 👇 relationship
    sessions = relationship(
        "SchoolSession",
        back_populates="school",
        lazy="selectin",
    )

    groups = relationship(
        "Group",
        back_populates="school",
        lazy="selectin",
    )

