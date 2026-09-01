"""
Notification & Milestone Achievement Repository
Handles user notifications, career milestone alerts, and progress achievements.
"""
from datetime import datetime
from .db_connection import get_connection

def add_notification(user_id: int, title: str, message: str, notif_type: str = "info") -> int:
    """Creates a new user alert or achievement notification."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO user_notifications (user_id, title, message, notif_type, is_read, created_at)
    VALUES (?, ?, ?, ?, 0, ?)
    """, (user_id, title, message, notif_type, now_str))

    notif_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return notif_id

def get_user_notifications(user_id: int, unread_only: bool = False) -> list:
    """Fetches notifications for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    if unread_only:
        cursor.execute("""
        SELECT id, title, message, notif_type, is_read, created_at
        FROM user_notifications WHERE user_id = ? AND is_read = 0 ORDER BY id DESC
        """, (user_id,))
    else:
        cursor.execute("""
        SELECT id, title, message, notif_type, is_read, created_at
        FROM user_notifications WHERE user_id = ? ORDER BY id DESC LIMIT 20
        """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_notification_read(notif_id: int, user_id: int) -> bool:
    """Marks a notification as read."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notif_id, user_id))
    conn.commit()
    conn.close()
    return True
