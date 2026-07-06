from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="AI Job Application Tracker",
    description="Two-sided platform for employers and candidates with AI-powered matching",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


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