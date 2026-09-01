"""
User Repository
Handles user registration, authentication, password verification, and password reset.
"""
import hashlib
from datetime import datetime
from .db_connection import get_connection

def _hash_password(password: str) -> str:
    """Hashes password with SHA-256 and a dedicated salt."""
    salt = "salt_ai_career_navigator_v2_"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def register_user(username: str, password: str, full_name: str, country: str = "United States") -> dict:
    """Registers a new user account with hashed password and country metadata."""
    clean_user = username.strip().lower()
    clean_name = full_name.strip()
    
    if not clean_user or not password:
        return {"success": False, "message": "Username and password are required."}
    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    conn = get_connection()
    cursor = conn.cursor()

    try:
        pass_hash = _hash_password(password)
        now_str = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (username, password_hash, full_name, country, created_at) VALUES (?, ?, ?, ?, ?)",
            (clean_user, pass_hash, clean_name if clean_name else clean_user, country, now_str)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {
            "success": True,
            "user_id": user_id,
            "username": clean_user,
            "full_name": clean_name if clean_name else clean_user,
            "country": country
        }
    except Exception as e:
        conn.close()
        if "UNIQUE" in str(e).upper() or "IntegrityError" in type(e).__name__:
            return {"success": False, "message": f"Username '{clean_user}' is already registered."}
        return {"success": False, "message": f"Registration failed: {str(e)}"}

def authenticate_user(username: str, password: str) -> dict:
    """Authenticates credentials against the users table."""
    clean_user = username.strip().lower()
    if not clean_user or not password:
        return {"success": False, "message": "Please enter username and password."}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash, full_name, country, created_at FROM users WHERE username = ?", (clean_user,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"success": False, "message": "User not found. Please check username or register."}

    expected_hash = _hash_password(password)
    # Also support legacy salt for existing seed users
    legacy_hash = hashlib.sha256(("salt_career_os_" + password).encode("utf-8")).hexdigest()

    if row["password_hash"] == expected_hash or row["password_hash"] == legacy_hash:
        return {
            "success": True,
            "user_id": row["id"],
            "username": row["username"],
            "full_name": row["full_name"],
            "country": row["country"] or "United States"
        }
    else:
        return {"success": False, "message": "Incorrect password. Please try again."}

def reset_user_password(username: str, new_password: str) -> dict:
    """Resets password for an existing user account."""
    clean_user = username.strip().lower()
    if not clean_user or not new_password:
        return {"success": False, "message": "Username and new password are required."}
    if len(new_password) < 6:
        return {"success": False, "message": "New password must be at least 6 characters."}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (clean_user,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"success": False, "message": f"Username '{clean_user}' does not exist."}

    new_hash = _hash_password(new_password)
    cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash, clean_user))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Password updated successfully. You can now log in."}

def get_user_by_id(user_id: int) -> dict:
    """Fetches user metadata by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, country, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_user_by_username(username: str) -> dict:
    """Fetches user metadata by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, country, created_at FROM users WHERE username = ?", (username.strip().lower(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
