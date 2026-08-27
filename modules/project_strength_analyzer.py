"""
Project Strength Auditor & "Build Me a Better Project" Generator Module
Evaluates student portfolio projects across 7 criteria and generates end-to-end project build blueprints.
"""

def audit_project_strength(project_name: str, tech_stack: str, description: str, has_deployment: bool, has_readme: bool) -> dict:
    """
    Audits a candidate project across 7 dimensions out of 100 points:
    1. Problem Relevance
    2. Technical Depth
    3. Implementation Rigor
    4. Deployment Evidence
    5. Business Value
    6. Documentation Quality
    7. GitHub Quality
    """
    desc_lower = description.lower()
    tech_lower = tech_stack.lower()
    
    # 1. Problem Relevance (Base 70 + bonus)
    prob_score = 75 + (10 if any(kw in desc_lower for kw in ["churn", "revenue", "sales", "fraud", "customer", "rag", "pipeline"]) else 0)
    
    # 2. Technical Depth
    tech_count = len(tech_stack.split(","))
    tech_depth = min(95, 60 + tech_count * 7)
    
    # 3. Implementation
    impl_score = 80 if any(kw in tech_lower for kw in ["pytorch", "xgboost", "scikit-learn", "fastapi", "spark", "postgres"]) else 70
    
    # 4. Deployment Evidence
    deploy_score = 90 if has_deployment else 40
    
    # 5. Business Value
    biz_score = 85 if any(kw in desc_lower for kw in ["%", "saved", "reduced", "increased", "k", "boosted"]) else 65
    
    # 6. Documentation
    doc_score = 85 if has_readme else 50
    
    # 7. GitHub Quality
    github_score = 80 if (has_deployment and has_readme) else 60

    overall_score = round(
        (prob_score * 0.15 + tech_depth * 0.20 + impl_score * 0.20 + 
         deploy_score * 0.20 + biz_score * 0.10 + doc_score * 0.08 + github_score * 0.07), 1
    )

    recommendations = []
    if not has_deployment:
        recommendations.append("🔴 Deploy application to Streamlit Cloud, Hugging Face Spaces, or Render (+20 deployment pts).")
    if not has_readme:
        recommendations.append("🔴 Add professional README.md with architecture diagram and installation steps (+15 doc pts).")
    if biz_score < 75:
        recommendations.append("🟡 Quantify business impact in description (e.g. 'Improved accuracy by 15%', 'Saved 6 hours weekly').")

    return {
        "project_name": project_name,
        "overall_score": overall_score,
        "criteria": {
            "Problem Relevance": prob_score,
            "Technical Depth": tech_depth,
            "Implementation Rigor": impl_score,
            "Deployment Evidence": deploy_score,
            "Business Value": biz_score,
            "Documentation Quality": doc_score,
            "GitHub Quality": github_score
        },
        "recommendations": recommendations
    }

