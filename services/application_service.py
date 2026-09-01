"""
Job Application Service
Handles job tracker pipeline management across Kanban and List views.
"""
from database.tracker_repo import (
    add_application, update_application_status, get_user_applications, delete_application
)

class ApplicationService:
    STATUSES = ["Saved", "Applied", "Screening", "Interview", "Offer", "Rejected"]

    @staticmethod
    def get_pipeline(user_id: int) -> dict:
        """Fetches applications and groups them by status for Kanban boards."""
        apps = get_user_applications(user_id) if user_id else []
        kanban = {s: [] for s in ApplicationService.STATUSES}
        for a in apps:
            st = a.get("status", "Saved")
            if st in kanban:
                kanban[st].append(a)
            else:
                kanban["Saved"].append(a)

        return {
            "all_applications": apps,
            "kanban": kanban,
            "total_count": len(apps),
            "interviews_count": len(kanban["Interview"]) + len(kanban["Screening"]),
            "offers_count": len(kanban["Offer"])
        }

    @staticmethod
    def add_job(user_id: int, company: str, role: str, location: str, salary: str, url: str, status: str, notes: str) -> int:
        """Adds a job to tracker."""
        return add_application(user_id, company, role, location, salary, url, status, notes)

    @staticmethod
    def update_status(app_id: int, user_id: int, status: str, notes: str = None) -> bool:
        """Updates job status."""
        return update_application_status(app_id, user_id, status, notes)

    @staticmethod
    def remove_job(app_id: int, user_id: int) -> bool:
        """Removes a job from tracker."""
        return delete_application(app_id, user_id)
