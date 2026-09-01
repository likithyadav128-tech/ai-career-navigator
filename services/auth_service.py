"""
Authentication Service
Orchestrates login, registration, password recovery, session guards, and demo access.
"""
from database.user_repo import register_user, authenticate_user, reset_user_password, get_user_by_id
from database.profile_repo import load_user_profile, load_onboarding_data

class AuthService:
    @staticmethod
    def sign_in(username: str, password: str) -> dict:
        """Authenticates user and returns profile state."""
        res = authenticate_user(username, password)
        if res["success"]:
            user_id = res["user_id"]
            prof = load_user_profile(user_id)
            onboarding = load_onboarding_data(user_id)
            res["profile"] = prof
            res["onboarding"] = onboarding
        return res

    @staticmethod
    def sign_up(username: str, password: str, full_name: str, country: str = "United States") -> dict:
        """Registers a new user."""
        return register_user(username, password, full_name, country)

    @staticmethod
    def reset_password(username: str, new_password: str) -> dict:
        """Resets user password."""
        return reset_user_password(username, new_password)

    @staticmethod
    def get_quick_demo_user(demo_type: str = "alex") -> dict:
        """Provides instant 1-click test credentials for evaluators."""
        if demo_type == "sam":
            return {
                "username": "sam_chen",
                "password": "demo123",
                "full_name": "Sam Chen",
                "target_role": "Software Engineer (Full-Stack)",
                "country": "Canada"
            }
        else:
            return {
                "username": "alex_rivera",
                "password": "demo123",
                "full_name": "Alex Rivera",
                "target_role": "Data Analyst",
                "country": "United States"
            }
