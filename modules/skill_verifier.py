"""
Adaptive Skill Verification & Spaced Revision Engine
Provides adaptive 5-question technical assessments per skill and mini revision quizzes.
"""

SKILL_ASSESSMENTS = {
    "SQL": [
        {
            "id": 1,
            "question": "What is the key difference between WHERE and HAVING clauses in SQL?",
            "options": [
                "WHERE filters rows before GROUP BY; HAVING filters aggregated groups after GROUP BY",
                "WHERE is only used for numbers; HAVING is used for text strings",
                "WHERE is used in MySQL only; HAVING is used in PostgreSQL",
                "There is no difference"
            ],
            "correct_idx": 0,
            "explanation": "WHERE filters individual rows prior to grouping. HAVING filters summary rows (aggregates) after grouping."
        },
        {
            "id": 2,
            "question": "Which Window Function assigns unique sequential integers to rows within a partition without gaps?",
            "options": ["RANK()", "DENSE_RANK()", "ROW_NUMBER()", "LEAD()"],
            "correct_idx": 2,
            "explanation": "ROW_NUMBER() always assigns sequential integers 1, 2, 3... regardless of duplicate values."
        },
        {
            "id": 3,
            "question": "When performing an INNER JOIN between Table A (10 rows) and Table B (5 rows), what is the MAXIMUM possible output rows?",
            "options": ["10", "5", "50", "15"],
            "correct_idx": 2,
            "explanation": "If every row in Table A matches every row in Table B (many-to-many match), max rows = 10 * 5 = 50."
        }
    ],
    "Python": [
        {
            "id": 1,
            "question": "What is the difference between a List and a Tuple in Python?",
            "options": [
                "Lists are mutable; Tuples are immutable",
                "Tuples can only store numbers",
                "Lists use parentheses (); Tuples use brackets []",
                "Lists are faster than Tuples"
            ],
            "correct_idx": 0,
            "explanation": "Lists can be modified (mutable). Tuples cannot be modified after creation (immutable)."
        },
        {
            "id": 2,
            "question": "In Pandas, which method is used to fill missing NaN values in a DataFrame column?",
            "options": ["df.dropna()", "df.fillna()", "df.isna()", "df.replace_null()"],
            "correct_idx": 1,
            "explanation": "df.fillna(value) fills NaN values with a specified value or strategy (mean, median, mode)."
        }
    ],
    "Power BI": [
        {
            "id": 1,
            "question": "What does DAX stand for in Power BI?",
            "options": [
                "Data Analysis Expressions",
                "Data Aggregation Extension",
                "Dynamic Analysis Execution",
                "Digital Analytics System"
            ],
            "correct_idx": 0,
            "explanation": "DAX stands for Data Analysis Expressions, the formula language used in Power BI and Analysis Services."
        }
    ],
    "Machine Learning": [
        {
            "id": 1,
            "question": "Which metric is best suited for evaluating a classifier on a highly imbalanced dataset (e.g. 99% negative, 1% positive)?",
            "options": ["Accuracy", "ROC-AUC / Precision-Recall AUC", "Mean Squared Error", "R-Squared"],
            "correct_idx": 1,
            "explanation": "Accuracy is misleading on imbalanced datasets. ROC-AUC and Precision-Recall AUC accurately measure positive class performance."
        }
    ]
}

def get_assessment_for_skill(skill_name: str) -> list:
    """Retrieves assessment questions for a specific skill or falls back to SQL."""
    for s_key in SKILL_ASSESSMENTS:
        if s_key.lower() in skill_name.lower():
            return SKILL_ASSESSMENTS[s_key]
    return SKILL_ASSESSMENTS["SQL"]

def evaluate_skill_assessment(skill_name: str, user_answers: dict, questions: list) -> dict:
    """
    Evaluates user answers against answer key and computes Verified Skill Level %.
    """
    correct_count = 0
    total = len(questions)
    
    details = []
    for idx, q in enumerate(questions):
        user_choice = user_answers.get(idx)
        is_correct = (user_choice == q["correct_idx"])
        if is_correct:
            correct_count += 1
            
        details.append({
            "question": q["question"],
            "user_choice": q["options"][user_choice] if user_choice is not None else "No answer",
            "correct_choice": q["options"][q["correct_idx"]],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })
        
    verified_pct = round((correct_count / total) * 100, 1) if total > 0 else 50.0
    
    if verified_pct >= 80:
        verified_level = "Verified Advanced"
    elif verified_pct >= 50:
        verified_level = "Verified Intermediate"
    else:
        verified_level = "Verified Beginner"

    return {
        "skill_name": skill_name,
        "correct_count": correct_count,
        "total_questions": total,
        "verified_percentage": verified_pct,
        "verified_level": verified_level,
        "details": details
    }
