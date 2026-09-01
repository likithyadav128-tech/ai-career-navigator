"""
Dynamic Career Roadmap Service
Generates an 8-stage step-by-step career path tailored to target role and skill gaps.
Stages: Foundation → Core Skills → Advanced Skills → Projects → Resume → Interview → Applications → Career Ready.
"""
from database.roadmap_repo import load_user_roadmap_progress, save_task_completion
from config import CAREER_TRACKS

class RoadmapService:
    @staticmethod
    def generate_8_stage_roadmap(user_id: int, missing_skills: list, moderate_skills: list, target_role: str) -> list:
        """
        Generates 8-stage career roadmap with interactive task IDs and persistent completion states.
        """
        user_progress = load_user_roadmap_progress(user_id) if user_id else {}
        track = CAREER_TRACKS.get(target_role, CAREER_TRACKS["Data Analyst"])
        
        miss_str = ", ".join(missing_skills[:3]) if missing_skills else "advanced domain frameworks"
        core_skills_sample = ", ".join(track["core_skills"][:4])

        phases = [
            {
                "phase_num": 1,
                "title": "Stage 1: Foundational Literacy & Tools",
                "duration": "Weeks 1 - 2",
                "difficulty": "Beginner",
                "focus": f"Master core syntax and developer workspace setup for {target_role}.",
                "tasks": [
                    {"id": "s1_t1", "title": "Configure Git, GitHub, and IDE development environment", "time": "2 hrs", "res": "Git Documentation"},
                    {"id": "s1_t2", "title": f"Complete foundational syntax exercises in {track['core_skills'][0] if track['core_skills'] else 'Python'}", "time": "6 hrs", "res": "Interactive Tutorials"},
                    {"id": "s1_t3", "title": "Build and push your first structured GitHub repository", "time": "3 hrs", "res": "GitHub Guides"}
                ]
            },
            {
                "phase_num": 2,
                "title": "Stage 2: Core Technical Competencies",
                "duration": "Weeks 3 - 5",
                "difficulty": "Intermediate",
                "focus": f"Gain hands-on proficiency in core required toolkits ({core_skills_sample}).",
                "tasks": [
                    {"id": "s2_t1", "title": f"Study and practice intermediate workflows for {track['core_skills'][1] if len(track['core_skills']) > 1 else 'SQL'}", "time": "8 hrs", "res": "Documentation & Labs"},
                    {"id": "s2_t2", "title": f"Bridge identified high-priority skill gap: {missing_skills[0] if missing_skills else 'Advanced Data Modeling'}", "time": "10 hrs", "res": "Specialized Courseware"},
                    {"id": "s2_t3", "title": "Implement 3 self-guided code katas/mini-challenges", "time": "5 hrs", "res": "LeetCode / HackerRank"}
                ]
            },
            {
                "phase_num": 3,
                "title": "Stage 3: Advanced Architectures & Production Tools",
                "duration": "Weeks 6 - 8",
                "difficulty": "Advanced",
                "focus": f"Level up to advanced production standards ({miss_str}).",
                "tasks": [
                    {"id": "s3_t1", "title": f"Learn production design patterns and optimization in {target_role}", "time": "8 hrs", "res": "Engineering Blogs"},
                    {"id": "s3_t2", "title": f"Bridge secondary gap: {missing_skills[1] if len(missing_skills) > 1 else 'Cloud / CI/CD Deployment'}", "time": "10 hrs", "res": "Hands-on Workshops"},
                    {"id": "s3_t3", "title": "Write unit tests and optimize pipeline performance", "time": "4 hrs", "res": "Testing Frameworks"}
                ]
            },
            {
                "phase_num": 4,
                "title": "Stage 4: Flagship Portfolio Project",
                "duration": "Weeks 9 - 11",
                "difficulty": "Advanced",
                "focus": "Build and deploy an end-to-end industry-grade flagship project.",
                "tasks": [
                    {"id": "s4_t1", "title": f"Architect flagship project addressing real-world {target_role} problem", "time": "4 hrs", "res": "Project Blueprint Generator"},
                    {"id": "s4_t2", "title": "Build modular codebase with clean separation and documentation", "time": "16 hrs", "res": "Clean Code Standards"},
                    {"id": "s4_t3", "title": "Deploy project live to cloud (Streamlit / Render / AWS) with interactive demo", "time": "4 hrs", "res": "Cloud Deployment Docs"},
                    {"id": "s4_t4", "title": "Write comprehensive README.md with architecture diagram and metrics", "time": "3 hrs", "res": "README Templates"}
                ]
            },
            {
                "phase_num": 5,
                "title": "Stage 5: ATS Resume & Profile Optimization",
                "duration": "Week 12",
                "difficulty": "Intermediate",
                "focus": f"Transform resume bullets with STAR method impact tailored to {target_role}.",
                "tasks": [
                    {"id": "s5_t1", "title": "Run Resume ATS Audit and achieve 85+ quality score", "time": "2 hrs", "res": "Resume AI Studio"},
                    {"id": "s5_t2", "title": "Rewrite project bullets using STAR action verbs and quantitative metrics", "time": "3 hrs", "res": "Bullet Point Optimizer"},
                    {"id": "s5_t3", "title": "Update LinkedIn and GitHub profiles with live flagship project link", "time": "2 hrs", "res": "Portfolio Builder"}
                ]
            },
            {
                "phase_num": 6,
                "title": "Stage 6: Mock Interview Lab & Technical Drills",
                "duration": "Weeks 13 - 14",
                "difficulty": "Advanced",
                "focus": f"Master technical deep-dives and behavioral interview questions for {target_role}.",
                "tasks": [
                    {"id": "s6_t1", "title": f"Practice 10 role-specific questions: {track['interview_focus']}", "time": "5 hrs", "res": "Interview Lab"},
                    {"id": "s6_t2", "title": "Complete HR behavioral interview simulation using STAR communication", "time": "3 hrs", "res": "STAR Coach"},
                    {"id": "s6_t3", "title": "Review AI communication feedback and refine timing/conciseness", "time": "2 hrs", "res": "Feedback Analytics"}
                ]
            },
            {
                "phase_num": 7,
                "title": "Stage 7: Targeted Job Applications & Networking",
                "duration": "Weeks 15 - 16",
                "difficulty": "Moderate",
                "focus": "Execute structured application pipeline across 15+ target companies.",
                "tasks": [
                    {"id": "s7_t1", "title": "Identify and save 15 target company job postings in Application Tracker", "time": "3 hrs", "res": "Job Tracker"},
                    {"id": "s7_t2", "title": "Reach out to 5 engineers/managers on LinkedIn for informational chats", "time": "3 hrs", "res": "Networking Templates"},
                    {"id": "s7_t3", "title": "Submit 10 tailored applications with customized resume keywords", "time": "6 hrs", "res": "Job Tracker Kanban"}
                ]
            },
            {
                "phase_num": 8,
                "title": "Stage 8: Offer Negotiation & Career Launch",
                "duration": "Ongoing",
                "difficulty": "Moderate",
                "focus": "Evaluate offers, negotiate compensation packages, and onboard smoothly.",
                "tasks": [
                    {"id": "s8_t1", "title": "Conduct final interview debriefs and log feedback", "time": "2 hrs", "res": "Job Tracker"},
                    {"id": "s8_t2", "title": f"Review market salary benchmarks ({track['avg_salary']}) for negotiation", "time": "2 hrs", "res": "Salary Insights"},
                    {"id": "s8_t3", "title": "Launch public career portfolio link to showcase verified skills", "time": "1 hr", "res": "Public Portfolio"}
                ]
            }
        ]

        # Annotate completion status and calculate totals
        total_tasks = 0
        completed_tasks = 0

        for p in phases:
            p_done = 0
            for t in p["tasks"]:
                total_tasks += 1
                is_done = user_progress.get(t["id"], False)
                t["is_completed"] = is_done
                if is_done:
                    completed_tasks += 1
                    p_done += 1
            p["completed_count"] = p_done
            p["total_count"] = len(p["tasks"])
            p["is_phase_completed"] = (p_done == len(p["tasks"]))

        return {
            "phases": phases,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overall_progress_pct": round((completed_tasks / total_tasks * 100) if total_tasks else 0, 1)
        }

    @staticmethod
    def toggle_task(user_id: int, phase_title: str, task_id: str, new_status: bool):
        """Toggles task completion state in SQLite."""
        if user_id:
            save_task_completion(user_id, phase_title, task_id, new_status)
