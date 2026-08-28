"""
User Authentication & Multi-Tenant Persistence Database Engine
Provides SQLite database storage for multi-user registration, password hashing, and isolated user workspace persistence.
"""

import sqlite3
import hashlib
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "users_db.sqlite")

def init_db():
    """Initializes SQLite tables for multi-tenant user authentication and workspace persistence."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # User Workspace Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        target_role TEXT NOT NULL,
        target_company TEXT NOT NULL,
        candidate_text TEXT NOT NULL,
        candidate_skills_json TEXT NOT NULL,
        github_user TEXT,
        readiness_score REAL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # User Verified Skills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_verified_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        verified_level TEXT NOT NULL,
        percentage REAL NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # User Daily Mission Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_daily_missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        completed INTEGER NOT NULL,
        mission_date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

def _hash_password(password: str) -> str:
    """Hashes password securely using SHA-256 with salt."""
    return hashlib.sha256(("salt_career_os_" + password).encode("utf-8")).hexdigest()

def register_user(username: str, password: str, full_name: str) -> dict:
    """Registers a new student account."""
    clean_user = username.strip().lower()
    if not clean_user or not password:
        return {"success": False, "message": "Username and password cannot be empty."}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        pass_hash = _hash_password(password)
        now_str = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (username, password_hash, full_name, created_at) VALUES (?, ?, ?, ?)",
            (clean_user, pass_hash, full_name, now_str)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"success": True, "user_id": user_id, "username": clean_user, "full_name": full_name}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "message": f"Username '{clean_user}' is already registered."}

def authenticate_user(username: str, password: str) -> dict:
    """Authenticates a user against hashed credentials."""
    clean_user = username.strip().lower()
    pass_hash = _hash_password(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name FROM users WHERE username = ? AND password_hash = ?", (clean_user, pass_hash))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"success": True, "user_id": row[0], "username": row[1], "full_name": row[2]}
    else:
        return {"success": False, "message": "Invalid username or password."}

def save_user_profile(user_id: int, target_role: str, target_company: str, candidate_text: str, candidate_skills: list, github_user: str, readiness_score: float):
    """Saves or updates user's isolated workspace profile."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    skills_json = json.dumps(candidate_skills)
    now_str = datetime.now().isoformat()

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

def load_user_profile(user_id: int) -> dict:
    """Loads user's saved workspace profile."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT target_role, target_company, candidate_text, candidate_skills_json, github_user, readiness_score FROM user_profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        try:
            skills = json.loads(row[3])
        except Exception:
            skills = []
        return {
            "has_profile": True,
            "target_role": row[0],
            "target_company": row[1],
            "candidate_text": row[2],
            "candidate_skills": skills,
            "github_user": row[4],
            "readiness_score": row[5]
        }
    return {"has_profile": False}

def create_demo_accounts():
    """Creates default demo student accounts for instant testing."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        register_user("alex_rivera", "demo123", "Alex Rivera")
        register_user("sam_chen", "demo123", "Sam Chen")
