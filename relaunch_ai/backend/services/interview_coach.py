"""
Interview Coach Service
Generates confident answers for explaining career breaks and other common questions.
"""

import json
import logging
import re
from backend.config import get_ai_client, settings
from backend.models import InterviewPrep, InterviewAnswer, UserProfile

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert interview coach specializing in helping professionals confidently discuss career breaks.

Your task is to create:
1. Confident, concise answers about the career break
2. Responses that reframe the break as valuable experience
3. Strategies for handling potential objections
4. Tips for projecting confidence and readiness

Guidelines:
- Answers should be 60-90 seconds when spoken
- Use positive, forward-looking language
- Avoid over-explaining or apologizing
- Emphasize skills gained during the break
- Show enthusiasm and readiness to contribute
- Address concerns without being defensive

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


def generate_interview_answers(profile: UserProfile) -> InterviewPrep:
    """
    Generate interview answers and coaching for returning professionals.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        InterviewPrep with Q&A and tips
    """
    client = get_ai_client()
    
    break_context = {
        "maternity": "maternity leave and early childcare responsibilities",
        "childcare": "dedicated time raising and caring for children",
        "eldercare": "caring for elderly family members",
        "health": "personal health and wellness period",
        "relocation": "family relocation and settling period",
        "education": "pursuing further education and certifications",
        "personal": "personal growth and reflection period",
        "other": "personal circumstances"
    }
    
    break_description = break_context.get(profile.break_reason.value, "personal circumstances")
    
    user_prompt = f"""Create interview coaching content for this professional:

NAME: {profile.name}
PREVIOUS ROLE: {profile.previous_role}
YEARS OF EXPERIENCE: {profile.years_experience}
CAREER BREAK: {profile.break_duration_months} months for {break_description}
SKILLS: {', '.join(profile.skills_known)}
TARGET ROLE: {profile.target_role}

Generate confident answers in this exact JSON format:
{{
    "break_explanation": {{
        "question": "Can you tell us about the gap in your resume?",
        "answer": "Confident 60-90 second response...",
        "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    "skill_refresh": {{
        "question": "How have you kept your skills current?",
        "answer": "Response about staying updated...",
        "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    "motivation_return": {{
        "question": "Why do you want to return to work now?",
        "answer": "Response about motivation...",
        "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    "handling_objections": {{
        "question": "How do we know you're ready for this commitment?",
        "answer": "Response addressing concerns...",
        "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    "general_tips": ["Tip 1", "Tip 2", "Tip 3", "Tip 4", "Tip 5"]
}}

Respond with ONLY the JSON, no other text."""

    try:
        logger.info(f"Generating interview answers for user: {profile.name}")
        
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
        
        return InterviewPrep(
            break_explanation=InterviewAnswer(**result["break_explanation"]),
            skill_refresh=InterviewAnswer(**result["skill_refresh"]),
            motivation_return=InterviewAnswer(**result["motivation_return"]),
            handling_objections=InterviewAnswer(**result["handling_objections"]),
            general_tips=result.get("general_tips", [])
        )
        
    except Exception as e:
        logger.error(f"Error in interview coaching: {str(e)}")
        raise Exception(f"Failed to generate interview coaching: {str(e)}")
