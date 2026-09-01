"""
Career Comparison Service
Enables side-by-side comparison between Career A and Career B.
Analyzes skill overlap, transition delta, salary differentials, learning curves, and interview focus.
"""
from config import CAREER_TRACKS
from modules.skill_gap_engine import analyze_skill_gaps

class CareerComparisonService:
    @staticmethod
    def compare_careers(role_a: str, role_b: str, candidate_skills: list) -> dict:
        """Compares two career tracks side-by-side."""
        track_a = CAREER_TRACKS.get(role_a, CAREER_TRACKS["Data Analyst"])
        track_b = CAREER_TRACKS.get(role_b, CAREER_TRACKS["Data Scientist"])

        gap_a = analyze_skill_gaps(candidate_skills, track_a["core_skills"])
        gap_b = analyze_skill_gaps(candidate_skills, track_b["core_skills"])

        skills_a_set = set(track_a["core_skills"])
        skills_b_set = set(track_b["core_skills"])

        shared_skills = sorted(list(skills_a_set.intersection(skills_b_set)))
        unique_to_a = sorted(list(skills_a_set - skills_b_set))
        unique_to_b = sorted(list(skills_b_set - skills_a_set))

        # Transition Delta
        missing_for_b_from_a = [s for s in track_b["core_skills"] if s not in skills_a_set]
        
        transition_months = len(missing_for_b_from_a) * 1.5
        if transition_months == 0:
            time_estimate = "Immediate / Ready"
        elif transition_months <= 3:
            time_estimate = f"~{int(transition_months)} - 3 Months"
        else:
            time_estimate = f"~{int(transition_months)} - {int(transition_months + 2)} Months"

        return {
            "track_a": {
                "role": role_a,
                "icon": track_a["icon"],
                "category": track_a["category"],
                "difficulty": track_a["difficulty"],
                "avg_salary": track_a["avg_salary"],
                "demand": track_a["demand_growth"],
                "match_score": gap_a["readiness_score"],
                "description": track_a["description"],
                "core_skills": track_a["core_skills"],
                "unique_skills": unique_to_a,
                "interview_focus": track_a["interview_focus"]
            },
            "track_b": {
                "role": role_b,
                "icon": track_b["icon"],
                "category": track_b["category"],
                "difficulty": track_b["difficulty"],
                "avg_salary": track_b["avg_salary"],
                "demand": track_b["demand_growth"],
                "match_score": gap_b["readiness_score"],
                "description": track_b["description"],
                "core_skills": track_b["core_skills"],
                "unique_skills": unique_to_b,
                "interview_focus": track_b["interview_focus"]
            },
            "shared_skills": shared_skills,
            "transition_delta": {
                "skills_needed": missing_for_b_from_a,
                "estimated_time": time_estimate,
                "difficulty_shift": f"{track_a['difficulty']} → {track_b['difficulty']}"
            }
        }
