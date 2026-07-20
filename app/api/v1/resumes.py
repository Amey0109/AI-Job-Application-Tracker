from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.dependencies import require_candidate
from app.core.config import settings
from app.models.user import User
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse
import uuid
import os
import shutil

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    # Validate mime type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    # Validate file size
    contents = await file.read()
    if len(contents) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit",
        )

    # Get candidate profile
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found. Create your profile first.",
        )

    # Save file to local storage
    file_id = uuid.uuid4()
    filename = f"{file_id}_{file.filename}"
    storage_path = os.path.join("uploads", "resumes", filename)

    with open(storage_path, "wb") as f:
        f.write(contents)

    # Check if this is the first resume — make it default
    existing_result = await db.execute(
        select(Resume).where(Resume.candidate_id == candidate.id)
    )
    existing_resumes = existing_result.scalars().all()
    is_default = len(existing_resumes) == 0

    # Save to database
    resume = Resume(
        candidate_id=candidate.id,
        filename=file.filename,
        storage_path=storage_path,
        file_size_bytes=len(contents),
        mime_type=file.content_type,
        is_default=is_default,
    )
    db.add(resume)
    await db.flush()
    await db.refresh(resume)
    return resume


@router.get("/", response_model=list[ResumeResponse])
async def list_resumes(
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

    result = await db.execute(
        select(Resume).where(Resume.candidate_id == candidate.id)
    )
    resumes = result.scalars().all()
    return resumes


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: uuid.UUID,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.user_id == current_user.id))
    candidate = result.scalar_one_or_none()

    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    if resume.candidate_id != candidate.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your resume")

    # Delete file from local storage
    if os.path.exists(resume.storage_path):
        os.remove(resume.storage_path)

    await db.delete(resume)