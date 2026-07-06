import uuid
from sqlalchemy import Column, ForeignKey, DateTime, func, SmallInteger, String, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    __table_args__ = (
        UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skills"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    source = Column(String(20), nullable=False)
    proficiency_level = Column(SmallInteger, nullable=True)
    years_experience = Column(Numeric(4, 1), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    candidate = relationship("Candidate", back_populates="skills")
    skill = relationship("Skill", back_populates="candidate_skills")