from pydantic import BaseModel
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime


class ApplicationStatus(str, Enum):
    applied = "applied"
    reviewed = "reviewed"
    shortlisted = "shortlisted"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    withdrawn = "withdrawn"


class ApplicationCreate(BaseModel):
    job_id: uuid.UUID
    resume_id: Optional[uuid.UUID] = None
    cover_letter: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    resume_id: Optional[uuid.UUID] = None
    status: ApplicationStatus
    cover_letter: Optional[str] = None
    match_score: Optional[float] = None
    matched_skills: Optional[dict] = None
    missing_skills: Optional[dict] = None
    ai_summary: Optional[str] = None
    ai_processed_at: Optional[datetime] = None
    applied_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationEmployerResponse(ApplicationResponse):
    employer_notes: Optional[str] = None
    employer_rating: Optional[int] = None