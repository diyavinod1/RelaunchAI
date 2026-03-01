"""
Roadmap Planner Service
Creates a structured 30-day comeback plan with daily tasks and milestones.
"""

import json
import logging
import re
from backend.config import get_ai_client, settings
from backend.models import ComebackRoadmap, RoadmapTask, WeeklyFocus, UserProfile

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert career transition coach specializing in structured comeback plans for returning professionals.

Your task is to create a detailed, actionable 30-day roadmap that includes:
1. Weekly themes and focus areas
2. Daily actionable tasks
3. Realistic time commitments
4. Specific resources and tools
5. Clear milestones and checkpoints

Guidelines:
- Tasks should be specific and actionable
- Balance between different activities (networking, skills, applications)
- Include rest days and self-care
- Make tasks achievable for someone with family responsibilities
- Provide concrete resources (websites, tools, platforms)
- Build momentum progressively

IMPORTANT: You must respond with ONLY valid JSON. Do not include any markdown formatting, explanations, or text outside the JSON."""


def extract_json_from_response(text: str) -> dict:
    """Extract JSON from text response."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from: {text[:200]}...")
        raise ValueError("Could not parse JSON from AI response")


def create_roadmap(profile: UserProfile) -> ComebackRoadmap:
    """
    Create a 30-day comeback roadmap for returning professionals.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        ComebackRoadmap with structured plan
    """
    client = get_ai_client()
    
    user_prompt = f"""Create a 30-day comeback roadmap for this professional:

NAME: {profile.name}
PREVIOUS ROLE: {profile.previous_role}
YEARS OF EXPERIENCE: {profile.years_experience}
CAREER BREAK: {profile.break_duration_months} months
TARGET ROLE: {profile.target_role}
SKILLS: {', '.join(profile.skills_known)}
INDUSTRY: {profile.industry or 'Not specified'}

Create a comprehensive 30-day plan in this exact JSON format:
{{
    "overview": "Motivational overview paragraph...",
    "weekly_focus": [
        {{
            "week": 1,
            "theme": "Week Theme",
            "objectives": ["Objective 1", "Objective 2", "Objective 3"]
        }}
    ],
    "daily_tasks": [
        {{
            "day": 1,
            "task": "Specific actionable task",
            "category": "Skills/Networking/Applications/Research/Self-Care",
            "estimated_hours": 1.5,
            "resources": ["resource1.com", "tool2.com"]
        }}
    ],
    "milestones": ["Milestone 1", "Milestone 2", ...]
}}

Respond with ONLY the JSON, no other text."""

    try:
        logger.info(f"Creating roadmap for user: {profile.name}")
        
        response = client.chat.completions.create(
            model=settings.sambanova_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            top_p=0.9
        )
        
        result_text = response.choices[0].message.content
        result = extract_json_from_response(result_text)
        
        # Construct WeeklyFocus objects
        weekly_focus = [
            WeeklyFocus(
                week=wf["week"],
                theme=wf["theme"],
                objectives=wf["objectives"]
            )
            for wf in result.get("weekly_focus", [])
        ]
        
        # Construct RoadmapTask objects
        daily_tasks = [
            RoadmapTask(
                day=dt["day"],
                task=dt["task"],
                category=dt["category"],
                estimated_hours=dt["estimated_hours"],
                resources=dt["resources"]
            )
            for dt in result.get("daily_tasks", [])
        ]
        
        return ComebackRoadmap(
            overview=result.get("overview", ""),
            weekly_focus=weekly_focus,
            daily_tasks=daily_tasks,
            milestones=result.get("milestones", [])
        )
        
    except Exception as e:
        logger.error(f"Error in roadmap creation: {str(e)}")
        raise Exception(f"Failed to create roadmap: {str(e)}")
