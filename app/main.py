from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.employers import router as employers_router
from app.api.v1.candidates import router as candidates_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.applications import router as applications_router

app = FastAPI(
    title="AI Job Application Tracker",
    description="Two-sided platform for employers and candidates with AI-powered matching",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(employers_router, prefix="/api/v1")
app.include_router(candidates_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(resumes_router, prefix="/api/v1")
app.include_router(applications_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    return {"message": "AI Job Application Tracker API"}