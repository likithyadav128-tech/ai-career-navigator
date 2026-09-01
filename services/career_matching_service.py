"""
Career Matching Service
Evaluates candidate profile, skills, education, and interests across 14+ career tracks.
Produces transparent match percentages, fit rationale, and personalized strengths/gaps.
"""
from config import CAREER_TRACKS
from modules.skill_gap_engine import analyze_skill_gaps

class CareerMatchingService:
    @staticmethod
    def match_all_careers(candidate_skills: list, interests: list = None, experience_level: str = "Entry Level") -> list:
        """
        Evaluates candidate skills across all 14+ career tracks.
        Returns sorted recommendations with transparent matching rationale.
        """
        results = []
        interests_set = set(i.lower() for i in (interests or []))

        for role_name, track_info in CAREER_TRACKS.items():
            gap_res = analyze_skill_gaps(candidate_skills, track_info["core_skills"])
            tech_match = gap_res["readiness_score"]
            
            # Bonus points for aligned user interests
            interest_bonus = 0.0
            category_lower = track_info["category"].lower()
            title_lower = role_name.lower()
            if any(term in category_lower or term in title_lower for term in interests_set):
                interest_bonus = 8.0

            # Experience alignment modifier
            exp_mod = 0.0
            if experience_level in ["Entry Level", "Student"] and track_info["difficulty"] in ["Moderate", "Moderate to High"]:
                exp_mod = 4.0
            elif experience_level in ["Experienced", "Senior"] and track_info["difficulty"] in ["High", "Very High"]:
                exp_mod = 5.0

            final_match = round(min(98.0, max(15.0, tech_match * 0.88 + interest_bonus + exp_mod)), 1)
            
            matched_skills = [s["skill"] for s in gap_res["strong_skills"]]
            missing_skills = [s["skill"] for s in gap_res["missing_skills"]]
            developing_skills = [s["skill"] for s in gap_res["moderate_skills"]]

            # Generate match rationale
            if final_match >= 75:
                fit_badge = "🔥 High Match"
                fit_reason = f"Strong foundational alignment in {', '.join(matched_skills[:3]) if matched_skills else 'core tech skills'}."
            elif final_match >= 50:
                fit_badge = "⚡ Moderate Transition"
                fit_reason = f"Good baseline. Bridging {', '.join(missing_skills[:2]) if missing_skills else 'key tools'} will unlock this track."
            else:
                fit_badge = "🌱 Long-Term Goal"
                fit_reason = f"High-growth specialized path requiring prerequisites in {', '.join(missing_skills[:3]) if missing_skills else 'foundational topics'}."

            results.append({
                "role": role_name,
                "category": track_info["category"],
                "icon": track_info["icon"],
                "match_score": final_match,
                "fit_badge": fit_badge,
                "fit_reason": fit_reason,
                "avg_salary": track_info["avg_salary"],
                "demand_growth": track_info["demand_growth"],
                "difficulty": track_info["difficulty"],
                "description": track_info["description"],
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "developing_skills": developing_skills,
                "core_skills": track_info["core_skills"],
                "interview_focus": track_info["interview_focus"]
            })

        # Sort by match score descending
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results

    @staticmethod
    def get_track_details(role_name: str) -> dict:
        """Fetches detailed track metadata."""
        return CAREER_TRACKS.get(role_name, CAREER_TRACKS["Data Analyst"])
