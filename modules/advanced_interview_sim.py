"""
Advanced AI Interview Simulator & Communication Intelligence Engine
Supports 4 modes (HR, Technical, Company-Specific, Pressure) and STAR structure scoring.
"""

COMPANY_SPECIFIC_QUESTIONS = {
    "TCS / Service Majors (Core Fundamentals & Aptitude)": [
        {
            "category": "Company Specific: TCS",
            "question": "Explain the difference between Primary Key and Unique Key in SQL. How do you optimize a slow database query?",
            "ideal_keywords": ["Primary Key", "Unique Key", "NULL values", "INDEX", "Execution Plan", "EXPLAIN", "JOIN"],
            "rubric": "Evaluates fundamental RDBMS concepts and database indexing knowledge."
        },
        {
            "category": "Company Specific: TCS",
            "question": "What is Object-Oriented Programming (OOP)? Explain Inheritance and Polymorphism with a real example.",
            "ideal_keywords": ["Class", "Object", "Inheritance", "Polymorphism", "Encapsulation", "Abstraction", "Method Overriding"],
            "rubric": "Assesses core OOP principles and code organization skills."
        }
    ],
    "Amazon / Tier-1 Product (Coding Rigor & System Architecture)": [
        {
            "category": "Company Specific: Amazon",
            "question": "Describe a time when you took Customer Obsession or Deep Dive into a technical problem. How did you handle ambiguous requirements?",
            "ideal_keywords": ["Customer Obsession", "Deep Dive", "STAR method", "Situation", "Task", "Action", "Result", "Ownership"],
            "rubric": "Evaluates Amazon Leadership Principles and structured STAR communication."
        },
        {
            "category": "Company Specific: Amazon",
            "question": "How would you design a scalable microservice architecture for real-time order processing handling 100,000 requests/sec?",
            "ideal_keywords": ["load balancer", "caching", "Redis", "Kafka", "queue", "database sharding", "microservices", "latency"],
            "rubric": "Tests high-throughput system design and bottleneck resolution."
        }
    ],
    "Google / Big Tech (Algorithmic Excellence & Innovation)": [
        {
            "category": "Company Specific: Google",
            "question": "Explain Time Complexity and Space Complexity of QuickSort vs MergeSort. In what scenario is HeapSort preferred?",
            "ideal_keywords": ["O(N log N)", "O(N^2)", "in-place", "space complexity", "pivot", "recursion", "worst case"],
            "rubric": "Assesses rigorous computer science algorithm analysis."
        }
    ],
    "Deloitte / Consulting (Analytics & Data Storytelling)": [
        {
            "category": "Company Specific: Deloitte",
            "question": "How would you explain a complex machine learning forecast model to a non-technical executive client?",
            "ideal_keywords": ["business impact", "key metrics", "executive summary", "visual dashboard", "ROI", "simplicity", "recommendation"],
            "rubric": "Evaluates data storytelling and stakeholder management."
        }
    ]
}

PRESSURE_MODE_QUESTIONS = [
    {
        "level": "Easy",
        "question": "What is the difference between a list and a dictionary in Python?",
        "ideal_keywords": ["index", "key-value", "mutable", "hash table", "O(1) lookup"]
    },
    {
        "level": "Medium",
        "question": "Your model has 98% accuracy on training data but 55% accuracy on test data. What is happening and how do you fix it?",
        "ideal_keywords": ["overfitting", "high variance", "regularization", "cross-validation", "dropout", "more data", "pruning"]
    },
    {
        "level": "Hard / Pressure",
        "question": "A production API serving predictions suddenly experiences a 500% latency spike. Walk me through your step-by-step emergency diagnostic procedure.",
        "ideal_keywords": ["logs", "CPU/Memory metric", "database connection pool", "latency", "caching", "rollback", "traffic spike", "microservices"]
    }
]

HR_QUESTIONS = [
    {
        "category": "HR & Culture Fit",
        "question": "Tell me about yourself, your technical background, and why you are interested in this target role.",
        "ideal_keywords": ["education", "projects", "passion", "skills", "STAR method", "alignment", "growth"]
    },
    {
        "category": "HR & Culture Fit",
        "question": "Describe a conflict you had with a teammate during a group project. How did you resolve it?",
        "ideal_keywords": ["communication", "listen", "compromise", "resolution", "teamwork", "outcome"]
    }
]

def get_questions_by_mode(mode: str, company: str, role: str) -> list:
    """Returns question list tailored to selected interview mode."""
    if mode == "Company-Specific":
        return COMPANY_SPECIFIC_QUESTIONS.get(company, COMPANY_SPECIFIC_QUESTIONS["TCS / Service Majors (Core Fundamentals & Aptitude)"])
    elif mode == "HR / Cultural Fit":
        return HR_QUESTIONS
    elif mode == "Pressure Interview (Adaptive)":
        return PRESSURE_MODE_QUESTIONS
    else:
        # Technical Deep Dive default
        from modules.interview_coach import ROLE_QUESTIONS
        for key in ROLE_QUESTIONS:
            if key.lower() in role.lower():
                return ROLE_QUESTIONS[key]
        return ROLE_QUESTIONS["Data Scientist"]

def evaluate_communication_intelligence(answer: str) -> dict:
    """
    Evaluates candidate communication quality across:
    - STAR Structure (Situation, Task, Action, Result)
    - Length & Depth
    - Technical Precision
    - Conciseness & Time Efficiency
    """
    ans_lower = answer.lower()
    words = answer.split()
    word_count = len(words)
    
    star_found = {
        "Situation": any(k in ans_lower for k in ["situation", "when", "context", "background", "project", "while"]),
        "Task": any(k in ans_lower for k in ["task", "goal", "needed to", "objective", "challenge", "problem"]),
        "Action": any(k in ans_lower for k in ["action", "built", "engineered", "developed", "implemented", "used", "wrote"]),
        "Result": any(k in ans_lower for k in ["result", "outcome", "improved", "saved", "%", "achieved", "increased", "reduced"])
    }
    
    star_score = sum(25 for k, v in star_found.items() if v)
    
    # Conciseness / Efficiency check (Optimal: 40 - 150 words)
    if 40 <= word_count <= 150:
        time_score = 90
        time_feedback = "Optimal answer length and timing."
    elif word_count > 150:
        time_score = 75
        time_feedback = "Answer is slightly verbose. Aim for crisp STAR structure under 120 words."
    else:
        time_score = 50
        time_feedback = "Answer is too brief. Elaborate on your technical actions and quantitative results."

    overall_comm_score = round(star_score * 0.6 + time_score * 0.4, 1)

    return {
        "comm_score": overall_comm_score,
        "star_checklist": star_found,
        "word_count": word_count,
        "time_feedback": time_feedback
    }
