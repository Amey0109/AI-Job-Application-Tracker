from pydantic import BaseModel
from typing import Optional
from enum import Enum
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
    any = "any"


class CandidateProfileCreate(BaseModel):
    full_name: str
    headline: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[float] = None
    open_to_work: bool = True
    preferred_job_type: Optional[JobType] = None
    preferred_remote: Optional[RemoteType] = None
    salary_expectation_min: Optional[int] = None
    salary_expectation_max: Optional[int] = None


class CandidateProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[float] = None
    open_to_work: Optional[bool] = None
    preferred_job_type: Optional[JobType] = None
    preferred_remote: Optional[RemoteType] = None
    salary_expectation_min: Optional[int] = None
    salary_expectation_max: Optional[int] = None


class CandidateProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    headline: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[float] = None
    open_to_work: bool
    preferred_job_type: Optional[JobType] = None
    preferred_remote: Optional[RemoteType] = None
    salary_expectation_min: Optional[int] = None
    salary_expectation_max: Optional[int] = None

    model_config = {"from_attributes": True}