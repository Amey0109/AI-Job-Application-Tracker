from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.dependencies import require_employer
from app.models.user import User
from app.models.employer import Employer
from app.schemas.employer import EmployerProfileCreate, EmployerProfileUpdate, EmployerProfileResponse

router = APIRouter(prefix="/employers", tags=["Employers"])


@router.post("/profile", response_model=EmployerProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: EmployerProfileCreate,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    # Check profile already exists
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employer profile already exists",
        )

    # Check slug is unique
    slug_result = await db.execute(select(Employer).where(Employer.company_slug == payload.company_slug))
    if slug_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company slug already taken",
        )

    employer = Employer(
        user_id=current_user.id,
        company_name=payload.company_name,
        company_slug=payload.company_slug,
        website=payload.website,
        industry=payload.industry,
        company_size=payload.company_size,
        description=payload.description,
        headquarters=payload.headquarters,
    )
    db.add(employer)
    await db.flush()
    await db.refresh(employer)
    return employer


@router.get("/profile", response_model=EmployerProfileResponse)
async def get_profile(
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer profile not found",
        )
    return employer


@router.patch("/profile", response_model=EmployerProfileResponse)
async def update_profile(
    payload: EmployerProfileUpdate,
    current_user: User = Depends(require_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employer).where(Employer.user_id == current_user.id))
    employer = result.scalar_one_or_none()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer profile not found",
        )

    # Update only fields that were sent
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employer, field, value)

    await db.flush()
    await db.refresh(employer)
    return employer