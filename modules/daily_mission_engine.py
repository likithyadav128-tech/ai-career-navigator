"""
Daily Career Mission Engine ("What Should I Do Today?")
Generates daily 90-minute actionable missions with readiness point rewards.
"""

def generate_daily_career_mission(missing_skills: list, moderate_skills: list, target_role: str = "Data Analyst") -> dict:
    """
    Generates a personalized 4-task daily mission designed to boost student readiness score.
    Total estimated time: 90 minutes.
    """
    top_missing = missing_skills[0]["skill"] if missing_skills else "Advanced SQL & Analytics"
    second_missing = missing_skills[1]["skill"] if len(missing_skills) > 1 else (moderate_skills[0]["skill"] if moderate_skills else "Power BI Dashboards")

    tasks = [
        {
            "id": 1,
            "title": f"Task 1 — Core Skill Focus: {top_missing}",
            "category": "Technical Skill",
            "time_estimate": "35 mins",
            "points": "+2.0 readiness pts",
            "description": f"Solve 5 practice problems focused on {top_missing}.",
            "action_type": "practice"
        },
        {
            "id": 2,
            "title": f"Task 2 — Resume Optimization",
            "category": "Resume",
            "time_estimate": "15 mins",
            "points": "+1.5 readiness pts",
            "description": f"Rewrite 2 project bullet points for {target_role} using STAR method and quantitative metrics.",
            "action_type": "resume"
        },
        {
            "id": 3,
            "title": f"Task 3 — Interview Practice",
            "category": "Interview",
            "time_estimate": "25 mins",
            "points": "+2.0 readiness pts",
            "description": f"Answer 3 technical interview questions for {target_role} on the AI Mock Interview Coach.",
            "action_type": "interview"
        },
        {
            "id": 4,
            "title": f"Task 4 — Project & GitHub Evidence: {second_missing}",
            "category": "Project",
            "time_estimate": "15 mins",
            "points": "+1.0 readiness pts",
            "description": f"Add clean README documentation or container setup to your {second_missing} repository.",
            "action_type": "github"
        }
    ]

    total_time = "90 minutes"
    total_potential_boost = "+6.5 readiness points"

    return {
        "title": f"Today's Career Mission — Target: {target_role}",
        "estimated_time": total_time,
        "potential_boost": total_potential_boost,
        "tasks": tasks
    }
