"""
Database Package for AI Career Navigator
Multi-tenant SQLite persistence layer with clean repository abstractions.
"""
from .db_connection import init_all_tables, get_connection, DB_PATH
from .user_repo import (
    register_user, authenticate_user, reset_user_password, get_user_by_id, get_user_by_username
)
from .profile_repo import (
    save_user_profile, load_user_profile, save_onboarding_data, load_onboarding_data
)
from .roadmap_repo import (
    save_task_completion, load_user_roadmap_progress, batch_init_roadmap
)
from .tracker_repo import (
    add_application, update_application_status, get_user_applications, delete_application
)
from .portfolio_repo import (
    save_user_portfolio, get_user_portfolio, get_public_portfolio_by_username
)
from .notification_repo import (
    add_notification, get_user_notifications, mark_notification_read
)
