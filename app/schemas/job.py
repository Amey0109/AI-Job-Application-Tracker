from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date
import uuid


class JobType(str, Enum):
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"
    internship = "internship"
    freelance = "freelance"


class RemoteType(str, Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"


class JobStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    closed = "closed"


class JobCreate(BaseModel):
    title: str
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    remote_type: Optional[RemoteType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description_raw: str
    application_deadline: Optional[date] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    remote_type: Optional[RemoteType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description_raw: Optional[str] = None
    application_deadline: Optional[date] = None


class JobStatusUpdate(BaseModel):
    status: JobStatus


class JobResponse(BaseModel):
    id: uuid.UUID
    employer_id: uuid.UUID
    title: str
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    remote_type: Optional[RemoteType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description_raw: str
    description_summary: Optional[str] = None
    required_skills: Optional[dict] = None
    nice_to_have_skills: Optional[dict] = None
    status: JobStatus
    application_deadline: Optional[date] = None
    views_count: int
    ai_processed_at: Optional[str] = None

    model_config = {"from_attributes": True}