"""
Pydantic models for ReLaunchAI API.
Defines request/response schemas and data structures.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CareerBreakReason(str, Enum):
    """Enumeration of common career break reasons."""
    MATERNITY = "maternity"
    CHILDCARE = "childcare"
    ELDERCARE = "eldercare"
    HEALTH = "health"
    RELOCATION = "relocation"
    EDUCATION = "education"
    PERSONAL = "personal"
    OTHER = "other"


class UserProfile(BaseModel):
    """User profile input model."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    education: str = Field(..., min_length=1, description="Educational background")
    previous_role: str = Field(..., min_length=1, description="Previous job title/role")
    years_experience: int = Field(..., ge=0, le=50, description="Years of prior work experience")
    break_duration_months: int = Field(..., ge=1, le=240, description="Duration of career break in months")
    break_reason: CareerBreakReason = Field(..., description="Primary reason for career break")
    break_reason_details: Optional[str] = Field(default=None, max_length=500, description="Additional details about break")
    skills_known: List[str] = Field(..., min_length=1, description="List of known skills")
    target_role: str = Field(..., min_length=1, description="Desired/target job role")
    industry: Optional[str] = Field(default=None, description="Target industry")
    location: Optional[str] = Field(default=None, description="User's location for returnship programs")


class SkillGap(BaseModel):
    """Individual skill gap item."""
    skill_name: str
    importance: str = Field(..., description="High, Medium, or Low importance")
    gap_level: str = Field(..., description="Critical, Moderate, or Minor")
    learning_resources: List[str]
    estimated_time_weeks: int


class SkillGapAnalysis(BaseModel):
    """Skill gap analysis response."""
    transferable_skills: List[str]
    skill_gaps: List[SkillGap]
    upskilling_priority: List[str]
    market_trends_note: str


class ResumeSummary(BaseModel):
    """Generated resume summary."""
    professional_summary: str
    key_strengths: List[str]
    career_break_positioning: str
    suggested_headline: str


class InterviewAnswer(BaseModel):
    """Individual interview Q&A."""
    question: str
    answer: str
    tips: List[str]


class InterviewPrep(BaseModel):
    """Interview preparation package."""
    break_explanation: InterviewAnswer
    skill_refresh: InterviewAnswer
    motivation_return: InterviewAnswer
    handling_objections: InterviewAnswer
    general_tips: List[str]


class RoadmapTask(BaseModel):
    """Individual task in the roadmap."""
    day: int
    task: str
    category: str
    estimated_hours: float
    resources: List[str]


class WeeklyFocus(BaseModel):
    """Weekly focus area."""
    week: int
    theme: str
    objectives: List[str]


class ComebackRoadmap(BaseModel):
    """30-day comeback roadmap."""
    overview: str
    weekly_focus: List[WeeklyFocus]
    daily_tasks: List[RoadmapTask]
    milestones: List[str]


class ReturnshipProgram(BaseModel):
    """Returnship program details."""
    program_name: str
    company: str
    location: str
    duration: str
    description: str
    eligibility: str
    application_link: Optional[str] = None
    deadline: Optional[str] = None


class ReturnshipSuggestions(BaseModel):
    """Returnship program recommendations."""
    recommended_programs: List[ReturnshipProgram]
    general_advice: str
    networking_tips: List[str]


class AgentResponse(BaseModel):
    """Complete agent response with all modules."""
    user_name: str
    skill_gap_analysis: SkillGapAnalysis
    resume_summary: ResumeSummary
    interview_prep: InterviewPrep
    comeback_roadmap: ComebackRoadmap
    returnship_suggestions: ReturnshipSuggestions
    generated_at: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: str
