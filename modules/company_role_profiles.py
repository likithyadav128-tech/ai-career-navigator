"""
Company & Role Intelligence Taxonomy Module
Defines target role skill weightings, company profile expectations, and skill dependency knowledge graphs.
"""

ROLE_TAXONOMY = {
    "Data Analyst": {
        "title": "Data Analyst",
        "description": "Transforms raw business data into actionable insights through SQL queries, statistical analysis, and interactive executive dashboards.",
        "skill_weights": {
            "SQL": 25,
            "Python": 15,
            "Excel": 10,
            "Power BI": 15,
            "Tableau": 10,
            "Statistics": 10,
            "Exploratory Data Analysis": 10,
            "Communication": 5
        },
        "core_skills": ["SQL", "Python", "Excel", "Power BI", "Tableau", "Statistics", "Exploratory Data Analysis", "Communication"]
    },
    "Data Scientist": {
        "title": "Data Scientist",
        "description": "Builds statistical models, machine learning algorithms, and experimental pipelines to predict business outcomes and solve complex problems.",
        "skill_weights": {
            "Python": 20,
            "SQL": 20,
            "Machine Learning": 15,
            "Scikit-learn": 10,
            "Statistics": 10,
            "Hypothesis Testing": 10,
            "Pandas": 5,
            "PyTorch": 5,
            "FastAPI": 5
        },
        "core_skills": ["Python", "SQL", "Machine Learning", "Scikit-learn", "Statistics", "Hypothesis Testing", "Pandas", "PyTorch", "FastAPI"]
    },
    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "description": "Designs, trains, containerizes, and deploys high-throughput machine learning models and MLOps pipelines in cloud environments.",
        "skill_weights": {
            "Python": 15,
            "PyTorch": 15,
            "Machine Learning": 15,
            "MLOps": 15,
            "Docker": 10,
            "FastAPI": 10,
            "SQL": 10,
            "Kubernetes": 5,
            "CI/CD": 5
        },
        "core_skills": ["Python", "PyTorch", "Machine Learning", "MLOps", "Docker", "FastAPI", "SQL", "Kubernetes", "CI/CD"]
    },
    "AI / LLM Engineer": {
        "title": "AI / LLM Engineer",
        "description": "Develops Generative AI applications, Retrieval-Augmented Generation (RAG) systems, vector database search, and fine-tunes LLMs.",
        "skill_weights": {
            "Python": 20,
            "LLMs": 20,
            "PyTorch": 15,
            "Hugging Face": 15,
            "FastAPI": 10,
            "Docker": 10,
            "Streamlit": 5,
            "Vector Databases": 5
        },
        "core_skills": ["Python", "LLMs", "PyTorch", "Hugging Face", "FastAPI", "Docker", "Streamlit", "Vector Databases"]
    },
    "Data Engineer": {
        "title": "Data Engineer",
        "description": "Architects reliable data pipelines, ETL workflows, database schemas, and big data infrastructure for downstream analytics.",
        "skill_weights": {
            "SQL": 25,
            "Python": 20,
            "PostgreSQL": 15,
            "PySpark": 15,
            "Docker": 10,
            "AWS": 10,
            "Apache Kafka": 5
        },
        "core_skills": ["SQL", "Python", "PostgreSQL", "PySpark", "Docker", "AWS", "Apache Kafka"]
    },
    "Full-Stack Developer": {
        "title": "Full-Stack Developer",
        "description": "Builds end-to-end web applications covering frontend user interfaces, backend REST APIs, and database management.",
        "skill_weights": {
            "JavaScript": 20,
            "React": 20,
            "Node.js": 15,
            "Python": 15,
            "FastAPI": 10,
            "PostgreSQL": 10,
            "Git": 5,
            "Docker": 5
        },
        "core_skills": ["JavaScript", "React", "Node.js", "Python", "FastAPI", "PostgreSQL", "Git", "Docker"]
    },
    "Frontend Developer": {
        "title": "Frontend Developer",
        "description": "Crafts responsive, performant, and intuitive user interfaces using modern JavaScript/TypeScript frameworks and UI libraries.",
        "skill_weights": {
            "JavaScript": 25,
            "TypeScript": 20,
            "React": 25,
            "HTML/CSS": 15,
            "Tailwind CSS": 10,
            "Git": 5
        },
        "core_skills": ["JavaScript", "TypeScript", "React", "HTML/CSS", "Tailwind CSS", "Git"]
    },
    "Backend Developer": {
        "title": "Backend Developer",
        "description": "Designs scalable server architecture, database schemas, REST APIs, authentication protocols, and microservices.",
        "skill_weights": {
            "Python": 25,
            "FastAPI": 20,
            "SQL": 20,
            "PostgreSQL": 15,
            "Docker": 10,
            "Redis": 5,
            "Git": 5
        },
        "core_skills": ["Python", "FastAPI", "SQL", "PostgreSQL", "Docker", "Redis", "Git"]
    },
    "Cloud / DevOps Engineer": {
        "title": "Cloud / DevOps Engineer",
        "description": "Automates CI/CD pipelines, manages cloud infrastructure, container orchestration, monitoring, and security compliance.",
        "skill_weights": {
            "Docker": 25,
            "Kubernetes": 20,
            "AWS": 20,
            "CI/CD": 15,
            "Linux": 10,
            "Bash": 10
        },
        "core_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Bash"]
    },
    "Cybersecurity Analyst": {
        "title": "Cybersecurity Analyst",
        "description": "Protects organizational networks, monitors threat logs, performs vulnerability assessments, and enforces security compliance.",
        "skill_weights": {
            "Network Security": 25,
            "Linux": 20,
            "Python": 15,
            "Bash": 15,
            "SIEM": 15,
            "Risk Assessment": 10
        },
        "core_skills": ["Network Security", "Linux", "Python", "Bash", "SIEM", "Risk Assessment"]
    }
}

