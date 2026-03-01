"""
Returnship Program Finder Service
Suggests relevant returnship programs and provides guidance.
"""

import json
import logging
import re
from backend.config import get_ai_client, settings
from backend.models import ReturnshipSuggestions, ReturnshipProgram, UserProfile

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert in returnship programs and career reintegration initiatives.

Your task is to recommend relevant returnship programs and provide guidance on:
1. Specific returnship programs by major companies
2. Eligibility requirements and application tips
3. Alternative pathways for career reentry
4. Networking strategies for returnship opportunities

Guidelines:
- Focus on legitimate, well-established programs
- Include programs from diverse industries
- Provide realistic eligibility criteria
- Include both formal returnships and alternative pathways
- Consider geographic relevance
- Offer networking and application advice

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


def find_returnship_programs(profile: UserProfile) -> ReturnshipSuggestions:
    """
    Find relevant returnship programs for returning professionals.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        ReturnshipSuggestions with program recommendations
    """
    client = get_ai_client()
    
    user_prompt = f"""Recommend returnship programs for this professional:

NAME: {profile.name}
PREVIOUS ROLE: {profile.previous_role}
YEARS OF EXPERIENCE: {profile.years_experience}
TARGET ROLE: {profile.target_role}
INDUSTRY: {profile.industry or 'Not specified'}
LOCATION: {profile.location or 'Any location'}
SKILLS: {', '.join(profile.skills_known)}

Provide recommendations in this exact JSON format:
{{
    "recommended_programs": [
        {{
            "program_name": "Program Name",
            "company": "Company Name",
            "location": "Location(s)",
            "duration": "e.g., 16 weeks",
            "description": "Brief description",
            "eligibility": "Who can apply",
            "application_link": "URL or 'Search: program name'",
            "deadline": "Application deadline info or 'Rolling'"
        }}
    ],
    "general_advice": "Paragraph of advice...",
    "networking_tips": ["Tip 1", "Tip 2", "Tip 3", "Tip 4", "Tip 5"]
}}

Respond with ONLY the JSON, no other text."""

    try:
        logger.info(f"Finding returnship programs for user: {profile.name}")
        
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
        
        # Construct ReturnshipProgram objects
        programs = [
            ReturnshipProgram(
                program_name=rp["program_name"],
                company=rp["company"],
                location=rp["location"],
                duration=rp["duration"],
                description=rp["description"],
                eligibility=rp["eligibility"],
                application_link=rp.get("application_link"),
                deadline=rp.get("deadline")
            )
            for rp in result.get("recommended_programs", [])
        ]
        
        return ReturnshipSuggestions(
            recommended_programs=programs,
            general_advice=result.get("general_advice", ""),
            networking_tips=result.get("networking_tips", [])
        )
        
    except Exception as e:
        logger.error(f"Error in returnship finder: {str(e)}")
        raise Exception(f"Failed to find returnship programs: {str(e)}")
