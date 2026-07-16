from pydantic import BaseModel
from typing import Optional
from enum import Enum
import uuid


class CompanySize(str, Enum):
    micro = "1-10"
    small = "11-50"
    medium = "51-200"
    large = "201-500"
    enterprise = "500+"


class Industry(str, Enum):
    software = "Software"
    finance = "Finance"
    healthcare = "Healthcare"
    education = "Education"
    ecommerce = "E-Commerce"
    manufacturing = "Manufacturing"
    consulting = "Consulting"
    media = "Media"
    telecom = "Telecom"
    real_estate = "Real Estate"
    logistics = "Logistics"
    hospitality = "Hospitality"
    legal = "Legal"
    government = "Government"
    nonprofit = "Non-Profit"
    other = "Other"


class EmployerProfileCreate(BaseModel):
    company_name: str
    company_slug: str
    website: Optional[str] = None
    industry: Optional[Industry] = None
    company_size: Optional[CompanySize] = None
    description: Optional[str] = None
    headquarters: Optional[str] = None


class EmployerProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[Industry] = None
    company_size: Optional[CompanySize] = None
    description: Optional[str] = None
    headquarters: Optional[str] = None


class EmployerProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    company_name: str
    company_slug: str
    website: Optional[str] = None
    industry: Optional[Industry] = None
    company_size: Optional[CompanySize] = None
    description: Optional[str] = None
    headquarters: Optional[str] = None
    is_verified: bool

    model_config = {"from_attributes": True}