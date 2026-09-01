"""
AI Career Navigator - Global Configuration & Taxonomy Engine
Defines career tracks, skill taxonomies, theme tokens, and application constants.
"""

APP_NAME = "AI Career Navigator"
APP_TAGLINE = "Your AI-powered roadmap from skills to career"
APP_VERSION = "2.0.0"

# 14+ Industry Career Tracks Taxonomy
CAREER_TRACKS = {
    "Data Analyst": {
        "category": "Data & Analytics",
        "title": "Data Analyst",
        "icon": "📊",
        "description": "Transforms raw business data into actionable insights through SQL queries, statistical analysis, and interactive executive dashboards.",
        "difficulty": "Moderate",
        "avg_salary": "$75,000 - $110,000",
        "demand_growth": "+23% (High)",
        "core_skills": ["SQL", "Python", "Excel", "Power BI", "Tableau", "Statistics", "Exploratory Data Analysis", "Communication"],
        "recommended_education": "Bachelor's in STEM, Business Analytics, or equivalent experience",
        "interview_focus": "SQL JOINs, Window Functions, Dashboard Case Studies, Business Metrics Interpretation"
    },
    "Data Scientist": {
        "category": "Data & Analytics",
        "title": "Data Scientist",
        "icon": "🔬",
        "description": "Builds predictive models, statistical frameworks, and machine learning algorithms to solve complex business problems.",
        "difficulty": "High",
        "avg_salary": "$115,000 - $165,000",
        "demand_growth": "+35% (Very High)",
        "core_skills": ["Python", "SQL", "Machine Learning", "Scikit-learn", "Statistics", "Hypothesis Testing", "Pandas", "PyTorch", "FastAPI"],
        "recommended_education": "Master's or Bachelor's in Data Science, Computer Science, Statistics, or Math",
        "interview_focus": "ML Algorithms, Overfitting/Regularization, Feature Engineering, A/B Testing, Coding"
    },
    "Machine Learning Engineer": {
        "category": "Artificial Intelligence",
        "title": "Machine Learning Engineer",
        "icon": "🤖",
        "description": "Designs, trains, containerizes, and deploys high-throughput machine learning models and MLOps pipelines in cloud production environments.",
        "difficulty": "Very High",
        "avg_salary": "$130,000 - $185,000",
        "demand_growth": "+40% (Extreme)",
        "core_skills": ["Python", "PyTorch", "Machine Learning", "MLOps", "Docker", "FastAPI", "SQL", "Kubernetes", "CI/CD"],
        "recommended_education": "Bachelor's/Master's in Computer Science or AI with strong engineering background",
        "interview_focus": "Model Serving Architecture, Distributed Training, Low-Latency Inference, Systems Design"
    },
    "AI / LLM Engineer": {
        "category": "Artificial Intelligence",
        "title": "AI / LLM Engineer",
        "icon": "🧠",
        "description": "Builds Generative AI applications, Retrieval-Augmented Generation (RAG) architectures, fine-tunes LLMs, and creates agentic workflows.",
        "difficulty": "Very High",
        "avg_salary": "$140,000 - $200,000",
        "demand_growth": "+65% (Explosive)",
        "core_skills": ["Python", "LLMs", "PyTorch", "Hugging Face", "LangChain", "FastAPI", "Docker", "Vector Databases"],
        "recommended_education": "Bachelor's/Master's in CS/AI or proven Open Source AI portfolio",
        "interview_focus": "RAG Architecture, Vector Indexing, Prompt Optimization, Context Window Tradeoffs"
    },
    "Software Engineer (Full-Stack)": {
        "category": "Software Engineering",
        "title": "Software Engineer (Full-Stack)",
        "icon": "💻",
        "description": "Architects and develops end-to-end web applications, responsive user interfaces, and robust backend microservices.",
        "difficulty": "Moderate to High",
        "avg_salary": "$95,000 - $145,000",
        "demand_growth": "+18% (Steady High)",
        "core_skills": ["JavaScript", "TypeScript", "React", "Node.js", "Python", "SQL", "Git", "REST APIs", "Docker"],
        "recommended_education": "Bachelor's in Computer Science, Software Engineering, or Web Dev Bootcamp",
        "interview_focus": "Data Structures & Algorithms, System Design, RESTful Architecture, State Management"
    },
    "Data Engineer": {
        "category": "Data & Analytics",
        "title": "Data Engineer",
        "icon": "⚙️",
        "description": "Constructs reliable, scalable data pipelines, data warehouses, and streaming infrastructure to ingest and organize big data.",
        "difficulty": "High",
        "avg_salary": "$110,000 - $160,000",
        "demand_growth": "+28% (High)",
        "core_skills": ["Python", "SQL", "Apache Spark", "PySpark", "PostgreSQL", "Snowflake", "Docker", "Apache Airflow", "Kafka"],
        "recommended_education": "Bachelor's in Computer Science, Information Systems, or Data Engineering",
        "interview_focus": "ETL/ELT Pipeline Design, Partitioning, SQL Query Optimization, Distributed Computing"
    },
    "Cloud Solutions Architect": {
        "category": "Cloud & Infrastructure",
        "title": "Cloud Solutions Architect",
        "icon": "☁️",
        "description": "Designs scalable, cost-effective, and resilient cloud infrastructures across AWS, Azure, or Google Cloud Platform.",
        "difficulty": "High",
        "avg_salary": "$135,000 - $190,000",
        "demand_growth": "+25% (High)",
        "core_skills": ["AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform", "Linux", "CI/CD", "Networking"],
        "recommended_education": "Bachelor's in CS/IT with AWS/GCP/Azure Professional Certifications",
        "interview_focus": "Cloud Cost Optimization, High Availability (HA), Disaster Recovery, Microservice Architecture"
    },
    "Cybersecurity Analyst": {
        "category": "Security",
        "title": "Cybersecurity Analyst",
        "icon": "🛡️",
        "description": "Protects organizational networks, systems, and data assets from security breaches, intrusions, and cyber threats.",
        "difficulty": "High",
        "avg_salary": "$90,000 - $140,000",
        "demand_growth": "+32% (Very High)",
        "core_skills": ["Linux", "Networking", "Python", "SIEM", "Vulnerability Assessment", "Firewalls", "Bash", "Incident Response"],
        "recommended_education": "Bachelor's in Cybersecurity, Computer Science, or Security+ / CISSP Certification",
        "interview_focus": "Threat Hunting, OWASP Top 10, Network Packet Analysis, Incident Remediation"
    },
    "DevOps & SRE Engineer": {
        "category": "Cloud & Infrastructure",
        "title": "DevOps & SRE Engineer",
        "icon": "🔄",
        "description": "Automates continuous integration and deployment pipelines while maximizing system uptime, reliability, and observability.",
        "difficulty": "High",
        "avg_salary": "$120,000 - $170,000",
        "demand_growth": "+24% (High)",
        "core_skills": ["Docker", "Kubernetes", "CI/CD", "Git", "Linux", "Terraform", "AWS", "Bash", "Prometheus"],
        "recommended_education": "Bachelor's in CS/IT or strong Systems/DevOps background",
        "interview_focus": "Infrastructure as Code, Zero-Downtime Deployments, Observability, SLA/SLO Management"
    },
    "Product Manager (Tech)": {
        "category": "Product & Strategy",
        "title": "Product Manager (Tech)",
        "icon": "🚀",
        "description": "Defines product vision, strategy, feature roadmaps, and coordinates engineering, design, and business teams to launch impactful software.",
        "difficulty": "Moderate to High",
        "avg_salary": "$110,000 - $165,000",
        "demand_growth": "+15% (Steady)",
        "core_skills": ["Agile", "User Research", "Data Analytics", "Roadmap Planning", "Wireframing", "A/B Testing", "Communication", "Leadership"],
        "recommended_education": "Bachelor's/MBA in Business, Engineering, or Product Management",
        "interview_focus": "Product Sense, Prioritization Frameworks (RICE), Metric Definitions, User Empathy"
    },
    "UI/UX Designer": {
        "category": "Design & Frontend",
        "title": "UI/UX Designer",
        "icon": "🎨",
        "description": "Researches user needs and crafts intuitive, accessible, and visually stunning digital product interfaces and interactive prototypes.",
        "difficulty": "Moderate",
        "avg_salary": "$80,000 - $125,000",
        "demand_growth": "+16% (Moderate to High)",
        "core_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Design Systems", "Usability Testing", "HTML/CSS"],
        "recommended_education": "Degree in Human-Computer Interaction, Design, or strong portfolio",
        "interview_focus": "Portfolio Walkthrough, User Flow Critique, Design System Scalability, Accessibility"
    },
    "Business Intelligence Engineer": {
        "category": "Data & Analytics",
        "title": "Business Intelligence Engineer",
        "icon": "📈",
        "description": "Bridges business metrics and technical data warehouses to develop interactive reporting architectures and automated KPI monitors.",
        "difficulty": "Moderate",
        "avg_salary": "$85,000 - $130,000",
        "demand_growth": "+20% (High)",
        "core_skills": ["SQL", "Power BI", "Tableau", "Excel", "Data Modeling", "ETL", "Statistics", "Executive Dashboards"],
        "recommended_education": "Bachelor's in Information Systems, Business Analytics, or STEM",
        "interview_focus": "Dimensional Modeling (Star/Snowflake), DAX / Calculated Measures, Stakeholder Communication"
    },
    "Financial Quantitative Analyst": {
        "category": "Finance & Quantitative",
        "title": "Financial Quantitative Analyst",
        "icon": "💹",
        "description": "Applies mathematical, statistical, and algorithmic techniques to financial market data, risk modeling, and algorithmic trading.",
        "difficulty": "Very High",
        "avg_salary": "$125,000 - $195,000",
        "demand_growth": "+18% (High)",
        "core_skills": ["Python", "R", "Statistics", "Time Series Forecasting", "Linear Algebra", "SQL", "Machine Learning", "Financial Modeling"],
        "recommended_education": "Master's or PhD in Financial Engineering, Quantitative Finance, Physics, or Math",
        "interview_focus": "Stochastic Calculus, Probability Brainteasers, Portfolio Optimization, Time Series Models"
    },
    "Healthcare Technology Specialist": {
        "category": "Healthcare & Biotech",
        "title": "Healthcare Technology Specialist",
        "icon": "🏥",
        "description": "Applies data analytics, EHR systems, and secure biomedical pipelines to improve clinical workflows, patient outcomes, and medical AI.",
        "difficulty": "Moderate to High",
        "avg_salary": "$85,000 - $135,000",
        "demand_growth": "+22% (High)",
        "core_skills": ["SQL", "Python", "Health Data Standards (HL7/FHIR)", "Data Security & Compliance", "Statistics", "Tableau", "Power BI"],
        "recommended_education": "Bachelor's in Health Informatics, Biomedical Engineering, or CS",
        "interview_focus": "Health Data Interoperability, HIPAA Compliance, Clinical Metric Analysis"
    }
}

