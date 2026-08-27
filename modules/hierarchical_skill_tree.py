"""
Hierarchical Skill Tree & Prerequisite Mastery Engine
Renders visual skill hierarchies showing Strong/Mastered skills, Next Immediate Learning Targets, and Prerequisite Dependencies.
"""

# Skill Hierarchy Taxonomy for Major Tech Roles
ROLE_SKILL_HIERARCHIES = {
    "Data Analyst": [
        # Level 1: Foundations
        {"skill": "SQL", "level": 1, "prereqs": [], "category": "Databases & Querying"},
        {"skill": "Python", "level": 1, "prereqs": [], "category": "Programming"},
        {"skill": "Excel", "level": 1, "prereqs": [], "category": "Spreadsheets"},
        {"skill": "Statistics", "level": 1, "prereqs": [], "category": "Mathematics"},
        
        # Level 2: Core Analytics & Data Wrangling
        {"skill": "JOINs", "level": 2, "prereqs": ["SQL"], "category": "Databases & Querying"},
        {"skill": "Pandas", "level": 2, "prereqs": ["Python"], "category": "Data Wrangling"},
        {"skill": "NumPy", "level": 2, "prereqs": ["Python"], "category": "Data Wrangling"},
        {"skill": "Power BI", "level": 2, "prereqs": ["Excel"], "category": "Visualization"},
        {"skill": "Tableau", "level": 2, "prereqs": ["Excel"], "category": "Visualization"},
        {"skill": "Exploratory Data Analysis", "level": 2, "prereqs": ["Pandas"], "category": "Analytics"},

        # Level 3: Advanced Querying & Statistical Modeling
        {"skill": "Window Functions", "level": 3, "prereqs": ["JOINs"], "category": "Databases & Querying"},
        {"skill": "Subqueries & CTEs", "level": 3, "prereqs": ["JOINs"], "category": "Databases & Querying"},
        {"skill": "Hypothesis Testing", "level": 3, "prereqs": ["Statistics"], "category": "Mathematics"},
        {"skill": "A/B Testing", "level": 3, "prereqs": ["Hypothesis Testing"], "category": "Analytics"},
        {"skill": "Plotly", "level": 3, "prereqs": ["Python"], "category": "Visualization"},

        # Level 4: Executive BI & Production Pipelines
        {"skill": "PostgreSQL", "level": 4, "prereqs": ["Window Functions"], "category": "Databases & Querying"},
        {"skill": "Executive Dashboards", "level": 4, "prereqs": ["Power BI"], "category": "Visualization"},
        {"skill": "Data Storytelling", "level": 4, "prereqs": ["Exploratory Data Analysis"], "category": "Communication"}
    ],
    "Data Scientist": [
        # Level 1: Foundations
        {"skill": "Python", "level": 1, "prereqs": [], "category": "Programming"},
        {"skill": "SQL", "level": 1, "prereqs": [], "category": "Databases"},
        {"skill": "Statistics", "level": 1, "prereqs": [], "category": "Mathematics"},
        {"skill": "Linear Algebra", "level": 1, "prereqs": [], "category": "Mathematics"},

        # Level 2: Core Data Science & Wrangling
        {"skill": "Pandas", "level": 2, "prereqs": ["Python"], "category": "Data Wrangling"},
        {"skill": "NumPy", "level": 2, "prereqs": ["Python"], "category": "Data Wrangling"},
        {"skill": "JOINs", "level": 2, "prereqs": ["SQL"], "category": "Databases"},
        {"skill": "Exploratory Data Analysis", "level": 2, "prereqs": ["Pandas"], "category": "Analytics"},

        # Level 3: Machine Learning & Modeling
        {"skill": "Machine Learning", "level": 3, "prereqs": ["Python", "Statistics"], "category": "ML / AI"},
        {"skill": "Scikit-learn", "level": 3, "prereqs": ["Machine Learning"], "category": "ML / AI"},
        {"skill": "XGBoost", "level": 3, "prereqs": ["Scikit-learn"], "category": "ML / AI"},
        {"skill": "Feature Engineering", "level": 3, "prereqs": ["Pandas"], "category": "Data Wrangling"},
        {"skill": "Hypothesis Testing", "level": 3, "prereqs": ["Statistics"], "category": "Mathematics"},

        # Level 4: Deep Learning & Deployment
        {"skill": "PyTorch", "level": 4, "prereqs": ["Machine Learning"], "category": "Deep Learning"},
        {"skill": "TensorFlow", "level": 4, "prereqs": ["Machine Learning"], "category": "Deep Learning"},
        {"skill": "FastAPI", "level": 4, "prereqs": ["Python"], "category": "Deployment"},
        {"skill": "Docker", "level": 4, "prereqs": ["FastAPI"], "category": "Infrastructure"}
    ],
    "Machine Learning Engineer": [
        # Level 1: Foundations
        {"skill": "Python", "level": 1, "prereqs": [], "category": "Programming"},
        {"skill": "Git", "level": 1, "prereqs": [], "category": "Version Control"},
        {"skill": "SQL", "level": 1, "prereqs": [], "category": "Databases"},

        # Level 2: ML & Web Basics
        {"skill": "Machine Learning", "level": 2, "prereqs": ["Python"], "category": "ML / AI"},
        {"skill": "Scikit-learn", "level": 2, "prereqs": ["Machine Learning"], "category": "ML / AI"},
        {"skill": "FastAPI", "level": 2, "prereqs": ["Python"], "category": "Web APIs"},
        {"skill": "Docker", "level": 2, "prereqs": ["Git"], "category": "Containers"},

        # Level 3: Deep Learning & MLOps
        {"skill": "PyTorch", "level": 3, "prereqs": ["Machine Learning"], "category": "Deep Learning"},
        {"skill": "MLOps", "level": 3, "prereqs": ["Docker", "Machine Learning"], "category": "MLOps"},
        {"skill": "MLflow", "level": 3, "prereqs": ["MLOps"], "category": "MLOps"},

        # Level 4: Scalable Infrastructure
        {"skill": "Kubernetes", "level": 4, "prereqs": ["Docker"], "category": "Infrastructure"},
        {"skill": "CI/CD", "level": 4, "prereqs": ["Git", "Docker"], "category": "DevOps"},
        {"skill": "CUDA", "level": 4, "prereqs": ["PyTorch"], "category": "Hardware Acceleration"}
    ]
}

