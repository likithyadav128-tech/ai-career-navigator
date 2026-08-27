"""
Career Route Simulator Module
Compares candidate readiness across 10 major technical career tracks simultaneously.
"""

from modules.company_role_profiles import ROLE_TAXONOMY
from modules.skill_gap_engine import analyze_skill_gaps

def simulate_multi_role_readiness(candidate_skills: list) -> list:
    """
    Simulates candidate job readiness % across all 10 major technical roles.
    Returns a sorted list of roles by readiness score descending with delta requirements.
    """
    simulations = []
    
    for r_key, r_info in ROLE_TAXONOMY.items():
        gap_res = analyze_skill_gaps(candidate_skills, r_info["core_skills"])
        readiness = gap_res["readiness_score"]
        
        missing_skills = [item["skill"] for item in gap_res["missing_skills"]]
        strong_skills = [item["skill"] for item in gap_res["strong_skills"]]
        
        simulations.append({
            "role": r_info["title"],
            "description": r_info["description"],
            "readiness_score": readiness,
            "strong_count": len(strong_skills),
            "missing_count": len(missing_skills),
            "missing_skills": missing_skills,
            "strong_skills": strong_skills
        })
        
    simulations.sort(key=lambda x: x["readiness_score"], reverse=True)
    return simulations

def calculate_role_transition_delta(candidate_skills: list, current_role: str, target_role: str) -> dict:
    """
    Calculates exact delta skills required to transition from Current Role to Target Role.
    """
    curr_info = ROLE_TAXONOMY.get(current_role, ROLE_TAXONOMY["Data Analyst"])
    targ_info = ROLE_TAXONOMY.get(target_role, ROLE_TAXONOMY["Data Scientist"])
    
    curr_gap = analyze_skill_gaps(candidate_skills, curr_info["core_skills"])
    targ_gap = analyze_skill_gaps(candidate_skills, targ_info["core_skills"])
    
    delta_skills = [s for s in targ_info["core_skills"] if s not in curr_info["core_skills"]]
    missing_delta = [s for s in delta_skills if s not in candidate_skills]
    
    return {
        "current_role": current_role,
        "current_readiness": curr_gap["readiness_score"],
        "target_role": target_role,
        "target_readiness": targ_gap["readiness_score"],
        "delta_skills_total": delta_skills,
        "missing_delta_skills": missing_delta,
        "estimated_transition_time": f"{len(missing_delta) * 2} Weeks"
    }
