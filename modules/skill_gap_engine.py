"""
AI Skill Gap Analysis Engine
Compares candidate skills with target job requirements, categorizes into Strong, Moderate, Missing,
and calculates a weighted job readiness score.
"""

# Map of related/foundational skills for Moderate matching
SKILL_RELATIONSHIPS = {
    "PyTorch": ["TensorFlow", "Deep Learning", "Python", "Scikit-learn"],
    "TensorFlow": ["PyTorch", "Deep Learning", "Python", "Scikit-learn"],
    "Deep Learning": ["Machine Learning", "PyTorch", "TensorFlow", "Neural Networks"],
    "Machine Learning": ["Statistics", "Python", "Scikit-learn", "Pandas"],
    "FastAPI": ["Flask", "Django", "Python", "REST APIs"],
    "Flask": ["FastAPI", "Django", "Python", "REST APIs"],
    "PostgreSQL": ["SQL", "MySQL", "SQLite", "Database Management"],
    "MySQL": ["SQL", "PostgreSQL", "SQLite"],
    "Tableau": ["Power BI", "Plotly", "Matplotlib", "Seaborn"],
    "Power BI": ["Tableau", "Plotly", "Excel"],
    "PySpark": ["Pandas", "Python", "SQL", "Big Data"],
    "MLOps": ["Docker", "Git", "CI/CD", "Machine Learning"],
    "Docker": ["Kubernetes", "Linux", "DevOps"],
    "AWS": ["GCP", "Azure", "Cloud Computing"],
    "GCP": ["AWS", "Azure", "Cloud Computing"],
    "A/B Testing": ["Statistics", "Hypothesis Testing", "Data Analysis"],
    "Hypothesis Testing": ["Statistics", "Data Analysis"]
}

def analyze_skill_gaps(candidate_skills: list, required_skills: list) -> dict:
    """
    Compares candidate skills against target job required skills.
    
    Categorizes each required skill as:
    - STRONG (Exact match)
    - MODERATE (Candidate has a strongly related tool/foundation)
    - MISSING (Candidate does not have exact or related skill yet)
    
    Calculates weighted Job Readiness Score %.
    """
    cand_set = set(candidate_skills)
    cand_lower_map = {s.lower(): s for s in candidate_skills}
    
    strong_skills = []
    moderate_skills = []
    missing_skills = []
    
    for req in required_skills:
        req_lower = req.lower()
        
        # 1. Check Exact Match (Strong)
        if req_lower in cand_lower_map or req in cand_set:
            strong_skills.append({
                "skill": req,
                "status": "Strong",
                "reason": "Exact skill present on resume"
            })
            continue
            
        # 2. Check Related Skill Match (Moderate)
        related = SKILL_RELATIONSHIPS.get(req, [])
        matched_related = [r for r in related if r in cand_set or r.lower() in cand_lower_map]
        
        if matched_related:
            moderate_skills.append({
                "skill": req,
                "status": "Moderate",
                "reason": f"Foundational match via {', '.join(matched_related[:2])}"
            })
        else:
            missing_skills.append({
                "skill": req,
                "status": "Missing",
                "reason": "Skill missing from resume profile"
            })
            
    # Calculate Job Readiness Score
    total_req = len(required_skills)
    if total_req == 0:
        readiness_score = 100.0
    else:
        # Strong = 1.0 weight, Moderate = 0.5 weight, Missing = 0.0 weight
        weighted_matched = len(strong_skills) * 1.0 + len(moderate_skills) * 0.5
        readiness_score = round((weighted_matched / total_req) * 100, 1)

    # Extra candidate skills not explicitly listed in JD (Bonus Skills)
    req_lower_set = {r.lower() for r in required_skills}
    bonus_skills = [s for s in candidate_skills if s.lower() not in req_lower_set]

    return {
        "readiness_score": readiness_score,
        "strong_skills": strong_skills,
        "moderate_skills": moderate_skills,
        "missing_skills": missing_skills,
        "bonus_skills": bonus_skills,
        "total_required": total_req,
        "strong_count": len(strong_skills),
        "moderate_count": len(moderate_skills),
        "missing_count": len(missing_skills)
    }
