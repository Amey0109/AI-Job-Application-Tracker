import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), unique=True, nullable=False)
    category = Column(String(80), nullable=True)
    aliases = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    job_skills = relationship("JobSkill", back_populates="skill")
    candidate_skills = relationship("CandidateSkill", back_populates="skill")