"""
AI Resume Analyzer Module
Parses PDF resumes, extracts skills & keywords, evaluates ATS quality score, and provides optimization suggestions.
"""

import re
import io
try:
    import pypdf
except ImportError:
    pypdf = None

# Comprehensive Tech & Soft Skills Taxonomy
# Comprehensive Tech & Soft Skills Taxonomy
SKILL_TAXONOMY = {
    # Programming Languages
    "python": "Python", "sql": "SQL", "r": "R", "java": "Java", "c++": "C++", "javascript": "JavaScript",
    "typescript": "TypeScript", "c#": "C#", "go": "Go", "golang": "Go", "rust": "Rust", "bash": "Bash", "scala": "Scala",
    
    # Spreadsheets & Analytical Tools
    "excel": "Excel", "ms excel": "Excel", "microsoft excel": "Excel", "advanced excel": "Excel",
    "vlookup": "Excel", "xlookup": "Excel", "pivot tables": "Excel", "pivot table": "Excel", "spreadsheets": "Excel", "spreadsheet": "Excel",
    
    # SQL & Database Concepts
    "joins": "JOINs", "join": "JOINs", "sql joins": "JOINs", "inner join": "JOINs", "left join": "JOINs", "outer join": "JOINs",
    "window functions": "Window Functions", "analytic functions": "Window Functions", "window function": "Window Functions",
    "subqueries": "Subqueries & CTEs", "subquery": "Subqueries & CTEs", "cte": "Subqueries & CTEs", "ctes": "Subqueries & CTEs",
    "subqueries & ctes": "Subqueries & CTEs", "common table expressions": "Subqueries & CTEs",
    
    # ML / AI / Data Science
    "machine learning": "Machine Learning", "deep learning": "Deep Learning", "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing", "computer vision": "Computer Vision",
    "pytorch": "PyTorch", "tensorflow": "TensorFlow", "scikit-learn": "Scikit-learn", "sklearn": "Scikit-learn",
    "xgboost": "XGBoost", "lightgbm": "LightGBM", "pandas": "Pandas", "numpy": "NumPy", "scipy": "SciPy",
    "bert": "BERT", "transformers": "Transformers", "llm": "LLMs", "large language models": "LLMs",
    "hugging face": "Hugging Face", "langchain": "LangChain", "genai": "Generative AI",
    "vector databases": "Vector Databases", "vector database": "Vector Databases", "vector db": "Vector Databases",
    "pinecone": "Vector Databases", "chromadb": "Vector Databases", "weaviate": "Vector Databases",
    "rag": "RAG", "prompt engineering": "Prompt Engineering", "cuda": "CUDA",
    
    # Data Engineering & Databases
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "mysql": "MySQL", "mongodb": "MongoDB",
    "redis": "Redis", "pyspark": "PySpark", "spark": "Apache Spark", "hadoop": "Hadoop",
    "kafka": "Apache Kafka", "snowflake": "Snowflake", "databricks": "Databricks", "dbt": "dbt",
    
    # Visualization & BI
    "tableau": "Tableau", "power bi": "Power BI", "plotly": "Plotly", "matplotlib": "Matplotlib",
    "seaborn": "Seaborn", "looker": "Looker",
    "dashboards": "Executive Dashboards", "dashboard": "Executive Dashboards",
    "executive dashboards": "Executive Dashboards", "interactive dashboards": "Executive Dashboards",
    "data storytelling": "Data Storytelling", "storytelling": "Data Storytelling",
    
    # Web & API Frameworks
    "fastapi": "FastAPI", "flask": "Flask", "django": "Django", "streamlit": "Streamlit",
    "react": "React", "next.js": "Next.js", "node.js": "Node.js", "express": "Express",
    
    # DevOps, Cloud & Tools
    "docker": "Docker", "kubernetes": "Kubernetes", "aws": "AWS", "gcp": "GCP", "azure": "Azure",
    "git": "Git", "github": "GitHub", "linux": "Linux", "mlops": "MLOps", "ci/cd": "CI/CD",
    "airflow": "Apache Airflow", "mlflow": "MLflow",
    
    # Concepts & Mathematics
    "statistics": "Statistics", "applied statistics": "Statistics", "hypothesis testing": "Hypothesis Testing",
    "a/b testing": "A/B Testing", "feature engineering": "Feature Engineering",
    "linear algebra": "Linear Algebra",
    "eda": "Exploratory Data Analysis", "exploratory data analysis": "Exploratory Data Analysis",
    "time series": "Time Series Forecasting", "recommendation systems": "Recommendation Systems",
    
    # Soft Skills
    "problem solving": "Problem Solving", "communication": "Communication",
    "business communication": "Business Communication", "team collaboration": "Team Collaboration",
    "agile": "Agile", "leadership": "Leadership", "critical thinking": "Critical Thinking"
}

