import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Text, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    employer_id = Column(UUID(as_uuid=True), ForeignKey("employers.id", ondelete="CASCADE"), nullable=False)
    round_number = Column(SmallInteger, nullable=False, default=1)
    interview_type = Column(String(60), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes = Column(SmallInteger, default=60, nullable=False)
    meeting_link = Column(Text, nullable=True)
    interviewer_names = Column(String(500), nullable=True)
    status = Column(String(30), default="scheduled", nullable=False)
    prep_notes = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    outcome = Column(String(30), nullable=True)
    reminder_sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    application = relationship("Application", back_populates="interviews")
    candidate = relationship("Candidate", back_populates="interviews")
    employer = relationship("Employer", back_populates="interviews")