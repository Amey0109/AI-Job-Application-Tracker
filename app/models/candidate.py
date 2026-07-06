import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, Text, Numeric, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    headline = Column(String(300), nullable=True)
    location = Column(String(150), nullable=True)
    phone = Column(String(30), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    years_experience = Column(Numeric(4, 1), nullable=True)
    open_to_work = Column(Boolean, default=True, nullable=False)
    preferred_job_type = Column(String(50), nullable=True)
    preferred_remote = Column(String(50), nullable=True)
    salary_expectation_min = Column(Integer, nullable=True)
    salary_expectation_max = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="candidate")
    resumes = relationship("Resume", back_populates="candidate")
    skills = relationship("CandidateSkill", back_populates="candidate")
    applications = relationship("Application", back_populates="candidate")
    interviews = relationship("Interview", back_populates="candidate")