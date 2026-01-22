from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Group(Base):
    __tablename__ = "groups"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    otp = Column(String(6), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 👇 relationship
    school = relationship("School", back_populates="groups", lazy="selectin")
