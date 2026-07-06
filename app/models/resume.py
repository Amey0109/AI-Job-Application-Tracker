import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    storage_path = Column(Text, nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    mime_type = Column(String(80), nullable=False)
    extracted_text = Column(Text, nullable=True)
    ai_skills = Column(JSONB, nullable=True)
    ai_processed_at = Column(DateTime(timezone=True), nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    candidate = relationship("Candidate", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")