COMPANY_PROFILES = {
    "Any Company (General Industry Standard)": {
        "name": "General Industry Standard",
        "focus_multiplier": {"Technical Skills": 1.0, "Projects": 1.0, "Interview": 1.0},
        "description": "Balanced focus across technical skills, portfolio evidence, and structured communication."
    },
    "TCS / Service Majors (Core Fundamentals & Aptitude)": {
        "name": "TCS & IT Services",
        "focus_multiplier": {"Technical Skills": 1.2, "Assessments": 1.3, "Communication": 1.1},
        "description": "Strong emphasis on core programming fundamentals, SQL queries, aptitude, and verbal communication."
    },
    "Amazon / Tier-1 Product (Coding Rigor & System Architecture)": {
        "name": "Amazon & Tier-1 Product",
        "focus_multiplier": {"Projects": 1.3, "Coding": 1.4, "Interview": 1.2},
        "description": "Heavily weights deep data structures/algorithms, system architecture, leadership principles, and deployed projects."
    },
    "Google / Big Tech (Algorithmic Excellence & Innovation)": {
        "name": "Google & Big Tech",
        "focus_multiplier": {"Coding": 1.5, "Technical Skills": 1.3, "Projects": 1.2},
        "description": "Focuses on algorithm optimization, mathematical computer science foundation, and scalable system design."
    },
    "Deloitte / Consulting (Analytics & Data Storytelling)": {
        "name": "Deloitte & Consulting",
        "focus_multiplier": {"Communication": 1.4, "Resume": 1.2, "Projects": 1.2},
        "description": "Emphasizes executive data storytelling, dashboarding, business presentation skills, and client-facing communication."
    }
}

SKILL_DEPENDENCY_GRAPH = {
    "Data Analyst": [
        {"skill": "SQL", "level": 1, "prereqs": []},
        {"skill": "JOINs", "level": 2, "prereqs": ["SQL"]},
        {"skill": "Window Functions", "level": 3, "prereqs": ["JOINs"]},
        {"skill": "Python", "level": 1, "prereqs": []},
        {"skill": "Pandas", "level": 2, "prereqs": ["Python"]},
        {"skill": "Statistics", "level": 1, "prereqs": []},
        {"skill": "Hypothesis Testing", "level": 2, "prereqs": ["Statistics"]},
        {"skill": "Power BI", "level": 1, "prereqs": []},
        {"skill": "Executive Dashboards", "level": 2, "prereqs": ["Power BI"]}
    ],
    "Data Scientist": [
        {"skill": "Python", "level": 1, "prereqs": []},
        {"skill": "NumPy & Pandas", "level": 2, "prereqs": ["Python"]},
        {"skill": "Statistics", "level": 1, "prereqs": []},
        {"skill": "Machine Learning", "level": 2, "prereqs": ["Python", "Statistics"]},
        {"skill": "Scikit-learn", "level": 3, "prereqs": ["Machine Learning"]},
        {"skill": "PyTorch", "level": 3, "prereqs": ["Machine Learning"]},
        {"skill": "SQL", "level": 1, "prereqs": []},
        {"skill": "FastAPI Deployment", "level": 3, "prereqs": ["Python"]}
    ],
    "Machine Learning Engineer": [
        {"skill": "Python", "level": 1, "prereqs": []},
        {"skill": "PyTorch", "level": 2, "prereqs": ["Python"]},
        {"skill": "Docker", "level": 2, "prereqs": []},
        {"skill": "MLOps", "level": 3, "prereqs": ["PyTorch", "Docker"]},
        {"skill": "FastAPI", "level": 2, "prereqs": ["Python"]},
        {"skill": "Kubernetes", "level": 4, "prereqs": ["Docker"]}
    ]
}
