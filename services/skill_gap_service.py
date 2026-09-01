"""
Skill Gap & Prerequisite Tree Service
Wraps skill gap analysis, prerequisite mastery evaluation, and top improvement recommendations.
"""
from modules.skill_gap_engine import analyze_skill_gaps
from modules.hierarchical_skill_tree import analyze_hierarchical_skill_tree
from config import CAREER_TRACKS

class SkillGapService:
    @staticmethod
    def evaluate_gaps(candidate_skills: list, target_role: str) -> dict:
        """Performs full gap analysis and returns structured breakdown."""
        track = CAREER_TRACKS.get(target_role, CAREER_TRACKS["Data Analyst"])
        gap_res = analyze_skill_gaps(candidate_skills, track["core_skills"])
        hierarchy_res = analyze_hierarchical_skill_tree(candidate_skills, target_role)

        # Top 5 Skills to Improve (sorted by prerequisite unlock priority)
        top_improvements = []
        for tgt in hierarchy_res.get("next_learning_targets", []):
            top_improvements.append({
                "skill": tgt["skill"],
                "level": tgt["level"],
                "category": tgt["category"],
                "prereqs": tgt["prereqs"],
                "impact": "Unlocks next tier skills and boosts technical readiness"
            })

        # If less than 5, pull from missing skills
        for m in gap_res.get("missing_skills", []):
            if len(top_improvements) >= 5:
                break
            if not any(t["skill"] == m["skill"] for t in top_improvements):
                top_improvements.append({
                    "skill": m["skill"],
                    "level": 2,
                    "category": "Core Role Requirement",
                    "prereqs": [],
                    "impact": "Required by industry standard job descriptions"
                })

        return {
            "gap_analysis": gap_res,
            "hierarchy_tree": hierarchy_res,
            "top_improvements": top_improvements[:5],
            "technical_match_pct": gap_res["readiness_score"]
        }
