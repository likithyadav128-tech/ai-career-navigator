"""
Job Application Tracker Repository
Handles CRUD operations for the job search pipeline (Saved, Applied, Screening, Interview, Offer, Rejected).
"""
from datetime import datetime
from .db_connection import get_connection

def add_application(user_id: int, company_name: str, role_title: str,
                    location: str = "Remote", salary_range: str = "",
                    app_url: str = "", status: str = "Saved", notes: str = "") -> int:
    """Adds a new job application entry."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO user_applications (user_id, company_name, role_title, location, salary_range, app_url, status, notes, applied_date, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, company_name.strip(), role_title.strip(), location.strip(), salary_range.strip(), app_url.strip(), status, notes.strip(), now_str[:10], now_str))

    app_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return app_id

def update_application_status(app_id: int, user_id: int, new_status: str, notes: str = None) -> bool:
    """Updates the status and optional notes for a job application."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    if notes is not None:
        cursor.execute("""
        UPDATE user_applications SET status = ?, notes = ?, updated_at = ? WHERE id = ? AND user_id = ?
        """, (new_status, notes, now_str, app_id, user_id))
    else:
        cursor.execute("""
        UPDATE user_applications SET status = ?, updated_at = ? WHERE id = ? AND user_id = ?
        """, (new_status, now_str, app_id, user_id))

    conn.commit()
    conn.close()
    return True

def get_user_applications(user_id: int) -> list:
    """Fetches all applications for a user ordered by most recently updated."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, company_name, role_title, location, salary_range, app_url, status, notes, applied_date, updated_at
    FROM user_applications WHERE user_id = ? ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_application(app_id: int, user_id: int) -> bool:
    """Deletes a job application record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_applications WHERE id = ? AND user_id = ?", (app_id, user_id))
    conn.commit()
    conn.close()
    return True
