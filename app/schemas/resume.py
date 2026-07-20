from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class ResumeResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    filename: str
    file_size_bytes: int
    mime_type: str
    is_default: bool
    ai_processed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}