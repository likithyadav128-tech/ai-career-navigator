"""
Sample Data for AI Career Navigator & Skill Gap Platform
Provides pre-loaded resumes and target job descriptions for instant testing.
"""

SAMPLE_RESUMES = {
    "Data Science Student (Alex Rivera)": {
        "text": """
Alex Rivera
Email: alex.rivera@university.edu | Phone: (555) 019-2834 | GitHub: github.com/arivera | LinkedIn: linkedin.com/in/alex-rivera-ds

OBJECTIVE
Motivated Computer Science & Data Science senior seeking an entry-level Data Scientist or Machine Learning Engineer role.

EDUCATION
Bachelor of Science in Data Science & Computer Science
State University, Expected Graduation: May 2025 | GPA: 3.85/4.0
Relevant Coursework: Machine Learning, Data Structures & Algorithms, Applied Statistics, Database Management Systems, Deep Learning, Natural Language Processing.

SKILLS
- Programming: Python, SQL, C++, R, Bash
- ML/DL Frameworks: PyTorch, Scikit-learn, TensorFlow, XGBoost, Pandas, NumPy
- Data Analysis & Viz: Matplotlib, Seaborn, Plotly, Tableau, SQL (PostgreSQL, MySQL)
- Tools & Cloud: Git, Docker, Jupyter, VS Code, Linux
- Soft Skills: Problem Solving, Team Collaboration, Technical Writing, Agile

PROJECTS
1. Customer Churn Prediction Engine | Python, Scikit-learn, Pandas, XGBoost
   - Engineered features from 50k+ user transaction logs, handling missing values and class imbalance using SMOTE.
   - Built XGBoost and Random Forest classifiers achieving 89.2% ROC-AUC score.
   - Deployed model interactive dashboard using Streamlit to display high-risk churn indicators.

2. Sentiment Analysis on Product Reviews | Python, NLP, PyTorch, Hugging Face
   - Fine-tuned BERT model on 10,000 Amazon product reviews for 3-class sentiment classification.
   - Achieved 91.5% accuracy, surpassing baseline TF-IDF + Logistic Regression by 14%.

3. Automated SQL Query Optimizer & EDA Tool | Python, PostgreSQL, Streamlit
   - Developed dynamic exploratory data analysis tool auto-generating summary statistics and Plotly charts.

EXPERIENCE
Data Science Intern | Tech Analytics Corp | June 2024 - August 2024
- Assisted in cleaning and pipeline processing of 1M+ daily telemetry records using Pandas and SQL.
- Automated weekly reporting script saving 6 hours of manual spreadsheet processing every week.
- Collaborated with senior data engineers to optimize PostgreSQL queries, reducing execution time by 30%.

CERTIFICATIONS & ACHIEVEMENTS
- DeepLearning.AI Machine Learning Specialization (Coursera)
- AWS Certified Cloud Practitioner (2024)
- 1st Place - State University Hackathon 2024 (Built Real-Time Traffic Anomaly Detector)
""",
        "extracted_skills": [
            "Python", "SQL", "C++", "R", "Bash", "PyTorch", "Scikit-learn", "TensorFlow",
            "XGBoost", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Tableau",
            "PostgreSQL", "MySQL", "Git", "Docker", "Jupyter", "Linux", "Streamlit",
            "Machine Learning", "Deep Learning", "Natural Language Processing", "BERT",
            "Feature Engineering", "Exploratory Data Analysis", "Model Evaluation"
        ]
    },
    "Software & Web Developer (Sam Chen)": {
        "text": """
Sam Chen
Email: sam.chen@dev.io | Portfolio: samchen.dev | GitHub: github.com/samchen-dev

SUMMARY
Passionate Full-Stack Developer with strong foundation in JavaScript/TypeScript, React, Python, and FastAPI.

EDUCATION
BS in Computer Science | Tech University (2021-2025)

SKILLS
- Languages: JavaScript, TypeScript, Python, HTML5, CSS3, SQL
- Frontend: React, Next.js, Redux, Tailwind CSS, HTML/CSS
- Backend: Node.js, Express, Python, FastAPI, REST APIs
- Databases: MongoDB, PostgreSQL, SQLite
- DevOps & Tools: Git, Docker, Postman, Vercel, Render

PROJECTS
- E-Commerce Web App (React, FastAPI, PostgreSQL, Stripe Integration)
- Real-Time Chat App (TypeScript, Node.js, Socket.io, Tailwind CSS)
""",
        "extracted_skills": [
            "JavaScript", "TypeScript", "Python", "HTML5", "CSS3", "SQL", "React",
            "Next.js", "Redux", "Tailwind CSS", "Node.js", "Express", "FastAPI",
            "REST APIs", "MongoDB", "PostgreSQL", "SQLite", "Git", "Docker", "Postman"
        ]
    }
}

