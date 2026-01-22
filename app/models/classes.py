from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 👇 relationship
    sections = relationship(
        "Sections",
        back_populates="classes",
        lazy="selectin",
    )
    students = relationship(
        "Student",
        back_populates="classes",
        lazy="selectin",
    )