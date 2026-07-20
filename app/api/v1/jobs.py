from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.dependencies import require_employer, get_current_user
from app.models.user import User
from app.models.employer import Employer
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobStatusUpdate, JobResponse
import uuid

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreate,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    # Get employer profile
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer profile not found. Create your company profile first.",
        )

    job = Job(
        employer_id=employer.id,
        title=payload.title,
        location=payload.location,
        job_type=payload.job_type,
        remote_type=payload.remote_type,
        salary_min=payload.salary_min,
        salary_max=payload.salary_max,
        description_raw=payload.description_raw,
        application_deadline=payload.application_deadline,
        status="draft",
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)
    return job


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role == "employer":
        # Employer sees their own jobs
        result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
        employer = result.scalar_one_or_none()
        if not employer:
            return []
        result = await db.execute(select(Job).where(Job.employer_id == employer.id))
    else:
        # Candidate sees all active jobs
        result = await db.execute(select(Job).where(Job.status == "active"))

    jobs = result.scalars().all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    # Increment view count for candidates
    if current_user.role == "candidate":
        job.views_count += 1
        await db.flush()

    return job


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    payload: JobUpdate,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()

    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if job.employer_id != employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your job")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    await db.flush()
    await db.refresh(job)
    return job


@router.patch("/{job_id}/status", response_model=JobResponse)
async def update_job_status(
    job_id: uuid.UUID,
    payload: JobStatusUpdate,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()

    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if job.employer_id != employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your job")

    job.status = payload.status
    await db.flush()
    await db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: uuid.UUID,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()

    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if job.employer_id != employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your job")

    await db.delete(job)