SAMPLE_JOB_DESCRIPTIONS = {
    "Data Scientist": {
        "title": "Data Scientist - AI & Analytics",
        "company": "NexusAI Solutions",
        "text": """
Role: Data Scientist
Company: NexusAI Solutions
Location: Remote / Hybrid

About the Role:
We are looking for a Data Scientist to join our advanced analytics team. You will build machine learning models, analyze complex datasets, perform statistical modeling, design A/B tests, and deploy predictive models to production.

Key Responsibilities:
- Extract, clean, and transform large structured and unstructured datasets using SQL and PySpark/Pandas.
- Develop predictive machine learning models (Classification, Regression, Clustering, Time Series forecasting) using Scikit-Learn, XGBoost, and PyTorch.
- Build interactive data dashboards and visualization reports using Plotly, Tableau, or Streamlit.
- Design and evaluate A/B testing experiments and hypothesis testing.
- Deploy ML models as REST APIs using FastAPI or Flask, containerized with Docker and monitored in cloud environments (AWS/GCP).
- Collaborate with product managers and software engineering teams to translate business requirements into ML solutions.

Requirements & Skills Needed:
- Technical Skills: Python, SQL, Advanced Statistics, Hypothesis Testing, Scikit-learn, PyTorch, Pandas, NumPy, XGBoost, PySpark, Docker, FastAPI, AWS/GCP, MLOps, A/B Testing, Plotly, Tableau.
- Soft Skills: Problem Solving, Business Communication, Critical Thinking, Cross-functional Collaboration.
- Education: Bachelor's or Master's degree in Data Science, Computer Science, Statistics, or quantitative field.
- Experience: 0-2 years (Entry to Junior level).
""",
        "required_skills": [
            "Python", "SQL", "Advanced Statistics", "Hypothesis Testing", "Scikit-learn",
            "PyTorch", "Pandas", "NumPy", "XGBoost", "PySpark", "Docker", "FastAPI",
            "AWS/GCP", "MLOps", "A/B Testing", "Plotly", "Tableau", "Problem Solving",
            "Business Communication", "Critical Thinking"
        ],
        "tech_skills": [
            "Python", "SQL", "Advanced Statistics", "Hypothesis Testing", "Scikit-learn",
            "PyTorch", "Pandas", "NumPy", "XGBoost", "PySpark", "Docker", "FastAPI",
            "AWS/GCP", "MLOps", "A/B Testing", "Plotly", "Tableau"
        ],
        "soft_skills": ["Problem Solving", "Business Communication", "Critical Thinking"]
    },
    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "company": "DeepTech Innovations",
        "text": """
Role: Machine Learning Engineer
Company: DeepTech Innovations

We are seeking a Machine Learning Engineer responsible for scaling ML models, building MLOps pipelines, containerization, model monitoring, PyTorch/TensorFlow deep learning model optimization, and REST API deployment with FastAPI & Kubernetes.

Required Skills:
Python, PyTorch, TensorFlow, MLOps, MLflow, Docker, Kubernetes, FastAPI, CI/CD, SQL, CUDA, Model Quantification, Git, Cloud (AWS/GCP).
""",
        "required_skills": [
            "Python", "PyTorch", "TensorFlow", "MLOps", "MLflow", "Docker",
            "Kubernetes", "FastAPI", "CI/CD", "SQL", "CUDA", "Model Quantification",
            "Git", "AWS/GCP"
        ],
        "tech_skills": [
            "Python", "PyTorch", "TensorFlow", "MLOps", "MLflow", "Docker",
            "Kubernetes", "FastAPI", "CI/CD", "SQL", "CUDA", "Model Quantification",
            "Git", "AWS/GCP"
        ],
        "soft_skills": ["Engineering Rigor", "System Architecture Thinking"]
    },
    "Data Analyst": {
        "title": "Junior Data Analyst",
        "company": "Global Analytics Corp",
        "text": """
Role: Junior Data Analyst
Company: Global Analytics Corp

Responsibilities:
Query databases with SQL, create dashboards in Power BI & Tableau, clean datasets with Excel & Python (Pandas), present insights to business stakeholders.

Required Skills:
SQL, PostgreSQL, Excel, Power BI, Tableau, Python, Pandas, Matplotlib, Data Storytelling, Communication, Statistics.
""",
        "required_skills": [
            "SQL", "PostgreSQL", "Excel", "Power BI", "Tableau", "Python",
            "Pandas", "Matplotlib", "Data Storytelling", "Communication", "Statistics"
        ],
        "tech_skills": [
            "SQL", "PostgreSQL", "Excel", "Power BI", "Tableau", "Python",
            "Pandas", "Matplotlib", "Statistics"
        ],
        "soft_skills": ["Data Storytelling", "Communication"]
    }
}
