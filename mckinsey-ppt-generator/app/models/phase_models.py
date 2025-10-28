from pydantic import BaseModel, Field
from typing import Optional, Dict


class PhaseRequest(BaseModel):
    project_id: str = Field(...)
    document: Optional[str] = None
    num_slides: Optional[int] = 10
    language: Optional[str] = "ko"


class PhaseResponse(BaseModel):
    project_id: str
    phase: str
    status: str
    result: Dict
    timestamp: Optional[str] = None

