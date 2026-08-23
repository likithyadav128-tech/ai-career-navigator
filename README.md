# 🎯 AI Career Accelerator & Skill Gap Platform

An end-to-end, AI-powered web application that analyzes student resumes, parses target job descriptions, conducts skill gap matrix evaluation, generates personalized learning roadmaps, recommends hands-on projects, coaches mock interviews, and answers career questions in real-time.

---

## 🚀 Key Modules & Features

1. 📈 **Career Dashboard**: Real-time Job Readiness Gauge %, ATS Resume Score, Skill Gap Matrix donut chart, and Competency Radar comparing candidate skills against job targets.
2. 📄 **AI Resume Analyzer**: PDF upload, automatic section parsing, keyword extraction, ATS scoring engine (contact info, impact metrics, action verbs, density).
3. 💼 **Job Description Analyzer**: Extracts technical vs. soft skills, experience tier detection, and target role profile.
4. 📊 **AI Skill Gap Analysis**: Categorizes skills into **Strong** (exact match), **Moderate** (foundational match), and **Missing** (high-priority gap).
5. 🗺️ **Personalized AI Roadmap**: Step-by-step phased learning path tailored to missing skills with timeline estimates and recommended resources.
6. 💡 **AI Project Recommender**: Tailored portfolio project suggestions with tech stack specs, difficulty ratings, and architecture blueprints.
7. 🎤 **AI Mock Interview Coach**: Role-specific technical & behavioral interview question generator, answer submission, instant score /10, and rubric feedback.
8. 🤖 **AI Career Assistant**: Conversational AI chatbot pre-loaded with candidate resume context answering *"What should I learn next?"*, *"Am I ready for a Data Analyst role?"*, etc.

---

## 🛠️ Project Structure

```text
ai_career_navigator/
├── app.py                      # Main Streamlit UI & layout engine
├── requirements.txt            # Python dependencies
├── README.md                   # Setup & deployment guide
└── modules/
    ├── __init__.py
    ├── sample_data.py          # Pre-configured student resumes & JDs for 1-click testing
    ├── resume_analyzer.py      # PDF parser, keyword extractor, ATS scoring
    ├── job_analyzer.py         # JD parser & skill taxonomy matcher
    ├── skill_gap_engine.py     # Skill gap matrix & job readiness score calculator
    ├── roadmap_generator.py    # Phased personalized learning roadmap builder
    ├── project_recommender.py  # Recommended portfolio project catalog & matcher
    ├── interview_coach.py      # Role-specific question bank & answer evaluator
    ├── career_assistant.py     # Conversational career assistant chatbot engine
    └── dashboard_metrics.py    # Plotly gauge, radar, donut & metric visualization generators
```

---

## ⚡ Quick Start (Local Run)

1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\likit\.gemini\antigravity\scratch\ai_career_navigator
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Streamlit web application:**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Deployment Options

- **Streamlit Community Cloud**: Connect your GitHub repository and point to `app.py`.
- **Hugging Face Spaces**: Select Streamlit SDK and upload repo files.
- **Render / Railway**: Use standard Python container service running `streamlit run app.py --server.port $PORT`.
