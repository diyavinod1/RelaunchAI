"""
Skill Gap Analysis Service
Analyzes user's current skills against target role requirements.
"""

import json
import logging
import re
from typing import List
from backend.config import get_ai_client, settings
from backend.models import SkillGapAnalysis, SkillGap, UserProfile

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert career counselor and skills analyst specializing in helping professionals return to the workforce after career breaks.

Your task is to analyze a user's current skills against their target role and identify:
1. Transferable skills they already possess
2. Skill gaps they need to address
3. Priority order for upskilling
4. Learning resources and time estimates

Guidelines:
- Be encouraging and supportive in tone
- Focus on realistic, achievable skill development
- Consider industry trends and market demands
- Account for skills that may need refreshing after a career break
- Provide specific, actionable recommendations
- Avoid gender bias or assumptions about capabilities

IMPORTANT: You must respond with ONLY valid JSON. Do not include any markdown formatting, explanations, or text outside the JSON."""


def extract_json_from_response(text: str) -> dict:
    """Extract JSON from text response."""
    # Try to find JSON between curly braces
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    # Try parsing the whole text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from: {text[:200]}...")
        raise ValueError("Could not parse JSON from AI response")


def analyze_skill_gaps(profile: UserProfile) -> SkillGapAnalysis:
    """
    Analyze skill gaps between user's profile and target role.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        SkillGapAnalysis with detailed recommendations
    """
    client = get_ai_client()
    
    user_prompt = f"""Analyze the skill gaps for this professional returning to work:

NAME: {profile.name}
PREVIOUS ROLE: {profile.previous_role}
YEARS OF EXPERIENCE: {profile.years_experience}
CAREER BREAK: {profile.break_duration_months} months
BREAK REASON: {profile.break_reason.value}
EDUCATION: {profile.education}
CURRENT SKILLS: {', '.join(profile.skills_known)}
TARGET ROLE: {profile.target_role}
INDUSTRY: {profile.industry or 'Not specified'}

Provide a comprehensive skill gap analysis in this exact JSON format:
{{
    "transferable_skills": ["skill1", "skill2", ...],
    "skill_gaps": [
        {{
            "skill_name": "Skill Name",
            "importance": "High/Medium/Low",
            "gap_level": "Critical/Moderate/Minor",
            "learning_resources": ["resource1", "resource2"],
            "estimated_time_weeks": 4
        }}
    ],
    "upskilling_priority": ["skill1", "skill2", ...],
    "market_trends_note": "Brief note on industry trends"
}}

Respond with ONLY the JSON, no other text."""

    try:
        logger.info(f"Analyzing skill gaps for user: {profile.name}")
        
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
        
        # Validate and construct SkillGap objects
        skill_gaps = [
            SkillGap(
                skill_name=sg["skill_name"],
                importance=sg["importance"],
                gap_level=sg["gap_level"],
                learning_resources=sg["learning_resources"],
                estimated_time_weeks=sg["estimated_time_weeks"]
            )
            for sg in result.get("skill_gaps", [])
        ]
        
        return SkillGapAnalysis(
            transferable_skills=result.get("transferable_skills", []),
            skill_gaps=skill_gaps,
            upskilling_priority=result.get("upskilling_priority", []),
            market_trends_note=result.get("market_trends_note", "")
        )
        
    except Exception as e:
        logger.error(f"Error in skill gap analysis: {str(e)}")
        raise Exception(f"Failed to analyze skill gaps: {str(e)}")
