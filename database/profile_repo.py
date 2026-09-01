"""
Profile & Onboarding Repository
Handles persistent user career profiles, onboarding answers, and workspace settings.
"""
import json
from datetime import datetime
from .db_connection import get_connection

def save_user_profile(user_id: int, target_role: str, target_company: str,
                      candidate_text: str, candidate_skills: list, github_user: str = "",
                      readiness_score: float = 0.0) -> bool:
    """Saves or updates the user's workspace profile."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    skills_json = json.dumps(candidate_skills)

    cursor.execute("""
    INSERT INTO user_profiles (user_id, target_role, target_company, candidate_text, candidate_skills_json, github_user, readiness_score, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        target_role = excluded.target_role,
        target_company = excluded.target_company,
        candidate_text = excluded.candidate_text,
        candidate_skills_json = excluded.candidate_skills_json,
        github_user = excluded.github_user,
        readiness_score = excluded.readiness_score,
        updated_at = excluded.updated_at
    """, (user_id, target_role, target_company, candidate_text, skills_json, github_user, readiness_score, now_str))

    conn.commit()
    conn.close()
    return True

def load_user_profile(user_id: int) -> dict:
    """Loads a user's saved workspace profile."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT target_role, target_company, candidate_text, candidate_skills_json, github_user, readiness_score, updated_at
    FROM user_profiles WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"has_profile": False}

    try:
        skills = json.loads(row["candidate_skills_json"])
    except Exception:
        skills = []

    return {
        "has_profile": True,
        "target_role": row["target_role"],
        "target_company": row["target_company"],
        "candidate_text": row["candidate_text"],
        "candidate_skills": skills,
        "github_user": row["github_user"] or "",
        "readiness_score": row["readiness_score"] or 0.0,
        "updated_at": row["updated_at"]
    }

def save_onboarding_data(user_id: int, country: str, education_level: str,
                         degree_field: str, experience_level: str,
                         interests: list, work_preference: str,
                         target_locations: str = "Remote") -> bool:
    """Saves 5-step onboarding wizard responses."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    interests_json = json.dumps(interests if isinstance(interests, list) else [])

    cursor.execute("""
    INSERT INTO user_onboarding (user_id, country, education_level, degree_field, experience_level, interests_json, work_preference, target_locations, is_completed, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        country = excluded.country,
        education_level = excluded.education_level,
        degree_field = excluded.degree_field,
        experience_level = excluded.experience_level,
        interests_json = excluded.interests_json,
        work_preference = excluded.work_preference,
        target_locations = excluded.target_locations,
        is_completed = 1,
        updated_at = excluded.updated_at
    """, (user_id, country, education_level, degree_field, experience_level, interests_json, work_preference, target_locations, now_str))

    conn.commit()
    conn.close()
    return True

def load_onboarding_data(user_id: int) -> dict:
    """Loads onboarding preferences."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT country, education_level, degree_field, experience_level, interests_json, work_preference, target_locations, is_completed
    FROM user_onboarding WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"is_completed": False}

    try:
        interests = json.loads(row["interests_json"])
    except Exception:
        interests = []

    return {
        "is_completed": bool(row["is_completed"]),
        "country": row["country"],
        "education_level": row["education_level"],
        "degree_field": row["degree_field"],
        "experience_level": row["experience_level"],
        "interests": interests,
        "work_preference": row["work_preference"],
        "target_locations": row["target_locations"]
    }
