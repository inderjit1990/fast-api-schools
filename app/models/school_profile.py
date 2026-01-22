from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class SchoolProfile(Base):
    __tablename__ = "school_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    school_id = Column(Integer, nullable=False)
    mobile = Column(Integer, nullable=False)
    address = Column(String(63), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())