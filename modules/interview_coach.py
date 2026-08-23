"""
AI Interview Coach Engine
Generates role-specific questions (Technical, System Design, Behavioral) and evaluates student responses.
"""

ROLE_QUESTIONS = {
    "Data Scientist": [
        {
            "id": 1,
            "category": "Technical ML",
            "question": "How do you handle severe class imbalance in a classification problem? Explain resampling methods vs algorithm-level tweaks.",
            "ideal_keywords": ["SMOTE", "undersampling", "oversampling", "class_weight", "ROC-AUC", "PR-AUC", "F1-score", "Precision-Recall", "XGBoost"],
            "rubric": "Evaluates candidate understanding of SMOTE, cost-sensitive learning, and choosing appropriate evaluation metrics (ROC-AUC/F1 vs Accuracy)."
        },
        {
            "id": 2,
            "category": "Statistics & A/B Testing",
            "question": "Explain P-value to a non-technical stakeholder. How do you determine sample size required for an A/B test?",
            "ideal_keywords": ["null hypothesis", "statistical significance", "p-value", "alpha", "power", "effect size", "sample size calculation"],
            "rubric": "Tests ability to translate statistical jargon into business language and understanding of statistical power & significance level."
        },
        {
            "id": 3,
            "category": "System Design / MLOps",
            "question": "How would you design a real-time recommendation engine for an e-commerce platform? Walk through data pipelines, embedding retrieval, and model scoring.",
            "ideal_keywords": ["candidate generation", "vector embeddings", "FAISS", "ranking model", "FastAPI", "latency", "caching", "A/B test"],
            "rubric": "Assesses 2-stage architecture (Retrieval + Ranking), latency management, and deployment considerations."
        },
        {
            "id": 4,
            "category": "Behavioral (STAR)",
            "question": "Describe a project where your initial model performed poorly. How did you diagnose the issue and improve model accuracy?",
            "ideal_keywords": ["data quality", "feature engineering", "error analysis", "confusion matrix", "hyperparameter tuning", "cross-validation", "result"],
            "rubric": "Looks for structured STAR method (Situation, Task, Action, Result) with scientific debugging mindset."
        }
    ],
    "Machine Learning Engineer": [
        {
            "id": 1,
            "category": "ML Systems & Deployment",
            "question": "What is the difference between Batch Inference and Real-Time Inference? When would you use Docker and FastAPI over offline batch predictions?",
            "ideal_keywords": ["latency", "throughput", "FastAPI", "REST API", "Docker", "microservice", "stream processing", "caching"],
            "rubric": "Tests system trade-offs between low latency real-time APIs vs high throughput offline batch jobs."
        },
        {
            "id": 2,
            "category": "Optimization & Deep Learning",
            "question": "Explain gradient vanishing and exploding in deep neural networks. What techniques prevent them?",
            "ideal_keywords": ["gradient clipping", "batch normalization", "residual connections", "Xavier/He initialization", "ReLU", "LSTM/Transformer"],
            "rubric": "Assesses deep learning mathematical knowledge and stabilization techniques."
        }
    ],
    "Data Analyst": [
        {
            "id": 1,
            "category": "SQL & Data Extraction",
            "question": "Explain the difference between WHERE and HAVING in SQL. Write a quick mental query finding top 3 customers per region using Window functions.",
            "ideal_keywords": ["GROUP BY", "WHERE filters rows before", "HAVING filters aggregates", "ROW_NUMBER()", "DENSE_RANK()", "PARTITION BY"],
            "rubric": "Checks fundamental SQL execution order and mastery of analytical window functions."
        },
        {
            "id": 2,
            "category": "Business Intelligence & Dashboarding",
            "question": "How do you choose between a bar chart, line chart, scatter plot, and heatmap when communicating data insights to executives?",
            "ideal_keywords": ["categorical comparison", "time series trends", "correlation", "distribution/density", "stakeholder storytelling"],
            "rubric": "Evaluates data visualization taxonomy and executive presentation skills."
        }
    ]
}

def get_questions_for_role(role: str) -> list:
    """Retrieve question list for the target role or default to Data Scientist."""
    for key in ROLE_QUESTIONS:
        if key.lower() in role.lower():
            return ROLE_QUESTIONS[key]
    return ROLE_QUESTIONS["Data Scientist"]

def evaluate_student_answer(question_obj: dict, student_answer: str) -> dict:
    """
    Evaluates student answer using heuristic NLP keyword & completeness checks:
    - Length & depth
    - Presence of key technical concepts/keywords
    - Constructive score out of 10
    - Strengths & actionable improvement suggestions
    """
    answer_lower = student_answer.lower()
    word_count = len(student_answer.split())
    
    if word_count < 10:
        return {
            "score": 2,
            "rating": "Needs Improvement",
            "matched_keywords": [],
            "missing_keywords": question_obj["ideal_keywords"],
            "strengths": ["Answer was submitted."],
            "improvements": ["Answer is too brief. Provide detailed explanations, code examples, and technical trade-offs."]
        }
        
    matched = [kw for kw in question_obj["ideal_keywords"] if kw.lower() in answer_lower]
    missing = [kw for kw in question_obj["ideal_keywords"] if kw.lower() not in answer_lower]
    
    match_ratio = len(matched) / len(question_obj["ideal_keywords"]) if question_obj["ideal_keywords"] else 0.5
    
    # Calculate score out of 10
    base_score = int(match_ratio * 6) + (3 if word_count >= 50 else (2 if word_count >= 25 else 1))
    score = min(10, max(1, base_score))
    
    if score >= 8:
        rating = "Excellent"
    elif score >= 6:
        rating = "Good / Solid"
    else:
        rating = "Needs Refinement"
        
    strengths = []
    if matched:
        strengths.append(f"Great inclusion of core terms: {', '.join(matched[:4])}.")
    if word_count >= 40:
        strengths.append("Detailed and comprehensive explanation length.")
        
    improvements = []
    if missing:
        improvements.append(f"Consider referencing key terms: {', '.join(missing[:4])}.")
    if "example" not in answer_lower and "project" not in answer_lower:
        improvements.append("Tip: Illustrate your answer with a real project example or code implementation detail.")
        
    return {
        "score": score,
        "rating": rating,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "strengths": strengths,
        "improvements": improvements
    }
