"""
Resume Summary Generator Service
Creates professional resume summaries that position career breaks positively.
"""

import json
import logging
import re
from backend.config import get_ai_client, settings
from backend.models import ResumeSummary, UserProfile

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert resume writer and career strategist specializing in helping professionals return to work after career breaks.

Your task is to create compelling resume content that:
1. Highlights strengths and transferable skills
2. Positions the career break as a period of growth
3. Creates a powerful professional narrative
4. Addresses potential employer concerns proactively

Guidelines:
- Use confident, professional language
- Frame the career break positively without over-explaining
- Focus on achievements and capabilities
- Create a narrative of continuous growth
- Avoid apologetic tone about the break
- Emphasize readiness and enthusiasm to return
- Keep content concise and impactful

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


def generate_resume_summary(profile: UserProfile) -> ResumeSummary:
    """
    Generate a professional resume summary for returning professionals.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        ResumeSummary with generated content
    """
    client = get_ai_client()
    
    break_context = {
        "maternity": "maternity leave and early childcare",
        "childcare": "dedicated time for family and childcare",
        "eldercare": "caring for elderly family members",
        "health": "personal health and wellness recovery",
        "relocation": "relocation and family transition",
        "education": "further education and skill development",
        "personal": "personal growth and reflection",
        "other": "personal circumstances"
    }
    
    break_description = break_context.get(profile.break_reason.value, "personal circumstances")
    
    user_prompt = f"""Create a compelling resume summary for this professional:

NAME: {profile.name}
PREVIOUS ROLE: {profile.previous_role}
YEARS OF EXPERIENCE: {profile.years_experience}
EDUCATION: {profile.education}
CAREER BREAK: {profile.break_duration_months} months for {break_description}
SKILLS: {', '.join(profile.skills_known)}
TARGET ROLE: {profile.target_role}
INDUSTRY: {profile.industry or 'Not specified'}

Generate content in this exact JSON format:
{{
    "professional_summary": "Compelling 3-4 sentence summary...",
    "key_strengths": ["Strength 1", "Strength 2", ...],
    "career_break_positioning": "How to frame the break...",
    "suggested_headline": "Target Role | Key Expertise | Value Proposition"
}}

Respond with ONLY the JSON, no other text."""

    try:
        logger.info(f"Generating resume summary for user: {profile.name}")
        
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
        
        return ResumeSummary(
            professional_summary=result.get("professional_summary", ""),
            key_strengths=result.get("key_strengths", []),
            career_break_positioning=result.get("career_break_positioning", ""),
            suggested_headline=result.get("suggested_headline", "")
        )
        
    except Exception as e:
        logger.error(f"Error in resume summary generation: {str(e)}")
        raise Exception(f"Failed to generate resume summary: {str(e)}")
