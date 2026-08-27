"""
Personal Career Twin & Transparent 7-Factor Job Readiness Engine
Calculates deterministic readiness scores and actionable score improvement recommendations.
"""

from modules.company_role_profiles import ROLE_TAXONOMY, COMPANY_PROFILES

def calculate_7_factor_readiness(
    resume_score: float,
    skill_gap_result: dict,
    project_score: float,
    assessment_score: float,
    interview_score: float,
    communication_score: float,
    evidence_score: float,
    target_role: str = "Data Analyst",
    company_name: str = "Any Company (General Industry Standard)"
) -> dict:
    """
    Computes a transparent, deterministic 7-factor Job Readiness Score out of 100.
    
    Formula:
    Readiness = (Resume * 0.15) + (TechSkills * 0.25) + (Projects * 0.15) + 
                (Coding * 0.15) + (Interview * 0.15) + (Communication * 0.10) + (Evidence * 0.05)
    """
    role_info = ROLE_TAXONOMY.get(target_role, ROLE_TAXONOMY["Data Analyst"])
    company_info = COMPANY_PROFILES.get(company_name, COMPANY_PROFILES["Any Company (General Industry Standard)"])
    
    tech_skills_score = skill_gap_result.get("readiness_score", 50.0)
    
    # Apply company weighting multipliers
    mults = company_info["focus_multiplier"]
    
    f_resume = min(100.0, resume_score * mults.get("Resume", 1.0))
    f_tech = min(100.0, tech_skills_score * mults.get("Technical Skills", 1.0))
    f_proj = min(100.0, project_score * mults.get("Projects", 1.0))
    f_code = min(100.0, assessment_score * mults.get("Coding", mults.get("Assessments", 1.0)))
    f_interview = min(100.0, interview_score * mults.get("Interview", 1.0))
    f_comm = min(100.0, communication_score * mults.get("Communication", 1.0))
    f_evidence = min(100.0, evidence_score)

    weights = {
        "Resume": 0.15,
        "Technical Skills": 0.25,
        "Projects": 0.15,
        "Coding / Assessments": 0.15,
        "Interview": 0.15,
        "Communication": 0.10,
        "Certifications / Evidence": 0.05
    }

    weighted_score = (
        f_resume * weights["Resume"] +
        f_tech * weights["Technical Skills"] +
        f_proj * weights["Projects"] +
        f_code * weights["Coding / Assessments"] +
        f_interview * weights["Interview"] +
        f_comm * weights["Communication"] +
        f_evidence * weights["Certifications / Evidence"]
    )
    
    overall_readiness = round(min(100.0, max(0.0, weighted_score)), 1)
    
    # Generate "What will increase my score?" Action Plan
    missing_skills = [s["skill"] for s in skill_gap_result.get("missing_skills", [])]
    moderate_skills = [s["skill"] for s in skill_gap_result.get("moderate_skills", [])]
    
    score_boosters = []
    
    if missing_skills:
        top_missing = missing_skills[0]
        score_boosters.append({
            "action": f"Upgrade {top_missing} from Missing → Intermediate",
            "points": "+5.0 pts",
            "category": "Technical Skills",
            "task": f"Complete {top_missing} assessment and practice mini-projects."
        })
    if len(missing_skills) > 1:
        score_boosters.append({
            "action": f"Acquire foundational knowledge in {missing_skills[1]}",
            "points": "+4.0 pts",
            "category": "Technical Skills",
            "task": f"Watch tutorial and build basic scripts for {missing_skills[1]}."
        })
    if project_score < 80:
        score_boosters.append({
            "action": f"Deploy flagship portfolio project with documentation",
            "points": "+4.5 pts",
            "category": "Projects",
            "task": "Add live Streamlit/Render link and detailed README to GitHub repo."
        })
    if assessment_score < 75:
        score_boosters.append({
            "action": "Complete Verified Skill Assessment",
            "points": "+3.5 pts",
            "category": "Coding / Assessments",
            "task": "Take the 5-question adaptive assessment for core role skills."
        })
    if interview_score < 80:
        score_boosters.append({
            "action": "Practice 3 STAR-method technical interview questions",
            "points": "+3.0 pts",
            "category": "Interview",
            "task": "Complete a session on AI Mock Interview Simulator."
        })
    if resume_score < 85:
        score_boosters.append({
            "action": "Optimize resume project descriptions with impact metrics",
            "points": "+2.0 pts",
            "category": "Resume",
            "task": "Use AI Resume Bullet Optimizer to add quantitative results (% accuracy, savings)."
        })

    return {
        "overall_readiness": overall_readiness,
        "target_role": target_role,
        "company_name": company_name,
        "factors": {
            "Resume": round(f_resume, 1),
            "Technical Skills": round(f_tech, 1),
            "Projects": round(f_proj, 1),
            "Coding / Assessments": round(f_code, 1),
            "Interview": round(f_interview, 1),
            "Communication": round(f_comm, 1),
            "Certifications / Evidence": round(f_evidence, 1)
        },
        "weights": weights,
        "score_boosters": score_boosters[:4]
    }
