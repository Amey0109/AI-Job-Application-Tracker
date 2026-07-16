from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.dependencies import require_candidate
from app.models.user import User
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateProfileCreate, CandidateProfileUpdate, CandidateProfileResponse

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post("/profile", response_model=CandidateProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: CandidateProfileCreate,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    # Check profile already exists
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate profile already exists",
        )

    candidate = Candidate(
        user_id=current_user.id,
        full_name=payload.full_name,
        headline=payload.headline,
        location=payload.location,
        phone=payload.phone,
        linkedin_url=payload.linkedin_url,
        github_url=payload.github_url,
        bio=payload.bio,
        years_experience=payload.years_experience,
        open_to_work=payload.open_to_work,
        preferred_job_type=payload.preferred_job_type,
        preferred_remote=payload.preferred_remote,
        salary_expectation_min=payload.salary_expectation_min,
        salary_expectation_max=payload.salary_expectation_max,
    )
    db.add(candidate)
    await db.flush()
    await db.refresh(candidate)
    return candidate


@router.get("/profile", response_model=CandidateProfileResponse)
async def get_profile(
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )
    return candidate


@router.patch("/profile", response_model=CandidateProfileResponse)
async def update_profile(
    payload: CandidateProfileUpdate,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)

    await db.flush()
    await db.refresh(candidate)
    return candidate