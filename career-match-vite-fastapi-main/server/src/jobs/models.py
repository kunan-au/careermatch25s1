from uuid import uuid4

from sqlalchemy import CHAR, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from src.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    job_type = Column(CHAR(2), nullable=False)  # full-time: ft, part-time: pt, contract/temp: ct, casual/vacation: cv
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
