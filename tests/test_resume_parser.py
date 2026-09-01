"""
Resume Parser and Skill Extraction Unit Tests
"""
import unittest
from modules.resume_analyzer import extract_skills_from_text, evaluate_resume_quality

class TestResumeParser(unittest.TestCase):
    def test_skill_extraction(self):
        sample_text = """
        Alex Rivera
        Email: alex@example.com | Phone: (555) 123-4567 | github.com/arivera
        Skills: Python, SQL, Excel, JOINs, Pandas, PyTorch, Power BI, Statistics, Machine Learning, Fastapi, Docker
        Experience: Developed customer churn prediction model with 89.2% accuracy.
        """
        skills = extract_skills_from_text(sample_text)
        self.assertIn("Python", skills)
        self.assertIn("SQL", skills)
        self.assertIn("Excel", skills)
        self.assertIn("JOINs", skills)
        self.assertIn("Pandas", skills)
        self.assertIn("PyTorch", skills)
        self.assertIn("Power BI", skills)

    def test_resume_ats_quality(self):
        text = """
        Jane Doe
        jane@email.com | (555) 987-6543 | github.com/janedoe | linkedin.com/in/janedoe
        Education: Bachelor of Science in Computer Science
        Experience: Built real-time analytics pipeline reducing latency by 45%. Spearheaded 3 machine learning projects.
        Skills: Python, SQL, Scikit-learn, Docker, FastAPI, Git
        Projects: Developed fraud detection engine on 100k transactions.
        """
        eval_res = evaluate_resume_quality(text, ["Python", "SQL", "Scikit-learn", "Docker", "FastAPI", "Git"])
        self.assertGreaterEqual(eval_res["score"], 60)
        self.assertIn("Contact Information", eval_res["checks"])
        self.assertIn("Core Resume Sections", eval_res["checks"])

if __name__ == "__main__":
    unittest.main()
