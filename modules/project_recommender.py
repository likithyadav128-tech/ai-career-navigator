"""
AI Project Recommender Engine
Suggests tailored portfolio projects matching the student's identified skill gaps and target role.
"""

PROJECT_CATALOG = [
    {
        "title": "Real-Time Customer Churn & LTV Predictive Engine",
        "role_category": "Data Scientist",
        "difficulty": "Intermediate",
        "tech_stack": ["Python", "Scikit-learn", "XGBoost", "FastAPI", "Docker", "Streamlit"],
        "target_skills": ["XGBoost", "FastAPI", "Docker", "Feature Engineering", "A/B Testing"],
        "description": "Build an end-to-end customer churn prediction dashboard. Train XGBoost model on transaction logs, serve via FastAPI endpoint, and wrap in Streamlit frontend with interactive churn risk sliders.",
        "architecture_steps": [
            "Data Extraction & SMOTE imbalance handling in Pandas",
            "Model training with Optuna hyperparameter tuning",
            "FastAPI REST API server creation",
            "Streamlit visual dashboard integration",
            "Docker container deployment"
        ]
    },
    {
        "title": "Enterprise SQL & Business Intelligence Analytics Suite",
        "role_category": "Data Analyst",
        "difficulty": "Beginner-Intermediate",
        "tech_stack": ["PostgreSQL", "Power BI / Tableau", "Python", "Pandas", "Plotly"],
        "target_skills": ["SQL", "PostgreSQL", "Power BI", "Tableau", "Hypothesis Testing"],
        "description": "Construct complex SQL database schemas for multi-channel sales. Write window functions, CTEs, and aggregated view queries to feed real-time KPI executive dashboards.",
        "architecture_steps": [
            "Design normalized relational PostgreSQL database schema",
            "Populate mock transactional dataset with 100k records",
            "Write analytical SQL queries using ROW_NUMBER(), DENSE_RANK(), LAG/LEAD",
            "Connect Power BI / Tableau dashboard with drill-down metrics"
        ]
    },
    {
        "title": "Production MLOps Pipeline with MLflow & Docker",
        "role_category": "Machine Learning Engineer",
        "difficulty": "Advanced",
        "tech_stack": ["PyTorch", "MLOps", "MLflow", "Docker", "Kubernetes", "FastAPI", "CI/CD"],
        "target_skills": ["MLOps", "MLflow", "Docker", "Kubernetes", "PyTorch", "CI/CD"],
        "description": "Implement automated model tracking, registry, CI/CD pipeline, and continuous deployment for deep learning image/text classification models.",
        "architecture_steps": [
            "Train PyTorch classification model with experiment logging in MLflow",
            "Register best performing artifact in MLflow Model Registry",
            "Build Docker image with auto-reloading FastAPI endpoint",
            "Set up GitHub Actions CI/CD workflow for automated unit tests & deployment"
        ]
    },
    {
        "title": "LLM-Powered Document Q&A RAG System",
        "role_category": "AI / NLP Engineer",
        "difficulty": "Intermediate-Advanced",
        "tech_stack": ["Python", "LangChain / LlamaIndex", "Hugging Face", "PyTorch", "Streamlit", "FastAPI"],
        "target_skills": ["LLMs", "Generative AI", "Hugging Face", "BERT", "FastAPI", "Streamlit"],
        "description": "Create Retrieval-Augmented Generation (RAG) platform allowing users to upload dense PDFs, generate embeddings, index in vector store, and receive citation-backed answers.",
        "architecture_steps": [
            "Text chunking & vector embedding generation using Hugging Face transformers",
            "Vector database indexing (FAISS / ChromaDB)",
            "Prompt engineering pipeline with LLM integration",
            "Streamlit interactive chatbot frontend"
        ]
    },
    {
        "title": "A/B Testing & Statistical Experimentation Simulator",
        "role_category": "Data Scientist",
        "difficulty": "Intermediate",
        "tech_stack": ["Python", "Statistics", "Hypothesis Testing", "A/B Testing", "SciPy", "Plotly"],
        "target_skills": ["A/B Testing", "Hypothesis Testing", "Statistics", "Plotly"],
        "description": "Simulate web traffic conversion split tests. Calculate sample sizes, p-values, confidence intervals, and sequential testing metrics with Plotly charts.",
        "architecture_steps": [
            "Generate synthetic user conversion datasets for Control vs Treatment groups",
            "Run two-sample t-test, Chi-Square test, and Mann-Whitney U test using SciPy",
            "Plot distribution curves and power analysis graphs",
            "Build interactive parameter slider dashboard"
        ]
    }
]

def recommend_projects_for_student(missing_skills: list, moderate_skills: list, target_role: str) -> list:
    """
    Ranks catalog projects by matching missing/moderate skills of the student.
    """
    gap_skills = {s["skill"].lower() for s in missing_skills + moderate_skills}
    
    scored_projects = []
    for proj in PROJECT_CATALOG:
        # Match score calculation
        target_matches = [s for s in proj["target_skills"] if s.lower() in gap_skills]
        role_match = 2 if target_role.lower() in proj["role_category"].lower() else 0
        match_score = len(target_matches) * 3 + role_match
        
        scored_projects.append({
            "project": proj,
            "matched_gap_skills": target_matches,
            "score": match_score
        })
        
    # Sort by match score descending
    scored_projects.sort(key=lambda x: x["score"], reverse=True)
    return [item["project"] for item in scored_projects[:3]]
