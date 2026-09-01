"""
Interview Service
Multi-mode interview lab (Technical, HR, Behavioral, Company-Specific, Pressure) with STAR-method communication analysis.
"""
from modules.advanced_interview_sim import get_questions_by_mode, evaluate_communication_intelligence
from modules.interview_coach import evaluate_student_answer

class InterviewService:
    MODES = [
        "HR / Cultural Fit",
        "Technical Deep-Dive",
        "Company-Specific",
        "Pressure Interview (Adaptive)"
    ]

    @staticmethod
    def get_questions(mode: str, company: str, role: str) -> list:
        """Retrieves questions by mode and target profile."""
        return get_questions_by_mode(mode, company, role)

    @staticmethod
    def evaluate_answer(question_item: dict, student_answer: str) -> dict:
        """Evaluates answer quality, STAR structure, timing, and action-orientation."""
        content_eval = evaluate_student_answer(question_item, student_answer)
        comm_eval = evaluate_communication_intelligence(student_answer)
        
        return {
            "content_score": content_eval["score"],
            "feedback": content_eval["feedback"],
            "strong_points": content_eval["strong_points"],
            "missing_points": content_eval["missing_points"],
            "comm_score": comm_eval["comm_score"],
            "word_count": comm_eval["word_count"],
            "time_feedback": comm_eval["time_feedback"],
            "star_checklist": comm_eval["star_checklist"]
        }
