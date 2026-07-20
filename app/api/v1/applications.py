from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.dependencies import require_candidate, require_employer, get_current_user
from app.models.user import User
from app.models.employer import Employer
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.models.resume import Resume
from app.schemas.application import ApplicationCreate, ApplicationStatusUpdate, ApplicationResponse, ApplicationEmployerResponse
import uuid

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    payload: ApplicationCreate,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    # Get candidate profile
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    # Check job exists and is active
    result = await db.execute(select(Job).where(Job.id == payload.job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job is not accepting applications",
        )

    # Check already applied
    result = await db.execute(
        select(Application).where(
            Application.candidate_id == candidate.id,
            Application.job_id == payload.job_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied to this job",
        )

    # Validate resume belongs to candidate
    resume_id = payload.resume_id
    if resume_id:
        result = await db.execute(select(Resume).where(Resume.id == resume_id))
        resume = result.scalar_one_or_none()
        if not resume or resume.candidate_id != candidate.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resume",
            )
    else:
        # Use default resume
        result = await db.execute(
            select(Resume).where(
                Resume.candidate_id == candidate.id,
                Resume.is_default == True,
            )
        )
        default_resume = result.scalar_one_or_none()
        resume_id = default_resume.id if default_resume else None

    application = Application(
        candidate_id=candidate.id,
        job_id=payload.job_id,
        resume_id=resume_id,
        cover_letter=payload.cover_letter,
        status="applied",
    )
    db.add(application)
    await db.flush()
    await db.refresh(application)
    return application


@router.get("/", response_model=list[ApplicationResponse])
async def list_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role == "candidate":
        result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
        candidate = result.scalar_one_or_none()
        if not candidate:
            return []
        result = await db.execute(
            select(Application).where(Application.candidate_id == candidate.id)
        )
    else:
        # Employer sees applications for their jobs
        result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
        employer = result.scalar_one_or_none()
        if not employer:
            return []
        result = await db.execute(
            select(Application).join(Job).where(Job.employer_id == employer.id)
        )

    applications = result.scalars().all()
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Application).where(Application.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    if current_user.role == "candidate":
        result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
        candidate = result.scalar_one_or_none()
        if application.candidate_id != candidate.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your application")
    else:
        result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
        employer = result.scalar_one_or_none()
        result = await db.execute(select(Job).where(Job.id == application.job_id))
        job = result.scalar_one_or_none()
        if job.employer_id != employer.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your job")

    return application


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: uuid.UUID,
    payload: ApplicationStatusUpdate,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()

    result = await db.execute(select(Application).where(Application.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    result = await db.execute(select(Job).where(Job.id == application.job_id))
    job = result.scalar_one_or_none()
    if job.employer_id != employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your job")

    application.status = payload.status
    await db.flush()
    await db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_application(
    application_id: uuid.UUID,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    candidate = result.scalar_one_or_none()

    result = await db.execute(select(Application).where(Application.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    if application.candidate_id != candidate.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your application")

    await db.delete(application)