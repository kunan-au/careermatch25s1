from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import OperationalError

from src.jobs import service
from src.jobs.schemas import JobCreate, JobRead

router = APIRouter()

@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: str) -> dict[str, str]:
    job = await service.get_by_id(job_id)
    return job

@router.post("/")
async def create_job(job: JobCreate) -> dict[str, str]:
    try:
        job = await service.create_job(job)
        return job
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database is not available")

@router.get("/recommendations/{email}", response_model=List[JobRead])
async def get_recommendations(email: str) -> List[JobRead]:
    jobs = await service.get_recommendations_by_email(email)
    return jobs
