"""
Personalized AI Learning Roadmap Generator
Generates a structured multi-phase learning path tailored to student's skill gaps.
"""

def generate_personalized_roadmap(missing_skills: list, moderate_skills: list, target_role: str) -> list:
    """
    Generates a phase-by-phase personalized learning roadmap:
    Phase 1: Core Fundamentals & Theory
    Phase 2: Technical Tools & Frameworks
    Phase 3: Advanced Skills & Infrastructure (MLOps/Cloud/Spark/Deployment)
    Phase 4: Practical Portfolio Projects
    Phase 5: Mock Interviews & Job Application Prep
    """
    missing_list = [item["skill"] for item in missing_skills]
    mod_list = [item["skill"] for item in moderate_skills]

    phases = []
    
    # Categorize missing & moderate skills into tiers
    foundations = [s for s in missing_list + mod_list if s in ["SQL", "Python", "Statistics", "Hypothesis Testing", "Linear Algebra", "R"]]
    core_tech = [s for s in missing_list + mod_list if s in ["Scikit-learn", "PyTorch", "TensorFlow", "Pandas", "NumPy", "XGBoost", "FastAPI", "React", "A/B Testing"]]
    tools_infra = [s for s in missing_list + mod_list if s in ["Docker", "Kubernetes", "PySpark", "AWS/GCP", "MLOps", "MLflow", "Power BI", "Tableau", "Git", "CI/CD"]]
    advanced_other = [s for s in missing_list + mod_list if s not in foundations and s not in core_tech and s not in tools_infra]

    # Phase 1: Foundational Skill Upgrading
    p1_items = foundations if foundations else (mod_list[:2] if mod_list else ["Advanced SQL Queries & Analytics"])
    phases.append({
        "phase": "Phase 1: Foundations & Fundamentals",
        "duration": "1 - 2 Weeks",
        "focus": "Strengthen foundational analytical & programming concepts",
        "topics": p1_items,
        "action_steps": [
            f"Complete practical exercises in {', '.join(p1_items[:3])}.",
            "Practice LeetCode / HackerRank query challenges & statistical concepts.",
            "Document key formulas and code snippets in GitHub notes."
        ],
        "recommended_resources": [
            "Kaggle Learn - Intro to SQL & Data Science",
            "Coursera - Mathematics for Machine Learning & Data Science",
            "Khan Academy - AP Statistics & Probability"
        ]
    })

    # Phase 2: Core Tools & Machine Learning / Web Mastery
    p2_items = core_tech if core_tech else (missing_list[:3] if missing_list else ["Advanced Feature Engineering & Modeling"])
    phases.append({
        "phase": "Phase 2: Core Frameworks & Algorithm Mastery",
        "duration": "2 - 3 Weeks",
        "focus": f"Master core frameworks required for {target_role}",
        "topics": p2_items,
        "action_steps": [
            f"Build hands-on mini-projects implementing {', '.join(p2_items[:3])}.",
            "Perform end-to-end data cleaning, EDA, hyperparameter tuning, and cross-validation.",
            "Publish Jupyter notebooks to GitHub with clear step-by-step explanations."
        ],
        "recommended_resources": [
            "Scikit-learn Official Documentation & Tutorials",
            "DeepLearning.AI - Machine Learning Specialization",
            "FastAPI Official Docs / Streamlit Learning Hub"
        ]
    })

    # Phase 3: Deployment, Cloud & MLOps Infrastructure
    p3_items = tools_infra + advanced_other if (tools_infra or advanced_other) else ["Model API Deployment & Containerization"]
    phases.append({
        "phase": "Phase 3: Production Deployment & MLOps",
        "duration": "2 Weeks",
        "focus": "Turn models and scripts into production-ready cloud services",
        "topics": p3_items,
        "action_steps": [
            "Containerize applications with Docker and compose services.",
            "Deploy REST endpoints to cloud platforms (Streamlit Cloud, Hugging Face, Render, AWS).",
            "Integrate automated logging, model evaluation metrics, and API documentation."
        ],
        "recommended_resources": [
            "Docker for Beginners Guide (FreeCodeCamp)",
            "MLOps Specialization by Andrew Ng (Coursera)",
            "Hugging Face Spaces & Streamlit Deployment Guides"
        ]
    })

    # Phase 4: Capstone Portfolio Projects
    phases.append({
        "phase": "Phase 4: Target Portfolio Projects",
        "duration": "2 Weeks",
        "focus": "Build 2 flagship projects specifically solving business challenges",
        "topics": ["End-to-End ML Pipeline", "Interactive Analytics Dashboard", "Cloud API Deployment"],
        "action_steps": [
            f"Build a production-grade portfolio project incorporating missing skills ({', '.join((missing_list + mod_list)[:3])}).",
            "Write clean, modular code with PEP 8 standards, README.md with architecture diagrams.",
            "Record a 2-minute Loom/Loom video demo and add link to resume."
        ],
        "recommended_resources": [
            "GitHub Awesome Machine Learning Projects",
            "Kaggle Master Pipelines & Notebooks"
        ]
    })

    # Phase 5: Interview Prep & Resume Polish
    phases.append({
        "phase": "Phase 5: Interview Preparation & Resume Optimization",
        "duration": "1 Week",
        "focus": "Acing technical interviews and updating resume with new projects",
        "topics": ["Technical Coding", "System Design / ML Architecture", "Behavioral STAR Stories"],
        "action_steps": [
            "Update Resume with newly acquired skills and metrics-backed project descriptions.",
            "Practice mock interview sessions on AI Interview Coach module.",
            "Prepare 5 STAR-method stories detailing problem, approach, tech stack, and quantitative results."
        ],
        "recommended_resources": [
            "Ace the Data Science Interview (Nick Singh)",
            "LeetCode Data Structures & SQL 50 Study Plan"
        ]
    })

    return phases
