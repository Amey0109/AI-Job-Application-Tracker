import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Text, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employer_id = Column(UUID(as_uuid=True), ForeignKey("employers.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    location = Column(String(200), nullable=True)
    job_type = Column(String(50), nullable=True)
    remote_type = Column(String(50), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    description_raw = Column(Text, nullable=False)
    description_summary = Column(Text, nullable=True)
    required_skills = Column(JSONB, nullable=True)
    nice_to_have_skills = Column(JSONB, nullable=True)
    status = Column(String(30), default="draft", nullable=False, index=True)
    ai_processed_at = Column(DateTime(timezone=True), nullable=True)
    application_deadline = Column(Date, nullable=True)
    views_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    employer = relationship("Employer", back_populates="jobs")
    job_skills = relationship("JobSkill", back_populates="job")
    applications = relationship("Application", back_populates="job")