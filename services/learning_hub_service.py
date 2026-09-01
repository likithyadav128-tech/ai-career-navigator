"""
Curated Learning Hub Service
Provides categorized, filterable, and bookmarkable learning resources across Beginner, Intermediate, and Advanced tiers.
"""
from database.db_connection import get_connection

DEFAULT_LEARNING_RESOURCES = [
    {
        "id": "res_sql_1",
        "title": "SQL for Data Analytics & Window Functions",
        "category": "Databases & Querying",
        "tier": "Beginner to Intermediate",
        "platform": "PostgreSQL Official / Mode Analytics",
        "url": "https://mode.com/sql-tutorial/",
        "duration": "12 hours",
        "skills": ["SQL", "JOINs", "Window Functions", "Subqueries & CTEs"],
        "description": "Comprehensive interactive SQL tutorial covering everything from fundamental SELECT and JOINs to advanced analytical window functions."
    },
    {
        "id": "res_python_ds",
        "title": "Python Data Science Handbook & Pandas Labs",
        "category": "Data Wrangling",
        "tier": "Intermediate",
        "platform": "O'Reilly Open Book",
        "url": "https://jakevdp.github.io/PythonDataScienceHandbook/",
        "duration": "18 hours",
        "skills": ["Python", "Pandas", "NumPy", "Matplotlib", "Scikit-learn"],
        "description": "Essential guide to data science computing in Python: efficient NumPy arrays, Pandas data manipulation, and visualization."
    },
    {
        "id": "res_ml_cousera",
        "title": "Machine Learning Specialization",
        "category": "Machine Learning",
        "tier": "Intermediate to Advanced",
        "platform": "DeepLearning.AI / Coursera",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "duration": "30 hours",
        "skills": ["Machine Learning", "Scikit-learn", "Statistics", "Feature Engineering"],
        "description": "Foundational course on supervised, unsupervised, and reinforcement learning by Andrew Ng."
    },
    {
        "id": "res_fastapi_ml",
        "title": "Building Production ML APIs with FastAPI & Docker",
        "category": "Deployment & MLOps",
        "tier": "Advanced",
        "platform": "FastAPI Official Guide",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "duration": "10 hours",
        "skills": ["FastAPI", "Docker", "Python", "REST APIs"],
        "description": "Learn to wrap scikit-learn/PyTorch models in high-performance asynchronous REST endpoints and containerize with Docker."
    },
    {
        "id": "res_rag_langchain",
        "title": "Generative AI with Large Language Models & RAG",
        "category": "Artificial Intelligence",
        "tier": "Advanced",
        "platform": "Hugging Face & DeepLearning.AI",
        "url": "https://huggingface.co/learn/nlp-course/",
        "duration": "24 hours",
        "skills": ["LLMs", "RAG", "PyTorch", "Hugging Face", "Vector Databases"],
        "description": "In-depth course on Transformers, attention mechanisms, fine-tuning LLMs, and building vector database search pipelines."
    },
    {
        "id": "res_bi_powerbi",
        "title": "Power BI & Tableau Executive Dashboard Masterclass",
        "category": "Visualization & BI",
        "tier": "Beginner to Intermediate",
        "platform": "Microsoft Learn & Tableau Public",
        "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi",
        "duration": "14 hours",
        "skills": ["Power BI", "Tableau", "Executive Dashboards", "Data Storytelling"],
        "description": "Build high-impact KPI scorecards, interactive cross-filtering visuals, and executive business summaries."
    },
    {
        "id": "res_devops_docker",
        "title": "Docker & Kubernetes Architecture from Scratch",
        "category": "Cloud & DevOps",
        "tier": "Intermediate to Advanced",
        "platform": "Kubernetes Docs",
        "url": "https://kubernetes.io/docs/tutorials/",
        "duration": "20 hours",
        "skills": ["Docker", "Kubernetes", "CI/CD", "Linux"],
        "description": "Master containerization, multi-stage builds, pods, deployments, service meshes, and Helm charts."
    },
    {
        "id": "res_stats_ab",
        "title": "Practical Statistics for Data Scientists & A/B Testing",
        "category": "Mathematics & Statistics",
        "tier": "Intermediate",
        "platform": "StatQuest / OpenIntro",
        "url": "https://www.openintro.org/book/os/",
        "duration": "15 hours",
        "skills": ["Statistics", "Hypothesis Testing", "A/B Testing"],
        "description": "Clear conceptual explanations of p-values, confidence intervals, sample size calculations, and statistical experimentation."
    }
]

class LearningHubService:
    @staticmethod
    def get_resources(filter_skill: str = None, filter_tier: str = None) -> list:
        """Filters learning resources by skill keyword or difficulty tier."""
        results = []
        for r in DEFAULT_LEARNING_RESOURCES:
            if filter_skill and filter_skill != "All Skills":
                if not any(filter_skill.lower() in s.lower() for s in r["skills"]):
                    continue
            if filter_tier and filter_tier != "All Levels":
                if filter_tier.lower() not in r["tier"].lower():
                    continue
            results.append(r)
        return results

    @staticmethod
    def bookmark_resource(user_id: int, res_id: str, title: str, url: str, category: str):
        """Saves a bookmark in SQLite."""
        if not user_id:
            return
        conn = get_connection()
        cursor = conn.cursor()
        from datetime import datetime
        now_str = datetime.now().isoformat()
        cursor.execute("""
        INSERT OR IGNORE INTO user_bookmarks (user_id, resource_id, resource_title, resource_url, category, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, res_id, title, url, category, now_str))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_bookmarks(user_id: int) -> list:
        """Retrieves user bookmarks."""
        if not user_id:
            return []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT resource_id, resource_title, resource_url, category, created_at FROM user_bookmarks WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
