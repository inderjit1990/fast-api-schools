from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SchoolSession(Base):
    __tablename__ = "school_sessions"
    __table_args__ = {"schema": "public"}

    def generate_schemaname(self):
        return f"schema_{self.school_id}_{self.session_year}"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("public.schools.id"))
    session_year = Column(Integer, nullable=False)
    schema_name = Column(String(63), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 👇 relationship
    school = relationship("School", back_populates="sessions")
