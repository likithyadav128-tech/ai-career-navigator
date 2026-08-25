"""
AI Career Accelerator & Skill Gap Platform
Full-stack Streamlit Application - Reorganized Layout Edition
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Imports from local modules
from modules.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
from modules.resume_analyzer import extract_text_from_pdf, extract_skills_from_text, evaluate_resume_quality
from modules.job_analyzer import analyze_job_description
from modules.skill_gap_engine import analyze_skill_gaps
from modules.roadmap_generator import generate_personalized_roadmap
from modules.project_recommender import recommend_projects_for_student
from modules.interview_coach import get_questions_for_role, evaluate_student_answer
from modules.career_assistant import generate_assistant_response
from modules.dashboard_metrics import (
    create_readiness_gauge,
    create_skill_distribution_chart,
    create_competency_radar_chart
)

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Career Accelerator & Skill Gap Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast CSS with Fixed Sidebar Contrast
st.markdown("""
<style>
    /* Main Background & Base Typography */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Sidebar Dark Theme with High-Contrast White Text */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #F8FAFC !important;
    }
    
    /* Sidebar Navigation Radio Options Styling */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #F8FAFC !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }
    
    /* Input Fields, Selectboxes & Textareas styling */
    .stSelectbox label, .stTextArea label, .stTextInput label, .stFileUploader label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0F172A !important;
    }
    textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    /* Main Header Banner */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #1D4ED8 100%);
        color: #FFFFFF !important;
        padding: 28px 36px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px -4px rgba(29, 78, 216, 0.25);
    }
    .main-header h1 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 1.05rem !important;
        color: #E2E8F0 !important;
        margin-top: 8px !important;
        margin-bottom: 0 !important;
    }

    /* Metric Cards */
    .card-metric {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px 16px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        text-align: center;
        margin-bottom: 16px;
    }
    .card-metric-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .card-metric-value {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
    }

    /* Content Cards */
    .content-box {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    /* High-Contrast Skill Tags */
    .tag-strong {
        background-color: #DCFCE7 !important;
        color: #15803D !important;
        border: 1.5px solid #16A34A !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
    }
    .tag-moderate {
        background-color: #FEF3C7 !important;
        color: #B45309 !important;
        border: 1.5px solid #D97706 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
    }
    .tag-missing {
        background-color: #FEE2E2 !important;
        color: #B91C1C !important;
        border: 1.5px solid #DC2626 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
    }
    .tag-bonus {
        background-color: #DBEAFE !important;
        color: #1E40AF !important;
        border: 1.5px solid #2563EB !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "candidate_text" not in st.session_state:
    default_res = SAMPLE_RESUMES["Data Science Student (Alex Rivera)"]
    st.session_state["candidate_text"] = default_res["text"]
    st.session_state["candidate_skills"] = default_res["extracted_skills"]

if "target_jd_text" not in st.session_state:
    default_jd = SAMPLE_JOB_DESCRIPTIONS["Data Scientist"]
    st.session_state["target_jd_text"] = default_jd["text"]
    st.session_state["target_role"] = default_jd["title"]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hi! I'm your AI Career Assistant. Ask me anything like:\n- *'What should I learn next?'*\n- *'Am I ready for a Data Analyst role?'*\n- *'Which skills should I add to my resume?'*"}
    ]

# ---------------------------------------------------------
# LEFT SIDEBAR: MODULE NAVIGATION MENU
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <div style="font-size: 2.8rem;">🎯</div>
        <h2 style="margin: 0; color: #FFFFFF; font-size: 1.35rem;">AI Career Copilot</h2>
        <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Skill Gap & Career Navigator</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 📌 Select Module")
    
    nav_module = st.radio(
        "Navigation:",
        [
            "📈 Career Dashboard",
            "📄 AI Resume Analyzer",
            "💼 Job Description Analyzer",
            "📊 Skill Gap Analysis",
            "🗺️ Personalized AI Roadmap",
            "💡 AI Project Recommender",
            "🎤 AI Mock Interview Coach",
            "🤖 AI Career Assistant"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    
    # Active Role Badge Widget in Sidebar
    st.markdown("### 🎯 Active Profile")
    st.markdown(f"**Target Role:** `{st.session_state['target_role'][:20]}`")
    st.markdown(f"**Extracted Skills:** `{len(st.session_state['candidate_skills'])} skills`")

# ---------------------------------------------------------
# MAIN AREA: HEADER & DATA INPUT CONTROL PANEL
# ---------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <h1>🎯 AI Career Accelerator & Skill Gap Navigator</h1>
    <p>AI Resume Analytics • Job Description Matching • Phased Learning Roadmap • Portfolio Projects • Interview Coaching</p>
</div>
""", unsafe_allow_html=True)

# Main Data Input Control Drawer / Expandable Card
with st.expander("⚙️ **Configure Profile Data & Target Job Description** (Click to expand/edit your Resume & Target Job)", expanded=False):
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("1. Candidate Resume Input")
        sample_res_choice = st.selectbox(
            "Load Sample Student Profile:",
            ["Custom Upload / Input", "Data Science Student (Alex Rivera)", "Software & Web Developer (Sam Chen)"]
        )
        
        if sample_res_choice != "Custom Upload / Input":
            st.session_state["candidate_text"] = SAMPLE_RESUMES[sample_res_choice]["text"]
            st.session_state["candidate_skills"] = SAMPLE_RESUMES[sample_res_choice]["extracted_skills"]
        else:
            uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"])
            if uploaded_pdf is not None:
                pdf_text = extract_text_from_pdf(uploaded_pdf)
                st.session_state["candidate_text"] = pdf_text
                st.session_state["candidate_skills"] = extract_skills_from_text(pdf_text)
            else:
                resume_text_input = st.text_area("Or Paste Resume Text:", value=st.session_state["candidate_text"], height=160)
                if resume_text_input:
                    st.session_state["candidate_text"] = resume_text_input
                    st.session_state["candidate_skills"] = extract_skills_from_text(resume_text_input)

    with col_input2:
        st.subheader("2. Target Job Description Input")
        sample_jd_choice = st.selectbox(
            "Load Sample Target Job:",
            ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "Custom Job Description"]
        )
        
        if sample_jd_choice != "Custom Job Description":
            st.session_state["target_jd_text"] = SAMPLE_JOB_DESCRIPTIONS[sample_jd_choice]["text"]
            st.session_state["target_role"] = SAMPLE_JOB_DESCRIPTIONS[sample_jd_choice]["title"]
        else:
            jd_input = st.text_area("Paste Target Job Description:", value=st.session_state["target_jd_text"], height=160)
            if jd_input:
                st.session_state["target_jd_text"] = jd_input
                st.session_state["target_role"] = "Custom Target Role"
                
    st.markdown('</div>', unsafe_allow_html=True)

# Compute Core Analytics Engine
resume_eval = evaluate_resume_quality(st.session_state["candidate_text"], st.session_state["candidate_skills"])
jd_eval = analyze_job_description(st.session_state["target_jd_text"])
gap_eval = analyze_skill_gaps(st.session_state["candidate_skills"], jd_eval["all_required_skills"])

# ---------------------------------------------------------
# MODULE 1: CAREER DASHBOARD
# ---------------------------------------------------------
if nav_module == "📈 Career Dashboard":
    st.markdown("## 📈 Executive Career Readiness Overview")
    
    # 4 Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        readiness_color = '#16A34A' if gap_eval['readiness_score'] >= 75 else ('#D97706' if gap_eval['readiness_score'] >= 50 else '#DC2626')
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Job Readiness Score</div>
            <div class="card-metric-value" style="color: {readiness_color};">{gap_eval['readiness_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Resume ATS Score</div>
            <div class="card-metric-value" style="color: #2563EB;">{resume_eval['score']}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Target Role</div>
            <div class="card-metric-value" style="font-size: 1.35rem; padding-top: 10px;">{jd_eval['title'][:22]}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Missing Skill Gaps</div>
            <div class="card-metric-value" style="color: #DC2626;">{gap_eval['missing_count']} Missing</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Gauge Chart & Skill Matrix Donut
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        gauge_fig = create_readiness_gauge(gap_eval["readiness_score"])
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_g2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        donut_fig = create_skill_distribution_chart(
            gap_eval["strong_count"], gap_eval["moderate_count"], gap_eval["missing_count"]
        )
        st.plotly_chart(donut_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Radar Chart & Action Plan
    r_col1, r_col2 = st.columns([1.2, 1])
    with r_col1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        radar_fig = create_competency_radar_chart(st.session_state["candidate_skills"], jd_eval["all_required_skills"])
        st.plotly_chart(radar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r_col2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### ⚡ Priority Action Items")
        if gap_eval["readiness_score"] >= 80:
            st.success("🎉 **High Job Readiness!** Your skill profile is competitive for " + jd_eval['title'] + ". Focus on mock interviews!")
        elif gap_eval["readiness_score"] >= 50:
            st.warning("⚡ **Moderate Readiness!** You have solid fundamentals. Closing 2-3 key missing skills will elevate your readiness above 80%.")
        else:
            st.error("🎯 **Skills Gap Identified.** We recommend executing Phase 1 & 2 of your Personalized Learning Roadmap.")

        st.markdown("#### 🔑 Immediate Focus Skills:")
        if gap_eval["missing_skills"]:
            for item in gap_eval["missing_skills"][:4]:
                st.markdown(f"- 🔴 **{item['skill']}**: High-demand requirement for {jd_eval['title']}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 2: AI RESUME ANALYZER
# ---------------------------------------------------------
elif nav_module == "📄 AI Resume Analyzer":
    st.markdown("## 📄 AI Resume Quality & ATS Keyword Analysis")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(f"### ATS Score: **{resume_eval['score']} / 100**")
        st.progress(resume_eval['score'] / 100)
        
        st.markdown("#### 📋 Quality Criteria Checklist:")
        for check_name, check_val in resume_eval["checks"].items():
            st.markdown(f"- **{check_name}**: `{check_val}`")
            
        if resume_eval["feedback"]:
            st.markdown("#### 💡 Resume Optimization Recommendations:")
            for tip in resume_eval["feedback"]:
                st.info(tip)
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col_a2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Extracted Resume Skills")
        st.write(f"Identified **{len(st.session_state['candidate_skills'])}** technical and analytical skills from your resume text:")
        
        skills_html = "".join([f'<span class="tag-strong">{s}</span>' for s in st.session_state['candidate_skills']])
        st.markdown(f'<div style="margin-top: 15px;">{skills_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🔍 View Extracted Resume Raw Text"):
        st.text(st.session_state["candidate_text"])

# ---------------------------------------------------------
# MODULE 3: JOB DESCRIPTION ANALYZER
# ---------------------------------------------------------
elif nav_module == "💼 Job Description Analyzer":
    st.markdown("## 💼 Target Job Description Breakdown")
    
    st.markdown(f"""
    <div class="content-box">
        <h2 style="margin:0; color:#0F172A;">Target Role: {jd_eval['title']}</h2>
        <p style="font-size:1.1rem; color:#475569; margin-top:8px;">Experience Tier Requirement: <strong>{jd_eval['exp_level']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### 💻 Required Technical Skills")
        tech_html = "".join([f'<span class="tag-bonus">{s}</span>' for s in jd_eval['tech_skills']])
        st.markdown(f'<div>{tech_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_j2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### 🤝 Required Soft & Domain Skills")
        soft_html = "".join([f'<span class="tag-moderate">{s}</span>' for s in jd_eval['soft_skills']])
        if not soft_html:
            soft_html = '<span class="tag-moderate">Problem Solving</span><span class="tag-moderate">Communication</span>'
        st.markdown(f'<div>{soft_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📄 View Full Job Description Text"):
        st.text(jd_eval["raw_text"])

# ---------------------------------------------------------
# MODULE 4: AI SKILL GAP ANALYSIS
# ---------------------------------------------------------
elif nav_module == "📊 Skill Gap Analysis":
    st.markdown("## 📊 Comprehensive Skill Gap Matrix")
    st.markdown(f"Comparing candidate resume skills against target job requirements for **{jd_eval['title']}**.")
    
    col_sg1, col_sg2, col_sg3 = st.columns(3)
    
    with col_sg1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(f"### 🟢 Strong Skills ({gap_eval['strong_count']})")
        st.caption("Exact skill verified on candidate resume")
        for item in gap_eval["strong_skills"]:
            st.markdown(f"- <span class='tag-strong'>{item['skill']}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_sg2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(f"### 🟡 Moderate Skills ({gap_eval['moderate_count']})")
        st.caption("Foundational match via related tools")
        for item in gap_eval["moderate_skills"]:
            st.markdown(f"- <span class='tag-moderate'>{item['skill']}</span><br><small style='color:#64748B;'>{item['reason']}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_sg3:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(f"### 🔴 Missing Skills ({gap_eval['missing_count']})")
        st.caption("High-priority skills to acquire")
        for item in gap_eval["missing_skills"]:
            st.markdown(f"- <span class='tag-missing'>{item['skill']}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if gap_eval["bonus_skills"]:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### ✨ Candidate Bonus Skills")
        st.caption("Skills on resume that distinguish you beyond the base JD requirements:")
        bonus_html = "".join([f'<span class="tag-bonus">{s}</span>' for s in gap_eval['bonus_skills'][:12]])
        st.markdown(f'<div>{bonus_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 5: PERSONALIZED AI ROADMAP
# ---------------------------------------------------------
elif nav_module == "🗺️ Personalized AI Roadmap":
    st.markdown("## 🗺️ Personalized AI Learning Roadmap")
    st.markdown("Custom step-by-step learning sequence engineered to bridge your specific skill gaps.")
    
    roadmap_phases = generate_personalized_roadmap(gap_eval["missing_skills"], gap_eval["moderate_skills"], jd_eval["title"])
    
    for idx, phase in enumerate(roadmap_phases, 1):
        with st.expander(f"📍 {phase['phase']}  |  ⏱️ {phase['duration']}", expanded=(idx <= 2)):
            st.markdown(f"**Focus Objective:** {phase['focus']}")
            st.markdown(f"**Key Topics to Master:** `{', '.join(phase['topics'])}`")
            
            st.markdown("#### 🎯 Actionable Implementation Steps:")
            for step in phase["action_steps"]:
                st.checkbox(step, key=f"step_rd_{idx}_{step[:15]}")
                
            st.markdown("#### 📚 Recommended Free Resources:")
            for res in phase["recommended_resources"]:
                st.markdown(f"- 📖 {res}")

# ---------------------------------------------------------
# MODULE 6: AI PROJECT RECOMMENDER
# ---------------------------------------------------------
elif nav_module == "💡 AI Project Recommender":
    st.markdown("## 💡 AI Portfolio Project Recommender")
    st.markdown("Recommended portfolio projects designed to demonstrate your target missing skills to employers.")
    
    recommended_projs = recommend_projects_for_student(gap_eval["missing_skills"], gap_eval["moderate_skills"], jd_eval["title"])
    
    for p in recommended_projs:
        st.markdown(f"""
        <div class="content-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; color:#0F172A;">🚀 {p['title']}</h3>
                <span class="tag-bonus" style="background:#DBEAFE; color:#1E40AF;">{p['difficulty']}</span>
            </div>
            <p style="color:#334155; font-size:1.05rem; margin-top:12px;">{p['description']}</p>
            <p style="margin-bottom:0;"><strong>🛠️ Tech Stack Specs:</strong> <code>{" , ".join(p['tech_stack'])}</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📐 View Implementation & Architecture Blueprint for '{p['title'][:35]}...'"):
            st.markdown("#### Step-by-Step Architecture Steps:")
            for step_i, step_txt in enumerate(p["architecture_steps"], 1):
                st.markdown(f"**Step {step_i}:** {step_txt}")
            st.info("💡 **Resume Impact Tip:** Add this project under your Resume Projects section with quantitative metrics!")

# ---------------------------------------------------------
# MODULE 7: AI MOCK INTERVIEW COACH
# ---------------------------------------------------------
elif nav_module == "🎤 AI Mock Interview Coach":
    st.markdown("## 🎤 AI Mock Interview Coach")
    st.markdown(f"Practice role-specific interview questions for **{jd_eval['title']}** and get instant scoring & feedback.")
    
    questions = get_questions_for_role(jd_eval["title"])
    
    selected_q_idx = st.selectbox("Select Question to Practice:", range(len(questions)), format_func=lambda i: f"Q{i+1}: [{questions[i]['category']}] {questions[i]['question'][:60]}...")
    
    q_curr = questions[selected_q_idx]
    
    st.markdown(f"""
    <div class="content-box" style="border-left: 6px solid #2563EB;">
        <h4 style="margin:0; color:#2563EB;">Category: {q_curr['category']}</h4>
        <h3 style="margin-top:8px; color:#0F172A;">{q_curr['question']}</h3>
        <p style="color:#64748B; font-size:0.95rem; margin-bottom:0;"><em>Evaluates: {q_curr['rubric']}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    student_ans = st.text_area("✍️ Type your detailed answer here:", height=160, placeholder="Explain your answer using STAR technique or technical concepts...")
    
    if st.button("🚀 Evaluate Answer with AI Coach", type="primary"):
        if student_ans.strip():
            eval_res = evaluate_student_answer(q_curr, student_ans)
            
            st.markdown(f"""
            <div class="content-box">
                <h3 style="margin:0;">AI Score: <strong>{eval_res['score']} / 10</strong> ({eval_res['rating']})</h3>
            </div>
            """, unsafe_allow_html=True)
            st.progress(eval_res['score'] / 10)
            
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.success("✅ **Strengths Identified:**")
                for s in eval_res["strengths"]:
                    st.markdown(f"- {s}")
                st.markdown('</div>', unsafe_allow_html=True)
            with e_col2:
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.warning("💡 **Improvement Feedback:**")
                for imp in eval_res["improvements"]:
                    st.markdown(f"- {imp}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please type an answer before submitting for evaluation.")

# ---------------------------------------------------------
# MODULE 8: AI CAREER ASSISTANT
# ---------------------------------------------------------
elif nav_module == "🤖 AI Career Assistant":
    st.markdown("## 🤖 AI Career Assistant Chatbot")
    st.markdown("Ask instant career questions. Your active resume and skill gap context are loaded into the AI assistant!")
    
    st.markdown("##### ⚡ Quick Prompt Triggers:")
    p_col1, p_col2, p_col3 = st.columns(3)
    
    preset_clicked = None
    with p_col1:
        if st.button("💡 What should I learn next?"):
            preset_clicked = "What should I learn next?"
    with p_col2:
        if st.button("📊 Am I ready for this role?"):
            preset_clicked = "Am I ready for a Data Analyst role?"
    with p_col3:
        if st.button("📄 Which skills should I add?"):
            preset_clicked = "Which skills should I add to my resume?"

    # Context dictionary for assistant
    ctx = {
        "candidate_skills": st.session_state["candidate_skills"],
        "target_role": jd_eval["title"],
        "readiness_score": gap_eval["readiness_score"],
        "missing_skills": gap_eval["missing_skills"],
        "moderate_skills": gap_eval["moderate_skills"],
        "strong_skills": gap_eval["strong_skills"],
        "resume_score": resume_eval["score"]
    }

    # Handle preset selection
    if preset_clicked:
        st.session_state["chat_history"].append({"role": "user", "content": preset_clicked})
        ans = generate_assistant_response(preset_clicked, ctx)
        st.session_state["chat_history"].append({"role": "assistant", "content": ans})

    # Render Chat History
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_query = st.chat_input("Ask your career assistant anything...")
    if user_query:
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        ans = generate_assistant_response(user_query, ctx)
        st.session_state["chat_history"].append({"role": "assistant", "content": ans})
        st.rerun()
