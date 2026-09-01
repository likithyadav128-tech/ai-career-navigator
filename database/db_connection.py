"""
Database Connection and Schema Migration Manager
Handles SQLite connection lifecycle and schema setup for multi-tenant isolation.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "users_db.sqlite")

def get_connection():
    """Returns a SQLite connection object with foreign keys enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_all_tables():
    """Creates all multi-tenant tables and applies incremental migrations."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        country TEXT DEFAULT 'United States',
        created_at TEXT NOT NULL
    );
    """)

    # Incremental column migration for country if table existed previously
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN country TEXT DEFAULT 'United States';")
    except Exception:
        pass

    # 2. User Profiles & Workspace Persistence
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        target_role TEXT NOT NULL,
        target_company TEXT NOT NULL,
        candidate_text TEXT NOT NULL,
        candidate_skills_json TEXT NOT NULL,
        github_user TEXT,
        readiness_score REAL DEFAULT 0.0,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 3. User Onboarding & Personalization Details
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_onboarding (
        user_id INTEGER PRIMARY KEY,
        country TEXT,
        education_level TEXT,
        degree_field TEXT,
        experience_level TEXT,
        interests_json TEXT,
        work_preference TEXT,
        target_locations TEXT,
        is_completed INTEGER DEFAULT 0,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 4. Roadmap Task Progress Tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_roadmap_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        phase_title TEXT NOT NULL,
        task_id TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0,
        completed_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(user_id, task_id)
    );
    """)

    # 5. Job Application Pipeline Tracker
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        company_name TEXT NOT NULL,
        role_title TEXT NOT NULL,
        location TEXT,
        salary_range TEXT,
        app_url TEXT,
        status TEXT NOT NULL DEFAULT 'Saved',
        notes TEXT,
        applied_date TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 6. Verified Skills & Quiz Results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_verified_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        verified_level TEXT NOT NULL,
        percentage REAL NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(user_id, skill_name)
    );
    """)

    # 7. Learning Hub Resource Bookmarks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resource_id TEXT NOT NULL,
        resource_title TEXT NOT NULL,
        resource_url TEXT,
        category TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(user_id, resource_id)
    );
    """)

    # 8. Public Career Portfolio
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_portfolios (
        user_id INTEGER PRIMARY KEY,
        headline TEXT,
        bio TEXT,
        github_url TEXT,
        linkedin_url TEXT,
        portfolio_url TEXT,
        is_public INTEGER DEFAULT 1,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 9. User Notifications & Achievements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        notif_type TEXT DEFAULT 'info',
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

# Initialize on import
init_all_tables()
