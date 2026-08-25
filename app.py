"""
AI Career Accelerator & Skill Gap Platform
Next-Level Animated UI & Semantic Intelligence Edition
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
from modules.github_verifier import verify_github_profile
from modules.semantic_matcher import compute_semantic_cosine_similarity, optimize_resume_bullet
from modules.dashboard_metrics import (
    create_readiness_gauge,
    create_skill_distribution_chart,
    create_competency_radar_chart
)

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Career Accelerator & Skill Gap Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject High-End Next-Level CSS with Moving Animated Background & Glassmorphism
st.markdown("""
<style>
    /* Keyframe Moving Gradient Background */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #090D16, #0F172A, #1E1B4B, #0F172A, #020617) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 18s ease infinite !important;
        color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Glassmorphism Content Box */
    .glass-card {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 20px !important;
        padding: 28px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease !important;
    }
    .glass-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px 0 rgba(56, 189, 248, 0.2) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
    }

    /* Animated Pulse Glow for Metric Cards */
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.4); }
        70% { box-shadow: 0 0 0 14px rgba(56, 189, 248, 0); }
        100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
    }
    
    .card-metric {
        background: rgba(30, 41, 59, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        padding: 22px 18px !important;
        text-align: center !important;
        margin-bottom: 18px !important;
        transition: transform 0.3s ease !important;
    }
    .card-metric:hover {
        transform: scale(1.03) !important;
        border-color: #38BDF8 !important;
    }
    .card-metric-title {
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 6px !important;
    }
    .card-metric-value {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #F8FAFC !important;
    }

    /* Main Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,27,75,0.9) 50%, rgba(29,78,216,0.9) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 32px 40px !important;
        border-radius: 24px !important;
        margin-bottom: 28px !important;
        box-shadow: 0 12px 40px -5px rgba(56, 189, 248, 0.3) !important;
    }
    .hero-title {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.15rem !important;
        color: #CBD5E1 !important;
        margin-top: 10px !important;
        margin-bottom: 0 !important;
    }

    /* Glowing Neon Skill Badges */
    .tag-strong {
        background: rgba(22, 163, 74, 0.25) !important;
        color: #4ADE80 !important;
        border: 1.5px solid #22C55E !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.2);
    }
    .tag-moderate {
        background: rgba(217, 119, 6, 0.25) !important;
        color: #FBBF24 !important;
        border: 1.5px solid #F59E0B !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
    }
    .tag-missing {
        background: rgba(220, 38, 38, 0.25) !important;
        color: #FCA5A5 !important;
        border: 1.5px solid #EF4444 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }
    .tag-bonus {
        background: rgba(37, 99, 235, 0.25) !important;
        color: #60A5FA !important;
        border: 1.5px solid #3B82F6 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        margin: 4px;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
    }
    
    /* Sidebar Dark Glass */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
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

if "github_user" not in st.session_state:
    st.session_state["github_user"] = "arivera"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hi! I'm your AI Career Assistant. Ask me anything like:\n- *'What should I learn next?'*\n- *'Am I ready for a Data Analyst role?'*\n- *'Which skills should I add to my resume?'*"}
    ]

# ---------------------------------------------------------
# SIDEBAR: NAVIGATION MENU & GITHUB VERIFIER
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <div style="font-size: 3rem;">⚡</div>
        <h2 style="margin: 0; color: #F8FAFC; font-size: 1.4rem; font-weight:800;">AI Career Copilot</h2>
        <p style="color: #38BDF8; font-size: 0.88rem; font-weight:600; margin-top: 4px;">Next-Gen Career Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 📌 Select Module")
    
    nav_module = st.radio(
        "Navigation:",
        [
            "📈 Career Dashboard",
            "🔗 GitHub Verifier",
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
    
    # Active Role & GitHub Input Widget
    st.markdown("### 🎯 Profile Controls")
    st.markdown(f"**Target Role:** `{st.session_state['target_role'][:22]}`")
    
    gh_input = st.text_input("Verify GitHub Profile:", value=st.session_state["github_user"], placeholder="Enter GitHub username...")
    if gh_input:
        st.session_state["github_user"] = gh_input

# ---------------------------------------------------------
# MAIN AREA: HERO BANNER & CONTROL DRAWER
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero-banner">
    <h1 class="hero-title">⚡ AI Career Accelerator & Skill Gap Platform</h1>
    <p class="hero-subtitle">Semantic Vector NLP • Live GitHub Verifier • Resume ATS Optimization • Phased Roadmaps • AI Interview Coach</p>
</div>
""", unsafe_allow_html=True)

# Main Data Input Control Drawer
with st.expander("⚙️ **Configure Candidate Resume & Target Job Description** (Click to edit inputs)", expanded=False):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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

# Compute Core & Semantic Analytics
resume_eval = evaluate_resume_quality(st.session_state["candidate_text"], st.session_state["candidate_skills"])
jd_eval = analyze_job_description(st.session_state["target_jd_text"])
gap_eval = analyze_skill_gaps(st.session_state["candidate_skills"], jd_eval["all_required_skills"])
semantic_sim = compute_semantic_cosine_similarity(st.session_state["candidate_text"], st.session_state["target_jd_text"])
github_res = verify_github_profile(st.session_state["github_user"])

# ---------------------------------------------------------
# MODULE 1: CAREER DASHBOARD
# ---------------------------------------------------------
if nav_module == "📈 Career Dashboard":
    st.markdown("## 📈 Executive Career Readiness Overview")
    
    # 4 Glowing Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        readiness_color = '#4ADE80' if gap_eval['readiness_score'] >= 75 else ('#FBBF24' if gap_eval['readiness_score'] >= 50 else '#FCA5A5')
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Job Readiness</div>
            <div class="card-metric-value" style="color: {readiness_color};">{gap_eval['readiness_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Semantic Vector Match</div>
            <div class="card-metric-value" style="color: #38BDF8;">{semantic_sim}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Resume ATS Score</div>
            <div class="card-metric-value" style="color: #818CF8;">{resume_eval['score']}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-metric-title">Developer Badge</div>
            <div class="card-metric-value" style="font-size: 1.15rem; color: {github_res.get('badge_color', '#38BDF8')};">{github_res.get('status_badge', '⚡ Active Dev')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Gauge Chart & Skill Matrix Donut
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        gauge_fig = create_readiness_gauge(gap_eval["readiness_score"])
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_g2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        donut_fig = create_skill_distribution_chart(
            gap_eval["strong_count"], gap_eval["moderate_count"], gap_eval["missing_count"]
        )
        st.plotly_chart(donut_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Radar Chart & Action Plan
    r_col1, r_col2 = st.columns([1.2, 1])
    with r_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        radar_fig = create_competency_radar_chart(st.session_state["candidate_skills"], jd_eval["all_required_skills"])
        st.plotly_chart(radar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Priority Action Items")
        if gap_eval["readiness_score"] >= 80:
            st.success("🎉 **High Job Readiness!** Your profile strongly matches target requirements for " + jd_eval['title'])
        elif gap_eval["readiness_score"] >= 50:
            st.warning("⚡ **Moderate Readiness!** Closing 2-3 key missing skills elevates readiness score above 80%.")
        else:
            st.error("🎯 **Skill Gap Identified.** Execute Phase 1 & 2 of your Personalized Learning Roadmap.")

        st.markdown("#### 🔑 High Impact Missing Skills:")
        if gap_eval["missing_skills"]:
            for item in gap_eval["missing_skills"][:4]:
                st.markdown(f"- 🔴 **{item['skill']}**: High requirement for {jd_eval['title']}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 2: GITHUB VERIFIER
# ---------------------------------------------------------
elif nav_module == "🔗 GitHub Verifier":
    st.markdown("## 🔗 Live GitHub Automated Profile Verifier")
    
    if github_res.get("verified"):
        st.markdown(f"""
        <div class="glass-card" style="border-left: 6px solid {github_res['badge_color']};">
            <div style="display:flex; align-items:center; gap:20px;">
                <img src="{github_res['avatar_url']}" style="width:80px; height:80px; border-radius:50%; border:3px solid {github_res['badge_color']};">
                <div>
                    <h2 style="margin:0; color:#F8FAFC;">{github_res['name']} (<a href="{github_res['profile_url']}" target="_blank" style="color:#38BDF8;">@{github_res['username']}</a>)</h2>
                    <h3 style="margin-top:6px; color:{github_res['badge_color']};">{github_res['status_badge']}</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        g1, g2, g3, g4 = st.columns(4)
        with g1:
            st.markdown(f'<div class="card-metric"><div class="card-metric-title">Public Repos</div><div class="card-metric-value">{github_res["public_repos"]}</div></div>', unsafe_allow_html=True)
        with g2:
            st.markdown(f'<div class="card-metric"><div class="card-metric-title">Total Stars</div><div class="card-metric-value">{github_res["total_stars"]}</div></div>', unsafe_allow_html=True)
        with g3:
            st.markdown(f'<div class="card-metric"><div class="card-metric-title">Followers</div><div class="card-metric-value">{github_res["followers"]}</div></div>', unsafe_allow_html=True)
        with g4:
            st.markdown(f'<div class="card-metric"><div class="card-metric-title">Dev Score</div><div class="card-metric-value" style="color:#38BDF8;">{github_res["developer_score"]}/100</div></div>', unsafe_allow_html=True)

        gh_col1, gh_col2 = st.columns(2)
        with gh_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Primary Code Languages")
            if github_res["languages"]:
                df_lang = pd.DataFrame(list(github_res["languages"].items()), columns=["Language", "Repositories"])
                fig_lang = px.pie(df_lang, values="Repositories", names="Language", hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_lang.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'))
                st.plotly_chart(fig_lang, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with gh_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🛠️ Verified Technology Repositories")
            if github_res["verified_tech"]:
                verified_html = "".join([f'<span class="tag-strong">✓ {t}</span>' for t in github_res["verified_tech"]])
                st.markdown(f'<div style="margin-top:15px;">{verified_html}</div>', unsafe_allow_html=True)
            else:
                st.info("No specific framework keywords detected in repository descriptions.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(github_res.get("error", "Unable to fetch GitHub profile."))

# ---------------------------------------------------------
# MODULE 3: AI RESUME ANALYZER & BULLET OPTIMIZER
# ---------------------------------------------------------
elif nav_module == "📄 AI Resume Analyzer":
    st.markdown("## 📄 AI Resume Quality & Bullet Optimizer")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### ATS Quality Score: **{resume_eval['score']} / 100**")
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
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Extracted Resume Skills")
        st.write(f"Identified **{len(st.session_state['candidate_skills'])}** technical skills:")
        
        skills_html = "".join([f'<span class="tag-strong">{s}</span>' for s in st.session_state['candidate_skills']])
        st.markdown(f'<div style="margin-top: 15px;">{skills_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Interactive AI Resume Bullet Optimizer Tool
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ✨ AI Resume Bullet Optimizer (STAR Method Generator)")
    st.markdown("Paste any weak resume bullet point to instantly rewrite it into a high-impact, quantified STAR-method bullet point:")
    
    user_bullet = st.text_input("Paste Bullet Point:", value="Worked on customer churn prediction model using Python", placeholder="e.g. Built a machine learning model for churn...")
    if st.button("🚀 Transform with AI Optimizer", type="primary"):
        opt_res = optimize_resume_bullet(user_bullet, jd_eval["title"])
        st.success("✅ **STAR Method Optimized Bullet Point:**")
        st.code(opt_res["optimized"], language="text")
        st.caption(f"Action Verb: **{opt_res['action_verb']}** | Quantified Metric: **{opt_res['impact_metric']}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 4: JOB DESCRIPTION ANALYZER
# ---------------------------------------------------------
elif nav_module == "💼 Job Description Analyzer":
    st.markdown("## 💼 Target Job Description Breakdown")
    
    st.markdown(f"""
    <div class="glass-card">
        <h2 style="margin:0; color:#F8FAFC;">Target Role: {jd_eval['title']}</h2>
        <p style="font-size:1.1rem; color:#38BDF8; margin-top:8px;">Experience Tier Requirement: <strong>{jd_eval['exp_level']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💻 Required Technical Skills")
        tech_html = "".join([f'<span class="tag-bonus">{s}</span>' for s in jd_eval['tech_skills']])
        st.markdown(f'<div>{tech_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_j2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤝 Required Soft & Domain Skills")
        soft_html = "".join([f'<span class="tag-moderate">{s}</span>' for s in jd_eval['soft_skills']])
        if not soft_html:
            soft_html = '<span class="tag-moderate">Problem Solving</span><span class="tag-moderate">Communication</span>'
        st.markdown(f'<div>{soft_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 5: AI SKILL GAP ANALYSIS
# ---------------------------------------------------------
elif nav_module == "📊 Skill Gap Analysis":
    st.markdown("## 📊 Comprehensive Skill Gap Matrix")
    st.markdown(f"Comparing candidate resume skills against target job requirements for **{jd_eval['title']}**.")
    
    col_sg1, col_sg2, col_sg3 = st.columns(3)
    
    with col_sg1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### 🟢 Strong Skills ({gap_eval['strong_count']})")
        st.caption("Exact skill verified on resume")
        for item in gap_eval["strong_skills"]:
            st.markdown(f"- <span class='tag-strong'>{item['skill']}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_sg2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### 🟡 Moderate Skills ({gap_eval['moderate_count']})")
        st.caption("Foundational match via related tools")
        for item in gap_eval["moderate_skills"]:
            st.markdown(f"- <span class='tag-moderate'>{item['skill']}</span><br><small style='color:#94A3B8;'>{item['reason']}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_sg3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### 🔴 Missing Skills ({gap_eval['missing_count']})")
        st.caption("High-priority skills to acquire")
        for item in gap_eval["missing_skills"]:
            st.markdown(f"- <span class='tag-missing'>{item['skill']}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 6: PERSONALIZED AI ROADMAP
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
# MODULE 7: AI PROJECT RECOMMENDER
# ---------------------------------------------------------
elif nav_module == "💡 AI Project Recommender":
    st.markdown("## 💡 AI Portfolio Project Recommender")
    st.markdown("Recommended portfolio projects designed to demonstrate your target missing skills to employers.")
    
    recommended_projs = recommend_projects_for_student(gap_eval["missing_skills"], gap_eval["moderate_skills"], jd_eval["title"])
    
    for p in recommended_projs:
        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; color:#F8FAFC;">🚀 {p['title']}</h3>
                <span class="tag-bonus" style="background:rgba(59,130,246,0.3); color:#60A5FA;">{p['difficulty']}</span>
            </div>
            <p style="color:#CBD5E1; font-size:1.05rem; margin-top:12px;">{p['description']}</p>
            <p style="margin-bottom:0;"><strong>🛠️ Tech Stack Specs:</strong> <code>{" , ".join(p['tech_stack'])}</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📐 View Implementation & Architecture Blueprint for '{p['title'][:35]}...'"):
            st.markdown("#### Step-by-Step Architecture Steps:")
            for step_i, step_txt in enumerate(p["architecture_steps"], 1):
                st.markdown(f"**Step {step_i}:** {step_txt}")

# ---------------------------------------------------------
# MODULE 8: AI MOCK INTERVIEW COACH
# ---------------------------------------------------------
elif nav_module == "🎤 AI Mock Interview Coach":
    st.markdown("## 🎤 AI Mock Interview Coach")
    st.markdown(f"Practice role-specific interview questions for **{jd_eval['title']}** and get instant scoring & feedback.")
    
    questions = get_questions_for_role(jd_eval["title"])
    
    selected_q_idx = st.selectbox("Select Question to Practice:", range(len(questions)), format_func=lambda i: f"Q{i+1}: [{questions[i]['category']}] {questions[i]['question'][:60]}...")
    
    q_curr = questions[selected_q_idx]
    
    st.markdown(f"""
    <div class="glass-card" style="border-left: 6px solid #38BDF8;">
        <h4 style="margin:0; color:#38BDF8;">Category: {q_curr['category']}</h4>
        <h3 style="margin-top:8px; color:#F8FAFC;">{q_curr['question']}</h3>
        <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;"><em>Evaluates: {q_curr['rubric']}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    student_ans = st.text_area("✍️ Type your detailed answer here:", height=160, placeholder="Explain your answer using STAR technique or technical concepts...")
    
    if st.button("🚀 Evaluate Answer with AI Coach", type="primary"):
        if student_ans.strip():
            eval_res = evaluate_student_answer(q_curr, student_ans)
            
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="margin:0;">AI Score: <strong>{eval_res['score']} / 10</strong> ({eval_res['rating']})</h3>
            </div>
            """, unsafe_allow_html=True)
            st.progress(eval_res['score'] / 10)
            
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.success("✅ **Strengths Identified:**")
                for s in eval_res["strengths"]:
                    st.markdown(f"- {s}")
                st.markdown('</div>', unsafe_allow_html=True)
            with e_col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.warning("💡 **Improvement Feedback:**")
                for imp in eval_res["improvements"]:
                    st.markdown(f"- {imp}")
                st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 9: AI CAREER ASSISTANT
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
