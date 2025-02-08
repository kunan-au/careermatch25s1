from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4

from src.models import CustomModel


class JobType(str, Enum):
    FULL_TIME = "ft"
    PART_TIME = "pt"
    CONTRACT_TEMP = "ct"
    CASUAL_VACATION = "cv"

class JobBase(CustomModel):
    title: str
    company: str
    job_type: JobType
    description: str

class JobCreate(JobBase):
    pass

class JobUpdate(CustomModel):
    title: Optional[str] = None
    company: Optional[str] = None
    job_type: Optional[JobType] = None
    description: Optional[str] = None

class JobRead(JobBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
