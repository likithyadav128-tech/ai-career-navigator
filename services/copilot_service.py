"""
AI Career Copilot Service
Context-aware conversational assistant tailored with user profile, target role, and identified skill gaps.
"""
from modules.career_assistant import generate_assistant_response

class CopilotService:
    QUICK_PROMPTS = [
        "What should I learn next based on my skill tree?",
        "Am I ready for a Data Analyst role right now?",
        "Which high-impact skills should I add to my resume?",
        "Give me an industry-grade portfolio project idea.",
        "How can I prepare for a behavioral STAR interview?",
        "Create a 30-day accelerated learning plan for me."
    ]

    @staticmethod
    def answer_query(query: str, context: dict) -> str:
        """Generates an intelligent context-aware response."""
        return generate_assistant_response(query, context)