def generate_flagship_project_blueprint(known_skills: list, target_role: str = "Data Analyst") -> dict:
    """
    Generates a complete 'Build Me a Better Project' flagship portfolio blueprint customized to candidate skills.
    Includes Dataset, Architecture, Step-by-Step Tasks, GitHub Directory Structure, README Template, and Deployment Plan.
    """
    skills_str = ", ".join(known_skills) if known_skills else "Python, SQL, Power BI"
    
    if "Analyst" in target_role:
        title = "Enterprise E-Commerce Sales & Customer Intelligence Platform"
        difficulty = "Intermediate"
        tech_specs = ["PostgreSQL", "Python", "Pandas", "Power BI / Tableau", "Plotly", "Streamlit"]
        dataset_name = "Kaggle Brazilian E-Commerce Public Dataset (Olist) / Synthesized Transactions"
        dataset_link = "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"
        desc = "Architect a multi-channel transactional database, execute complex SQL window function queries for Cohort Analysis & Customer Lifetime Value (LTV), and deploy interactive Power BI / Streamlit dashboards."
        tasks = [
            "Design normalized PostgreSQL schema (Customers, Orders, OrderItems, Products, Payments)",
            "Populate mock transactional dataset with 100,000+ records",
            "Write analytical SQL queries using ROW_NUMBER(), DENSE_RANK(), LAG/LEAD for MoM retention",
            "Build interactive Power BI / Streamlit executive dashboard with dynamic slicers",
            "Deploy dashboard app and commit code to GitHub with detailed documentation"
        ]
        readme_snippet = """# 🛍️ Enterprise E-Commerce Sales & Customer LTV Analytics
## 📊 Architecture
`PostgreSQL Database -> Python Pandas Data Pipeline -> Power BI / Streamlit Executive Dashboard`
## 🔑 Key SQL Queries Implemented
- **LTV Cohort Analysis** via `DENSE_RANK()` and `LAG()`
- **RFM Segmentation (Recency, Frequency, Monetary)** using NTILE(4)
"""

    elif "Engineer" in target_role and "Machine" in target_role:
        title = "Production MLOps Pipeline & Model Serving Engine"
        difficulty = "Advanced"
        tech_specs = ["Python", "PyTorch / XGBoost", "FastAPI", "Docker", "MLflow", "GitHub Actions"]
        dataset_name = "Kaggle Credit Card Fraud Detection / Customer Churn Dataset"
        dataset_link = "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud"
        desc = "Train an end-to-end model with MLflow experiment tracking, package in FastAPI REST API microservice, containerize with Docker, and setup CI/CD workflow."
        tasks = [
            "Data extraction & SMOTE imbalance handling in Pandas",
            "Model training with Optuna hyperparameter tuning and MLflow logging",
            "FastAPI REST API server creation with Pydantic data validation",
            "Docker container build and Streamlit visual interface integration",
            "GitHub Actions CI/CD setup for automated testing & deployment"
        ]
        readme_snippet = """# 🚀 Production MLOps Model Pipeline & Docker API
## 🛠️ Tech Stack
`PyTorch + MLflow + FastAPI + Docker + Streamlit`
## ⚡ Quick Start
`docker build -t ml-engine . && docker run -p 8000:8000 ml-engine`
"""

    else:
        title = "AI Customer Intelligence & Churn Prediction System"
        difficulty = "Intermediate-Advanced"
        tech_specs = ["Python", "Scikit-learn", "XGBoost", "FastAPI", "Streamlit", "Docker"]
        dataset_name = "Telco Customer Churn Dataset"
        dataset_link = "https://www.kaggle.com/datasets/blastchar/telco-customer-churn"
        desc = "End-to-end predictive machine learning web application predicting customer churn risk, explaining feature importance via SHAP, and serving predictions through Streamlit."
        tasks = [
            "Perform Exploratory Data Analysis & feature correlation in Pandas & Seaborn",
            "Train Logistic Regression, Random Forest, and XGBoost models; evaluate ROC-AUC",
            "Build Streamlit web interface with interactive risk assessment sliders",
            "Containerize application using Docker and deploy to Streamlit Cloud / Render"
        ]
        readme_snippet = """# 🎯 AI Customer Churn Risk Prediction Engine
## 📈 Model Performance
- XGBoost Classifier ROC-AUC: **89.4%**
- Latency per prediction: **< 15ms**
"""

    return {
        "title": title,
        "difficulty": difficulty,
        "target_role": target_role,
        "skills_demonstrated": len(tech_specs),
        "estimated_time": "2 - 3 Weeks",
        "tech_specs": tech_specs,
        "dataset_name": dataset_name,
        "dataset_link": dataset_link,
        "description": desc,
        "tasks": tasks,
        "github_structure": """
project_repo/
├── app.py                  # Main Streamlit web application
├── Dockerfile              # Containerization configuration
├── requirements.txt        # Python dependencies
├── README.md               # Architecture documentation & Loom video link
├── data/
│   └── raw_dataset.csv     # Data source files
├── models/
│   └── trained_model.pkl   # Serialized model artifact
└── notebooks/
    └── eda_modeling.ipynb  # Exploratory Data Analysis notebook
""",
        "readme_snippet": readme_snippet
    }
