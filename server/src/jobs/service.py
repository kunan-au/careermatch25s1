import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import insert, select

from src.database import execute, fetch_one, jobs
from src.jobs.AISystemChain import get_recommendations_2
from src.users.service import get_user_profile


def format_job(job: dict) -> dict[str, Any]:
    return {
        "id": str(job["id"]),
        "title": job["title"],
        "company": job["company"],
        "job_type": job["job_type"],
        "description": job["description"],
        "created_at": job["created_at"].isoformat(),
        "updated_at": job["updated_at"].isoformat() if job["updated_at"] else None,
    }

async def get_by_id(id: str) -> dict[str, Any] | None:
    select_query = select(jobs).where(jobs.c.id == id)
    job = await fetch_one(select_query)
    formatted_job = format_job(job)
    print(formatted_job)
    return formatted_job if job else None

async def create_job(job: dict[str, Any]) -> dict[str, Any]:
    job_id = uuid.uuid4()
    insert_query = insert(jobs).values(
        id=job_id,
        title=job.title,
        company=job.company,
        job_type=job.job_type,
        description=job.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    await execute(insert_query)
    job = await get_by_id(job_id)
    return job

async def get_recommendations_by_email(email: str) -> list[dict[str, Any]]:
    user = await get_user_profile(email)
    if not user:
        return []
    # get pdf from s3 by http request
    print(user)
    print(f'https://careermatch-resume-2024.s3.ap-southeast-2.amazonaws.com/{user["resume"]}')
    recommendations = get_recommendations_2(f'https://careermatch-resume-2024.s3.ap-southeast-2.amazonaws.com/{user["resume"]}')
    print(recommendations)

    jobs = []
    for job_id in recommendations:
        job = await get_by_id(job_id)
        if job:
            jobs.append(job)
    return jobs
