"""
Resume AI Service
Handles multi-format parsing (PDF, DOCX, TXT), ATS score calculation, checklist audits,
and STAR method bullet point rewriting with Original vs Improved comparisons.
"""
import re
from modules.resume_analyzer import (
    extract_text_from_pdf, extract_skills_from_text, evaluate_resume_quality, SKILL_TAXONOMY
)
from modules.semantic_matcher import optimize_resume_bullet, compute_semantic_cosine_similarity

class ResumeService:
    @staticmethod
    def parse_resume_file(uploaded_file) -> dict:
        """Parses PDF, DOCX, or TXT file into text and extracts recognized skills."""
        if uploaded_file is None:
            return {"text": "", "skills": [], "file_name": ""}

        filename = uploaded_file.name.lower()
        text = ""

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif filename.endswith(".txt"):
            try:
                text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            except Exception:
                text = str(uploaded_file.getvalue())
        elif filename.endswith(".docx"):
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([p.text for p in doc.paragraphs])
            except Exception:
                text = "DOCX parser: Please paste text below."
        else:
            text = "Unsupported file type."

        skills = extract_skills_from_text(text)
        return {
            "text": text,
            "skills": skills,
            "file_name": uploaded_file.name
        }

    @staticmethod
    def evaluate_ats_quality(text: str, skills: list) -> dict:
        """Evaluates ATS formatting, contact details, action verbs, and section checklist."""
        return evaluate_resume_quality(text, skills)

    @staticmethod
    def optimize_bullet(original_bullet: str, target_role: str) -> dict:
        """Rewrites a weak bullet point into STAR format with action verbs and impact metrics."""
        return optimize_resume_bullet(original_bullet, target_role)

    @staticmethod
    def compute_job_match_similarity(resume_text: str, jd_text: str) -> float:
        """Computes TF-IDF cosine similarity between resume and job description."""
        return compute_semantic_cosine_similarity(resume_text, jd_text)
