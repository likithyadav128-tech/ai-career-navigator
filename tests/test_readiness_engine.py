"""
Career Readiness and Matching Tests
"""
import unittest
from services.career_matching_service import CareerMatchingService
from services.readiness_service import ReadinessService
from modules.skill_gap_engine import analyze_skill_gaps

class TestReadinessAndMatching(unittest.TestCase):
    def test_career_matching(self):
        skills = ["Python", "SQL", "Excel", "Power BI", "Statistics"]
        matches = CareerMatchingService.match_all_careers(skills, interests=["Big Data", "Data Analytics"])
        
        self.assertGreater(len(matches), 10)
        # Data Analyst should rank high with SQL, Excel, Power BI, Statistics
        top_role = matches[0]["role"]
        self.assertIn(top_role, ["Data Analyst", "Business Intelligence Engineer", "Data Scientist"])
        self.assertGreaterEqual(matches[0]["match_score"], 60.0)

    def test_7_factor_readiness(self):
        gap_res = analyze_skill_gaps(["Python", "SQL", "Excel", "Power BI"], ["SQL", "Python", "Excel", "Power BI", "Tableau", "Statistics"])
        res = ReadinessService.calculate_readiness(
            resume_score=85.0,
            skill_gap_result=gap_res,
            project_score=80.0,
            assessment_score=75.0,
            interview_score=70.0,
            communication_score=80.0,
            evidence_score=85.0,
            target_role="Data Analyst",
            target_company="Any Company (General Industry Standard)"
        )
        self.assertGreater(res["overall_readiness"], 50.0)
        self.assertIn("factors", res)
        self.assertEqual(len(res["factors"]), 7)

if __name__ == "__main__":
    unittest.main()
