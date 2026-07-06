import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Text, Numeric, SmallInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_application_candidate_job"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="RESTRICT"), nullable=False, index=True)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), default="applied", nullable=False, index=True)
    cover_letter = Column(Text, nullable=True)
    match_score = Column(Numeric(5, 2), nullable=True)
    matched_skills = Column(JSONB, nullable=True)
    missing_skills = Column(JSONB, nullable=True)
    ai_summary = Column(Text, nullable=True)
    ai_processed_at = Column(DateTime(timezone=True), nullable=True)
    employer_notes = Column(Text, nullable=True)
    employer_rating = Column(SmallInteger, nullable=True)
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status_updated_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    candidate = relationship("Candidate", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")