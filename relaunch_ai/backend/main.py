"""
FastAPI Backend for ReLaunchAI
Main application entry point with API routes.
"""

import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.models import (
    UserProfile, 
    AgentResponse, 
    HealthResponse,
    SkillGapAnalysis,
    ResumeSummary,
    InterviewPrep,
    ComebackRoadmap,
    ReturnshipSuggestions
)
from backend.agent import run_agent_pipeline
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered career reintegration assistant for women returning after career breaks",
    version=settings.app_version,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API information."""
    return HealthResponse(
        status="operational",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/api/analyze", response_model=AgentResponse)
async def analyze_profile(profile: UserProfile):
    """
    Run complete AI analysis pipeline on user profile.
    
    This endpoint processes the user profile through all AI modules:
    - Skill Gap Analysis
    - Resume Summary Generation
    - Interview Answer Generation
    - 30-Day Roadmap Creation
    - Returnship Program Suggestions
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        AgentResponse with all generated content
    """
    try:
        logger.info(f"Received analysis request for user: {profile.name}")
        result = run_agent_pipeline(profile)
        logger.info(f"Analysis completed for user: {profile.name}")
        return result
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/api/skill-gap", response_model=SkillGapAnalysis)
async def analyze_skills_only(profile: UserProfile):
    """
    Analyze skill gaps only.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        SkillGapAnalysis with skill recommendations
    """
    from backend.services import analyze_skill_gaps
    
    try:
        logger.info(f"Skill gap analysis for: {profile.name}")
        return analyze_skill_gaps(profile)
    except Exception as e:
        logger.error(f"Skill gap analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/resume", response_model=ResumeSummary)
async def generate_resume_only(profile: UserProfile):
    """
    Generate resume summary only.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        ResumeSummary with generated content
    """
    from backend.services import generate_resume_summary
    
    try:
        logger.info(f"Resume generation for: {profile.name}")
        return generate_resume_summary(profile)
    except Exception as e:
        logger.error(f"Resume generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/interview", response_model=InterviewPrep)
async def generate_interview_only(profile: UserProfile):
    """
    Generate interview answers only.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        InterviewPrep with Q&A content
    """
    from backend.services import generate_interview_answers
    
    try:
        logger.info(f"Interview prep for: {profile.name}")
        return generate_interview_answers(profile)
    except Exception as e:
        logger.error(f"Interview prep failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/roadmap", response_model=ComebackRoadmap)
async def create_roadmap_only(profile: UserProfile):
    """
    Create 30-day roadmap only.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        ComebackRoadmap with structured plan
    """
    from backend.services import create_roadmap
    
    try:
        logger.info(f"Roadmap creation for: {profile.name}")
        return create_roadmap(profile)
    except Exception as e:
        logger.error(f"Roadmap creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/returnships", response_model=ReturnshipSuggestions)
async def find_returnships_only(profile: UserProfile):
    """
    Find returnship programs only.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        ReturnshipSuggestions with program recommendations
    """
    from backend.services import find_returnship_programs
    
    try:
        logger.info(f"Returnship search for: {profile.name}")
        return find_returnship_programs(profile)
    except Exception as e:
        logger.error(f"Returnship search failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