# 10-Step Career Journey
PRODUCT_JOURNEY = [
    {"step": 1, "name": "Discover", "icon": "🔍", "desc": "Explore 14+ high-growth tech tracks & find your best fit."},
    {"step": 2, "name": "Analyze", "icon": "📄", "desc": "ATS resume evaluation & transparent 7-factor job readiness audit."},
    {"step": 3, "name": "Plan", "icon": "🗺️", "desc": "Dynamic 8-stage step-by-step roadmap tailored to your timeline."},
    {"step": 4, "name": "Learn", "icon": "📚", "desc": "Curated beginner-to-advanced learning hub with verified quizzes."},
    {"step": 5, "name": "Build", "icon": "💡", "desc": "Flagship project blueprints and 7D portfolio strength auditor."},
    {"step": 6, "name": "Prepare", "icon": "🎤", "desc": "Interactive mock interview simulator with STAR method intelligence."},
    {"step": 7, "name": "Apply", "icon": "💼", "desc": "Kanban & list-view job application pipeline tracker."},
    {"step": 8, "name": "Track", "icon": "📈", "desc": "Daily missions, milestone achievements, and progress analytics."},
    {"step": 9, "name": "Grow", "icon": "🌐", "desc": "Shareable public portfolio profile with custom verification badges."}
]

# FAQ Items for Landing Page
LANDING_FAQ = [
    {
        "q": "How is AI Career Navigator different from generic resume checkers?",
        "a": "Unlike superficial keyword checkers, AI Career Navigator uses a deterministic 7-factor Career Twin engine. It audits not just your resume formatting, but also your prerequisite skill dependency tree, portfolio project depth, verified quiz performance, and STAR-method interview readiness."
    },
    {
        "q": "Are the career readiness scores scientifically guaranteed?",
        "a": "Our readiness scores are transparent benchmarks calibrated against real tech industry requirements. They serve as an actionable guide showing you exactly what skills, projects, and interview practice will elevate your candidate profile, rather than an unverified promise of employment."
    },
    {
        "q": "Can I switch target career tracks later?",
        "a": "Yes! You can explore and switch between 14+ career tracks at any time. The dynamic roadmap, skill gap engine, and interview simulator will immediately recalibrate to your newly selected target role."
    },
    {
        "q": "Is my resume and personal data secure?",
        "a": "Absolutely. All user workspaces and profile data are isolated with user-level authentication. We never sell, share, or expose your resume or contact details."
    }
]
