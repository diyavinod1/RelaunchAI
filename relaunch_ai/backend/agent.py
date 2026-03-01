"""
AI Agent Module for ReLaunchAI
Orchestrates the sequential reasoning pipeline for career reintegration assistance.
"""

import logging
from datetime import datetime
from typing import Dict, Any

from backend.models import UserProfile, AgentResponse
from backend.services import (
    analyze_skill_gaps,
    generate_resume_summary,
    generate_interview_answers,
    create_roadmap,
    find_returnship_programs,
)

logger = logging.getLogger(__name__)


class ReLaunchAgent:
    """
    AI Agent for career reintegration assistance.
    
    This agent orchestrates a sequential pipeline:
    1. Skill Gap Analysis
    2. Resume Summary Generation
    3. Interview Answer Generation
    4. 30-Day Roadmap Creation
    5. Returnship Program Suggestions
    """
    
    def __init__(self):
        self.pipeline_steps = [
            ("skill_gap_analysis", self._run_skill_gap_analysis),
            ("resume_summary", self._run_resume_summary),
            ("interview_prep", self._run_interview_prep),
            ("comeback_roadmap", self._run_roadmap),
            ("returnship_suggestions", self._run_returnship_finder),
        ]
    
    def _run_skill_gap_analysis(self, profile: UserProfile) -> Dict[str, Any]:
        """Execute skill gap analysis step."""
        logger.info("Step 1/5: Analyzing skill gaps...")
        return analyze_skill_gaps(profile)
    
    def _run_resume_summary(self, profile: UserProfile) -> Dict[str, Any]:
        """Execute resume summary generation step."""
        logger.info("Step 2/5: Generating resume summary...")
        return generate_resume_summary(profile)
    
    def _run_interview_prep(self, profile: UserProfile) -> Dict[str, Any]:
        """Execute interview preparation step."""
        logger.info("Step 3/5: Generating interview answers...")
        return generate_interview_answers(profile)
    
    def _run_roadmap(self, profile: UserProfile) -> Dict[str, Any]:
        """Execute roadmap creation step."""
        logger.info("Step 4/5: Creating 30-day roadmap...")
        return create_roadmap(profile)
    
    def _run_returnship_finder(self, profile: UserProfile) -> Dict[str, Any]:
        """Execute returnship program finder step."""
        logger.info("Step 5/5: Finding returnship programs...")
        return find_returnship_programs(profile)
    
    def process(self, profile: UserProfile) -> AgentResponse:
        """
        Process user profile through the complete AI pipeline.
        
        Args:
            profile: UserProfile with all career details
            
        Returns:
            AgentResponse containing all generated content
        """
        logger.info(f"Starting AI pipeline for user: {profile.name}")
        
        try:
            # Execute all pipeline steps
            skill_analysis = self._run_skill_gap_analysis(profile)
            resume = self._run_resume_summary(profile)
            interview = self._run_interview_prep(profile)
            roadmap = self._run_roadmap(profile)
            returnships = self._run_returnship_finder(profile)
            
            logger.info("AI pipeline completed successfully")
            
            return AgentResponse(
                user_name=profile.name,
                skill_gap_analysis=skill_analysis,
                resume_summary=resume,
                interview_prep=interview,
                comeback_roadmap=roadmap,
                returnship_suggestions=returnships,
                generated_at=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"AI pipeline failed: {str(e)}")
            raise


# Global agent instance
agent = ReLaunchAgent()


def run_agent_pipeline(profile: UserProfile) -> AgentResponse:
    """
    Convenience function to run the complete agent pipeline.
    
    Args:
        profile: UserProfile with career details
        
    Returns:
        AgentResponse with all generated content
    """
    return agent.process(profile)