def analyze_hierarchical_skill_tree(candidate_skills: list, target_role: str = "Data Analyst") -> dict:
    """
    Analyzes skill mastery based on hierarchy level and prerequisite readiness.
    
    Status Rules:
    - 🟢 STRONG / MASTERED: Candidate possesses exact skill.
    - 🚀 NEXT IMMEDIATE LEARNING TARGET: Skill missing, BUT ALL PREREQUISITES ARE SATISFIED!
    - 🔒 BLOCKED: Skill missing AND one or more prerequisites are missing.
    """
    cand_set = {s.lower() for s in candidate_skills}
    hierarchy = ROLE_SKILL_HIERARCHIES.get(target_role, ROLE_SKILL_HIERARCHIES["Data Analyst"])
    
    levels = {1: [], 2: [], 3: [], 4: []}
    
    mastered_count = 0
    next_target_count = 0
    blocked_count = 0
    
    next_learning_targets = []

    for item in hierarchy:
        skill_name = item["skill"]
        level = item["level"]
        prereqs = item["prereqs"]
        category = item["category"]
        
        # Check if candidate has skill
        has_skill = skill_name.lower() in cand_set
        
        # Check prerequisites
        missing_prereqs = [p for p in prereqs if p.lower() not in cand_set]
        prereqs_satisfied = len(missing_prereqs) == 0
        
        if has_skill:
            status = "🟢 Mastered / Strong"
            status_code = "STRONG"
            mastered_count += 1
            reason = "Skill present on resume profile"
        elif prereqs_satisfied:
            status = "🚀 Next Immediate Learning Target"
            status_code = "NEXT_TARGET"
            next_target_count += 1
            reason = "Prerequisites satisfied! Ready to learn now."
            next_learning_targets.append({
                "skill": skill_name,
                "level": level,
                "category": category,
                "prereqs": prereqs
            })
        else:
            status = "🔒 Blocked by Prerequisites"
            status_code = "BLOCKED"
            blocked_count += 1
            reason = f"Requires prerequisite: {', '.join(missing_prereqs)}"

        levels[level].append({
            "skill": skill_name,
            "level": level,
            "category": category,
            "status": status,
            "status_code": status_code,
            "prereqs": prereqs,
            "missing_prereqs": missing_prereqs,
            "reason": reason
        })

    return {
        "target_role": target_role,
        "levels": levels,
        "summary": {
            "mastered": mastered_count,
            "next_targets": next_target_count,
            "blocked": blocked_count,
            "total_skills": len(hierarchy)
        },
        "next_learning_targets": next_learning_targets
    }
