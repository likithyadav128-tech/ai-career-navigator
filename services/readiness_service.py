"""
Career Readiness Service
Orchestrates the transparent 7-Factor Career Twin readiness scoring engine.
Factors: Resume ATS (15%), Technical Skills (25%), Projects (15%), Coding/Assessments (15%), Interview (15%), Communication (10%), Evidence (5%).
"""
from modules.career_twin_engine import calculate_7_factor_readiness

class ReadinessService:
    @staticmethod
    def calculate_readiness(
        resume_score: float,
        skill_gap_result: dict,
        project_score: float,
        assessment_score: float,
        interview_score: float,
        communication_score: float,
        evidence_score: float,
        target_role: str,
        target_company: str
    ) -> dict:
        """Computes deterministic 7-factor readiness and actionable score booster recommendations."""
        return calculate_7_factor_readiness(
            resume_score=resume_score,
            skill_gap_result=skill_gap_result,
            project_score=project_score,
            assessment_score=assessment_score,
            interview_score=interview_score,
            communication_score=communication_score,
            evidence_score=evidence_score,
            target_role=target_role,
            company_name=target_company
        )
