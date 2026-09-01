"""
Project Service
Generates targeted flagship portfolio blueprints and audits existing student projects across 7 engineering dimensions.
"""
from modules.project_strength_analyzer import audit_project_strength, generate_flagship_project_blueprint

class ProjectService:
    @staticmethod
    def audit_project(name: str, tech_stack: str, description: str, has_deployment: bool, has_documentation: bool) -> dict:
        """Audits project strength across 7 dimensions (0-100 score)."""
        return audit_project_strength(name, tech_stack, description, has_deployment, has_documentation)

    @staticmethod
    def generate_blueprint(candidate_skills: list, target_role: str) -> dict:
        """Generates industry-grade flagship project blueprint with architecture and README specs."""
        return generate_flagship_project_blueprint(candidate_skills, target_role)
