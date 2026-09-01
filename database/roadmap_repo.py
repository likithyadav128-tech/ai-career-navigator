"""
Roadmap Progress Repository
Persists completed tasks and milestone progress for dynamic career roadmaps.
"""
from datetime import datetime
from .db_connection import get_connection

def save_task_completion(user_id: int, phase_title: str, task_id: str, is_completed: bool) -> bool:
    """Saves or updates task completion state."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat() if is_completed else None

    cursor.execute("""
    INSERT INTO user_roadmap_tasks (user_id, phase_title, task_id, is_completed, completed_at)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(user_id, task_id) DO UPDATE SET
        is_completed = excluded.is_completed,
        completed_at = excluded.completed_at
    """, (user_id, phase_title, task_id, 1 if is_completed else 0, now_str))

    conn.commit()
    conn.close()
    return True

def load_user_roadmap_progress(user_id: int) -> dict:
    """Loads all completed tasks for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT task_id, is_completed FROM user_roadmap_tasks WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    progress = {}
    for r in rows:
        progress[r["task_id"]] = bool(r["is_completed"])
    return progress

def batch_init_roadmap(user_id: int, tasks_list: list) -> bool:
    """Initializes empty task states for a new roadmap."""
    conn = get_connection()
    cursor = conn.cursor()
    for phase_title, task_id in tasks_list:
        cursor.execute("""
        INSERT OR IGNORE INTO user_roadmap_tasks (user_id, phase_title, task_id, is_completed)
        VALUES (?, ?, ?, 0)
        """, (user_id, phase_title, task_id))
    conn.commit()
    conn.close()
    return True
