"""
Job Description Analyzer Module
Parses target job descriptions, extracts required technical & soft skills, and analyzes role expectations.
"""

import re
from modules.resume_analyzer import SKILL_TAXONOMY, extract_skills_from_text

def analyze_job_description(jd_text: str) -> dict:
    """
    Parses job description text and extracts:
    - Target Role Title (heuristic detection)
    - Technical Skills required
    - Soft Skills required
    - Experience level requirements
    """
    lines = [line.strip() for line in jd_text.split("\n") if line.strip()]
    
    # Try to detect Title
    role_title = "Target Role"
    for line in lines[:5]:
        if "role:" in line.lower() or "title:" in line.lower() or "position:" in line.lower():
            role_title = line.split(":", 1)[1].strip()
            break
        elif any(kw in line.lower() for kw in ["data scientist", "machine learning engineer", "data analyst", "software engineer", "ai engineer", "full stack"]):
            role_title = line
            break
            
    # Extract all matching skills from taxonomy
    all_extracted = extract_skills_from_text(jd_text)
    
    # Categorize into Technical vs Soft Skills
    soft_skills_list = ["Problem Solving", "Communication", "Business Communication", "Team Collaboration", "Agile", "Leadership", "Critical Thinking", "Data Storytelling"]
    
    tech_skills = [s for s in all_extracted if s not in soft_skills_list]
    soft_skills = [s for s in all_extracted if s in soft_skills_list]
    
    # Experience Level Heuristic
    lower_jd = jd_text.lower()
    if any(k in lower_jd for k in ["0-2 years", "entry level", "junior", "graduate", "fresher", "intern", "bachelor"]):
        exp_level = "Entry Level / Junior (0-2 years)"
    elif any(k in lower_jd for k in ["3-5 years", "mid-level", "mid level"]):
        exp_level = "Mid-Level (3-5 years)"
    elif any(k in lower_jd for k in ["5+ years", "senior", "lead", "principal"]):
        exp_level = "Senior / Lead (5+ years)"
    else:
        exp_level = "Entry to Mid-Level"

    return {
        "title": role_title,
        "all_required_skills": all_extracted,
        "tech_skills": tech_skills,
        "soft_skills": soft_skills,
        "exp_level": exp_level,
        "raw_text": jd_text
    }
