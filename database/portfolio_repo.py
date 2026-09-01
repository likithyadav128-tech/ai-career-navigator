"""
Public Portfolio Repository
Persists shareable career portfolio profiles and visibility settings.
"""
from datetime import datetime
from .db_connection import get_connection

def save_user_portfolio(user_id: int, headline: str, bio: str,
                        github_url: str = "", linkedin_url: str = "",
                        portfolio_url: str = "", is_public: bool = True) -> bool:
    """Saves or updates the user's public/private career portfolio."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO user_portfolios (user_id, headline, bio, github_url, linkedin_url, portfolio_url, is_public, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        headline = excluded.headline,
        bio = excluded.bio,
        github_url = excluded.github_url,
        linkedin_url = excluded.linkedin_url,
        portfolio_url = excluded.portfolio_url,
        is_public = excluded.is_public,
        updated_at = excluded.updated_at
    """, (user_id, headline.strip(), bio.strip(), github_url.strip(), linkedin_url.strip(), portfolio_url.strip(), 1 if is_public else 0, now_str))

    conn.commit()
    conn.close()
    return True

def get_user_portfolio(user_id: int) -> dict:
    """Gets portfolio settings for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT headline, bio, github_url, linkedin_url, portfolio_url, is_public, updated_at
    FROM user_portfolios WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "has_portfolio": False,
            "headline": "Aspiring Tech Professional",
            "bio": "Building industry-grade projects and mastering in-demand skills.",
            "github_url": "",
            "linkedin_url": "",
            "portfolio_url": "",
            "is_public": True
        }

    return {
        "has_portfolio": True,
        "headline": row["headline"] or "Aspiring Tech Professional",
        "bio": row["bio"] or "Building industry-grade projects and mastering in-demand skills.",
        "github_url": row["github_url"] or "",
        "linkedin_url": row["linkedin_url"] or "",
        "portfolio_url": row["portfolio_url"] or "",
        "is_public": bool(row["is_public"]),
        "updated_at": row["updated_at"]
    }

def get_public_portfolio_by_username(username: str) -> dict:
    """Fetches a public profile for external viewing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.username, u.full_name, u.country, p.target_role, p.target_company, p.candidate_skills_json, p.readiness_score,
           pf.headline, pf.bio, pf.github_url, pf.linkedin_url, pf.portfolio_url, pf.is_public
    FROM users u
    LEFT JOIN user_profiles p ON u.id = p.user_id
    LEFT JOIN user_portfolios pf ON u.id = pf.user_id
    WHERE u.username = ?
    """, (username.strip().lower(),))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # Check privacy
    if row["is_public"] is not None and row["is_public"] == 0:
        return {"is_private": True, "full_name": row["full_name"]}

    import json
    try:
        skills = json.loads(row["candidate_skills_json"]) if row["candidate_skills_json"] else []
    except Exception:
        skills = []

    return {
        "is_private": False,
        "username": row["username"],
        "full_name": row["full_name"],
        "country": row["country"] or "Global",
        "target_role": row["target_role"] or "Tech Professional",
        "headline": row["headline"] or f"Aspiring {row['target_role'] or 'Developer'}",
        "bio": row["bio"] or "Driven learner building portfolio projects and career readiness.",
        "skills": skills,
        "readiness_score": row["readiness_score"] or 0.0,
        "github_url": row["github_url"] or "",
        "linkedin_url": row["linkedin_url"] or "",
        "portfolio_url": row["portfolio_url"] or ""
    }