ACTION_VERBS = [
    "developed", "built", "engineered", "designed", "implemented", "optimized", "created",
    "led", "reduced", "increased", "generated", "deployed", "automated", "spearheaded",
    "achieved", "analyzed", "extracted", "fine-tuned", "integrated", "constructed"
]

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file bytes or file-like object."""
    if pypdf is None:
        return "PDF parser not installed."
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip()
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

def extract_skills_from_text(text: str) -> list:
    """Extract recognized technical & soft skills from resume text or skill list."""
    if not text:
        return []
        
    lower_text = text.lower()
    found_skills = set()
    
    # 1. Search for skills using taxonomy dictionary
    for term, canonical_name in SKILL_TAXONOMY.items():
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, lower_text):
            found_skills.add(canonical_name)
            
    # 2. Check comma/bullet/newline-separated direct tokens
    tokens = re.split(r'[,;\n•|/\t]+', text)
    for token in tokens:
        cleaned = token.strip()
        cleaned_lower = cleaned.lower()
        if cleaned_lower in SKILL_TAXONOMY:
            found_skills.add(SKILL_TAXONOMY[cleaned_lower])
        elif len(cleaned) >= 2 and cleaned_lower in {s.lower() for s in SKILL_TAXONOMY.values()}:
            for canon in SKILL_TAXONOMY.values():
                if canon.lower() == cleaned_lower:
                    found_skills.add(canon)
            
    # 3. Capture custom capitalized acronyms / technologies in text
    custom_matches = re.findall(r'\b[A-Z][a-zA-Z0-9\+#]{1,15}\b', text)
    known_tech = {"SQL", "AWS", "GCP", "BERT", "API", "REST", "JSON", "SMOTE", "NLP", "CUDA", "CI/CD", "MLOps", "LLM", "RAG"}
    for m in custom_matches:
        if m in known_tech:
            found_skills.add(m)
            
    return sorted(list(found_skills))

def evaluate_resume_quality(text: str, extracted_skills: list) -> dict:
    """
    Evaluates ATS quality score (0-100) based on key criteria:
    - Contact Info completeness (Email, Phone, LinkedIn/GitHub)
    - Action verbs density
    - Quantitative impact metrics (percentages, numbers, savings)
    - Skill section depth
    - Education section presence
    """
    score = 0
    feedback = []
    checks = {}
    
    # 1. Contact Information (Max 15 pts)
    email_found = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
    phone_found = bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
    github_linkedin = bool(re.search(r'(github|linkedin)\.com', text.lower()))
    
    contact_pts = 0
    if email_found: contact_pts += 5
    if phone_found: contact_pts += 5
    if github_linkedin: contact_pts += 5
    score += contact_pts
    checks["Contact Information"] = f"{contact_pts}/15 pts"
    if contact_pts < 15:
        feedback.append("⚠️ Add full contact details including LinkedIn & GitHub profile links.")

    # 2. Key Sections Presence (Max 20 pts)
    lower = text.lower()
    has_edu = "education" in lower
    has_exp = "experience" in lower or "internship" in lower or "projects" in lower
    has_skills = "skills" in lower
    has_proj = "projects" in lower or "portfolio" in lower
    
    sec_pts = 0
    if has_edu: sec_pts += 5
    if has_exp: sec_pts += 5
    if has_skills: sec_pts += 5
    if has_proj: sec_pts += 5
    score += sec_pts
    checks["Core Resume Sections"] = f"{sec_pts}/20 pts"

    # 3. Action Verbs & Impact (Max 25 pts)
    action_verb_count = sum(1 for verb in ACTION_VERBS if re.search(r'\b' + verb + r'\b', lower))
    action_pts = min(15, action_verb_count * 3)
    
    # Numbers/Metrics check (% or numbers like 91.5%, 50k, 6 hours)
    metrics_count = len(re.findall(r'(\d+%\b|\d+k\b|\d+\+\b|\$\d+)', lower))
    metrics_pts = min(10, metrics_count * 2.5)
    
    score += (action_pts + int(metrics_pts))
    checks["Action Verbs & Impact"] = f"{action_pts + int(metrics_pts)}/25 pts"
    if metrics_count < 3:
        feedback.append("💡 Add quantifiable metrics (e.g., 'Improved accuracy by 15%', 'Processed 50k records').")

    # 4. Skill Diversity (Max 25 pts)
    skill_count = len(extracted_skills)
    skill_pts = min(25, skill_count * 2)
    score += skill_pts
    checks["Skill Keyword Density"] = f"{skill_pts}/25 pts ({skill_count} skills detected)"
    if skill_count < 8:
        feedback.append("⚠️ Increase skill variety by listing specific tools, libraries, and frameworks.")

    # 5. Length & Formatting (Max 15 pts)
    word_count = len(text.split())
    if 250 <= word_count <= 800:
        length_pts = 15
    elif word_count > 800:
        length_pts = 10
        feedback.append("ℹ️ Resume is slightly lengthy. Aim for 1 concise page (300-600 words) for student entry-level.")
    else:
        length_pts = 8
        feedback.append("⚠️ Resume text is brief. Elaborate on your project implementations and technical tools.")
    score += length_pts
    checks["Length & Formatting"] = f"{length_pts}/15 pts ({word_count} words)"

    final_score = min(100, max(0, score))
    
    return {
        "score": final_score,
        "checks": checks,
        "feedback": feedback,
        "extracted_skills": extracted_skills,
        "word_count": word_count
    }
