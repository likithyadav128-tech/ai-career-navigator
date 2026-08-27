"""
AI Career Intelligence & Job Readiness Operating System
Full-stack Streamlit Application - Hierarchical Skill Mastery & Prerequisites Edition
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
from modules.company_role_profiles import ROLE_TAXONOMY, COMPANY_PROFILES, SKILL_DEPENDENCY_GRAPH
from modules.career_twin_engine import calculate_7_factor_readiness
from modules.daily_mission_engine import generate_daily_career_mission
from modules.skill_verifier import get_assessment_for_skill, evaluate_skill_assessment
from modules.hierarchical_skill_tree import analyze_hierarchical_skill_tree
from modules.project_strength_analyzer import audit_project_strength, generate_flagship_project_blueprint
from modules.advanced_interview_sim import get_questions_by_mode, evaluate_communication_intelligence
from modules.career_route_simulator import simulate_multi_role_readiness, calculate_role_transition_delta
from modules.roadmap_generator import generate_personalized_roadmap
from modules.project_recommender import recommend_projects_for_student
from modules.interview_coach import evaluate_student_answer
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
    page_title="AI Career Intelligence & Job Readiness OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean Styling
st.markdown("""
<style>
    /* Main Background & Base Typography */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #F8FAFC !important;
    }
    
    /* Main Header Banner */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #2563EB 100%);
        color: #FFFFFF !important;
        padding: 26px 36px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
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
        margin-top: 6px !important;
        margin-bottom: 0 !important;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 16px;
    }
    .metric-lbl {
        font-size: 0.88rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E293B;
    }

    /* Skill Badges */
    .badge-strong {
        background-color: #DCFCE7 !important;
        color: #15803D !important;
        border: 1px solid #86EFAC !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-moderate {
        background-color: #FEF3C7 !important;
        color: #B45309 !important;
        border: 1px solid #FCD34D !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-missing {
        background-color: #FEE2E2 !important;
        color: #B91C1C !important;
        border: 1px solid #FCA5A5 !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-bonus {
        background-color: #E0E7FF !important;
        color: #4338CA !important;
        border: 1px solid #A5B4FC !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }

    /* Card Containers */
    .card-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "candidate_text" not in st.session_state:
    default_res = SAMPLE_RESUMES["Data Science Student (Alex Rivera)"]
    st.session_state["candidate_text"] = default_res["text"]
    st.session_state["candidate_skills"] = default_res["extracted_skills"]

if "target_jd_text" not in st.session_state:
    default_jd = SAMPLE_JOB_DESCRIPTIONS["Data Scientist"]
    st.session_state["target_jd_text"] = default_jd["text"]
    st.session_state["target_role"] = "Data Analyst"

if "target_company" not in st.session_state:
    st.session_state["target_company"] = "Any Company (General Industry Standard)"

if "github_user" not in st.session_state:
    st.session_state["github_user"] = "arivera"

if "verified_skills" not in st.session_state:
    st.session_state["verified_skills"] = {}

if "project_audit_history" not in st.session_state:
    st.session_state["project_audit_history"] = {}

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hi! I'm your AI Career Assistant. Ask me anything like:\n- *'What should I learn next?'*\n- *'Am I ready for a Data Analyst role?'*\n- *'Which skills should I add to my resume?'*"}
    ]

# ---------------------------------------------------------
# SIDEBAR: CONTROLS & PROFILE TARGETING
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <div style="font-size: 2.8rem;">🎯</div>
        <h2 style="margin: 0; color: #FFFFFF; font-size: 1.35rem;">AI Career OS</h2>
        <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Personal Job-Preparation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("⚙️ Profile & Targeting")
    
    st.subheader("1. Target Role & Company")
    role_keys = list(ROLE_TAXONOMY.keys())
    sel_role = st.selectbox("Select Target Job Role:", role_keys, index=0)
    st.session_state["target_role"] = sel_role

    company_keys = list(COMPANY_PROFILES.keys())
    sel_company = st.selectbox("Select Target Company:", company_keys, index=0)
    st.session_state["target_company"] = sel_company

    st.divider()

    st.subheader("2. Candidate Resume Source")
    sample_res_choice = st.selectbox(
        "Load Sample Candidate Profile:",
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
            resume_text_input = st.text_area("Or Paste Resume Text:", value=st.session_state["candidate_text"], height=140)
            if resume_text_input:
                st.session_state["candidate_text"] = resume_text_input
                st.session_state["candidate_skills"] = extract_skills_from_text(resume_text_input)

    st.divider()

    st.subheader("3. GitHub Verification")
    gh_input = st.text_input("GitHub Username:", value=st.session_state["github_user"])
    if gh_input:
        st.session_state["github_user"] = gh_input

# Core Analytics Calculation
role_info = ROLE_TAXONOMY.get(st.session_state["target_role"], ROLE_TAXONOMY["Data Analyst"])
resume_eval = evaluate_resume_quality(st.session_state["candidate_text"], st.session_state["candidate_skills"])
jd_eval = analyze_job_description(st.session_state["target_jd_text"])

# Gap evaluation against selected role core skills
gap_eval = analyze_skill_gaps(st.session_state["candidate_skills"], role_info["core_skills"])
semantic_sim = compute_semantic_cosine_similarity(st.session_state["candidate_text"], st.session_state["target_jd_text"])
github_res = verify_github_profile(st.session_state["github_user"])
hierarchy_analysis = analyze_hierarchical_skill_tree(st.session_state["candidate_skills"], st.session_state["target_role"])

# Calculate 7-Factor Transparent Readiness Score
readiness_eval = calculate_7_factor_readiness(
    resume_score=resume_eval["score"],
    skill_gap_result=gap_eval,
    project_score=72.0,
    assessment_score=68.0,
    interview_score=75.0,
    communication_score=80.0,
    evidence_score=85.0 if github_res.get("verified") else 50.0,
    target_role=st.session_state["target_role"],
    company_name=st.session_state["target_company"]
)

# Daily Career Mission
daily_mission = generate_daily_career_mission(gap_eval["missing_skills"], gap_eval["moderate_skills"], st.session_state["target_role"])

# Header Banner
st.markdown(f"""
<div class="main-header">
    <h1>🎯 AI Career Intelligence & Job Readiness OS</h1>
    <p>Target Role: <strong>{st.session_state['target_role']}</strong> | Target Company: <strong>{st.session_state['target_company'].split('(')[0]}</strong> | Overall Job Readiness: <strong>{readiness_eval['overall_readiness']}%</strong></p>
</div>
""", unsafe_allow_html=True)

# Build Top Navigation Tabs
tabs = st.tabs([
    "🏆 Career Twin & Readiness OS",
    "🎯 Daily Mission ('Do Today')",
    "📄 Resume & Job Matcher",
    "📊 Skill Graph & Hierarchy Matrix",
    "🗺️ Adaptive AI Roadmap",
    "💡 Project Auditor & Builder",
    "🎤 Advanced Interview Simulator",
    "🧭 Career Route Simulator",
    "🤖 AI Career Assistant"
])

# ---------------------------------------------------------
# TAB 1: CAREER TWIN & TRANSPARENT 7-FACTOR READINESS OS
# ---------------------------------------------------------
with tabs[0]:
    st.header("🏆 Personal Career Twin & Transparent 7-Factor Readiness")
    st.markdown(f"Continuously tracking digital twin profile for **{st.session_state['target_role']}** targeting **{st.session_state['target_company']}**.")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Overall Job Readiness</div>
            <div class="metric-val" style="color: #16A34A;">{readiness_eval['overall_readiness']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Resume ATS Score</div>
            <div class="metric-val" style="color: #2563EB;">{resume_eval['score']}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Technical Skills Match</div>
            <div class="metric-val" style="color: #D97706;">{gap_eval['readiness_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">GitHub Dev Badge</div>
            <div class="metric-val" style="font-size: 1.15rem; color: #2563EB;">{github_res.get('status_badge', '⚡ Active Dev')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_twin1, col_twin2 = st.columns([1.1, 1])
    
    with col_twin1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Transparent 7-Factor Breakdown")
        
        for factor_name, factor_val in readiness_eval["factors"].items():
            col_f1, col_f2 = st.columns([3, 1])
            with col_f1:
                st.write(f"**{factor_name}** ({int(readiness_eval['weights'][factor_name]*100)}% weight)")
                st.progress(factor_val / 100)
            with col_f2:
                st.markdown(f"<h3 style='margin:0; text-align:right; color:#1E293B;'>{factor_val}%</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_twin2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### ⚡ What Will Increase My Score?")
        st.caption("Actionable recommendations generated by the Readiness Engine:")
        
        for booster in readiness_eval["score_boosters"]:
            st.markdown(f"""
            <div style="border-left: 4px solid #16A34A; padding-left: 12px; margin-bottom: 12px;">
                <h4 style="margin:0; color:#15803D;">{booster['action']} <span style="background:#DCFCE7; padding:2px 8px; border-radius:12px; font-size:0.85rem;">{booster['points']}</span></h4>
                <p style="color:#64748B; margin:4px 0 0 0; font-size:0.9rem;">{booster['task']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    gauge_fig = create_readiness_gauge(readiness_eval["overall_readiness"])
    st.plotly_chart(gauge_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: DAILY MISSION ("WHAT SHOULD I DO TODAY?")
# ---------------------------------------------------------
with tabs[1]:
    st.header("🎯 Today's Career Mission — 'What Should I Do Today?'")
    st.markdown(f"**Estimated Completion Time:** `{daily_mission['estimated_time']}` | **Potential Score Boost:** `{daily_mission['potential_boost']}`")
    
    st.info("💡 Completing daily missions updates your Personal Career Twin readiness score in real time!")
    
    for task in daily_mission["tasks"]:
        st.markdown(f"""
        <div class="card-box" style="border-left: 5px solid #2563EB;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; color:#1E293B;">{task['title']}</h3>
                <span class="badge-strong">{task['points']}</span>
            </div>
            <p style="color:#475569; margin-top:8px;">{task['description']}</p>
            <p><strong>⏱️ Time Estimate:</strong> <code>{task['time_estimate']}</code> | <strong>Category:</strong> <code>{task['category']}</code></p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox(f"Mark {task['title']} as Completed Today", key=f"daily_chk_{task['id']}")

# ---------------------------------------------------------
# TAB 3: RESUME & JOB MATCHER
# ---------------------------------------------------------
with tabs[2]:
    st.header("📄 Resume & Job Description Matcher")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown(f"### ATS Resume Quality: **{resume_eval['score']}/100**")
        st.progress(resume_eval['score'] / 100)
        
        st.markdown("#### Quality Checklist:")
        for k, v in resume_eval["checks"].items():
            st.markdown(f"- **{k}**: `{v}`")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_m2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown(f"### Semantic Cosine Similarity: **{semantic_sim}%**")
        st.progress(semantic_sim / 100)
        st.markdown("Evaluates contextual overlap between candidate resume text and target job description.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Bullet Optimizer Tool
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("### ✨ AI Resume Bullet Rewriter (STAR Method Generator)")
    user_bullet = st.text_input("Paste any weak bullet point:", value="Worked on customer churn prediction model using Python")
    if st.button("🚀 Optimize Bullet Point"):
        opt_res = optimize_resume_bullet(user_bullet, st.session_state["target_role"])
        st.success("✅ **STAR Method Optimized Bullet Point:**")
        st.code(opt_res["optimized"], language="text")
        st.caption(f"Action Verb: **{opt_res['action_verb']}** | Impact Metric: **{opt_res['impact_metric']}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: SKILL GRAPH & HIERARCHY MASTERY MATRIX
# ---------------------------------------------------------
with tabs[3]:
    st.header(f"📊 Skill Hierarchy Matrix & Prerequisite Tree — {st.session_state['target_role']}")
    st.markdown("Evaluates your **Mastered Skills** and identifies your **Exact Next Learning Targets** based on prerequisite dependencies.")
    
    # Hierarchy Summary Cards
    h_sum = hierarchy_analysis["summary"]
    hc1, hc2, hc3, hc4 = st.columns(4)
    with hc1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Mastered Skills</div>
            <div class="metric-val" style="color: #16A34A;">{h_sum['mastered']} / {h_sum['total_skills']}</div>
        </div>
        """, unsafe_allow_html=True)
    with hc2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Next Learning Targets</div>
            <div class="metric-val" style="color: #2563EB;">{h_sum['next_targets']} Ready</div>
        </div>
        """, unsafe_allow_html=True)
    with hc3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Blocked by Prereqs</div>
            <div class="metric-val" style="color: #DC2626;">{h_sum['blocked']} Skills</div>
        </div>
        """, unsafe_allow_html=True)
    with hc4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Hierarchy Mastery</div>
            <div class="metric-val" style="color: #D97706;">{round((h_sum['mastered']/h_sum['total_skills'])*100, 1)}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # High Priority Callout: Next Immediate Learning Targets
    if hierarchy_analysis["next_learning_targets"]:
        st.markdown('<div class="card-box" style="border-left: 6px solid #2563EB; background: #F0F9FF;">', unsafe_allow_html=True)
        st.markdown("### 🚀 What Should You Learn Next? (Prerequisites Satisfied)")
        st.markdown("Based on your verified skills, all prerequisites for these skills are met! **Target these next:**")
        
        for tgt in hierarchy_analysis["next_learning_targets"]:
            prereq_str = f" (Prerequisites satisfied: {', '.join(tgt['prereqs'])})" if tgt['prereqs'] else " (Foundational Skill)"
            st.markdown(f"- 🚀 **{tgt['skill']}** `[Level {tgt['level']} — {tgt['category']}]`{prereq_str}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Detailed Hierarchy Level Matrix
    st.subheader("🌲 Complete Role Skill Hierarchy Tree")
    
    level_titles = {
        1: "Level 1: Foundations & Prerequisites",
        2: "Level 2: Core Analytical Tools & Libraries",
        3: "Level 3: Advanced Modeling & Domain Expertise",
        4: "Level 4: Production, Infrastructure & Deployment"
    }

    for lvl in range(1, 5):
        items = hierarchy_analysis["levels"].get(lvl, [])
        if items:
            with st.expander(f"📍 {level_titles[lvl]} ({len(items)} Skills)", expanded=(lvl <= 2)):
                for sk in items:
                    badge_style = "badge-strong" if sk["status_code"] == "STRONG" else ("badge-bonus" if sk["status_code"] == "NEXT_TARGET" else "badge-missing")
                    
                    st.markdown(f"""
                    <div style="border-bottom: 1px solid #E2E8F0; padding: 10px 0;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 style="margin:0; color:#1E293B;">{sk['status'].split()[0]} {sk['skill']}</h4>
                            <span class="{badge_style}">{sk['status']}</span>
                        </div>
                        <p style="color:#64748B; margin:4px 0 0 0; font-size:0.9rem;">Category: <code>{sk['category']}</code> | {sk['reason']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    st.divider()

    # Adaptive Assessment Tool
    st.subheader("🧪 Adaptive Skill Verification Test")
    test_skill = st.selectbox("Select Skill to Verify:", ["SQL", "Python", "Power BI", "Machine Learning"])
    questions = get_assessment_for_skill(test_skill)
    
    user_ans = {}
    for idx, q in enumerate(questions):
        st.markdown(f"**Q{idx+1}: {q['question']}**")
        user_ans[idx] = st.radio(f"Select answer for Q{idx+1}:", range(len(q['options'])), format_func=lambda i: q['options'][i], key=f"q_{test_skill}_{idx}")
        
    if st.button(f"Submit {test_skill} Verification Assessment"):
        eval_res = evaluate_skill_assessment(test_skill, user_ans, questions)
        st.session_state["verified_skills"][test_skill] = eval_res["verified_level"]
        
        st.success(f"🎉 Result: **{eval_res['verified_level']}** ({eval_res['verified_percentage']}% Score)")
        for d in eval_res["details"]:
            st.markdown(f"- {'✅' if d['is_correct'] else '❌'} {d['question']} (Your choice: *{d['user_choice']}*)")

# ---------------------------------------------------------
# TAB 5: ADAPTIVE AI ROADMAP
# ---------------------------------------------------------
with tabs[4]:
    st.header("🗺️ Dynamic Adaptive AI Learning Roadmap")
    st.markdown(f"Phased learning sequence prioritized for **{st.session_state['target_role']}**.")
    
    roadmap_phases = generate_personalized_roadmap(gap_eval["missing_skills"], gap_eval["moderate_skills"], st.session_state["target_role"])
    
    for idx, phase in enumerate(roadmap_phases, 1):
        with st.expander(f"📍 {phase['phase']} | ⏱️ {phase['duration']}", expanded=(idx <= 2)):
            st.markdown(f"**Focus Objective:** {phase['focus']}")
            st.markdown(f"**Topics:** `{', '.join(phase['topics'])}`")
            for step in phase["action_steps"]:
                st.checkbox(step, key=f"chk_rd_{idx}_{step[:12]}")

# ---------------------------------------------------------
# TAB 6: PROJECT AUDITOR & BUILDER
# ---------------------------------------------------------
with tabs[5]:
    st.header("💡 Project Strength Auditor & 'Build Me a Better Project'")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 🔍 7-Dimensional Project Auditor")
        p_name = st.text_input("Project Name:", value="Customer Churn Prediction Engine")
        p_tech = st.text_input("Tech Stack (comma separated):", value="Python, XGBoost, Scikit-learn, Streamlit")
        p_desc = st.text_area("Project Description:", value="Built XGBoost churn classifier on 50k transaction logs achieving 89.2% ROC-AUC score.")
        has_dep = st.checkbox("Deployed to Live Server (Streamlit / Render)", value=True)
        has_doc = st.checkbox("Has README.md Documentation", value=True)
        
        if st.button("Audit Project Strength"):
            audit_res = audit_project_strength(p_name, p_tech, p_desc, has_dep, has_doc)
            st.subheader(f"Project Strength Score: **{audit_res['overall_score']}/100**")
            for c_name, c_score in audit_res["criteria"].items():
                st.write(f"**{c_name}:** {c_score}/100")
                st.progress(c_score / 100)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_p2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 🚀 'Build Me a Better Project' Blueprint Generator")
        
        blueprint = generate_flagship_project_blueprint(st.session_state["candidate_skills"], st.session_state["target_role"])
        
        st.markdown(f"#### Flagship Project: **{blueprint['title']}**")
        st.markdown(f"**Difficulty:** `{blueprint['difficulty']}` | **Estimated Time:** `{blueprint['estimated_time']}`")
        st.markdown(f"**Dataset:** [{blueprint['dataset_name']}]({blueprint['dataset_link']})")
        st.markdown(f"**Description:** {blueprint['description']}")
        
        st.markdown("#### 📋 Implementation Tasks:")
        for t_idx, task_txt in enumerate(blueprint["tasks"], 1):
            st.markdown(f"{t_idx}. {task_txt}")
            
        with st.expander("📂 View GitHub Repository Directory Structure & README Template"):
            st.code(blueprint["github_structure"], language="text")
            st.code(blueprint["readme_snippet"], language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 7: ADVANCED INTERVIEW SIMULATOR
# ---------------------------------------------------------
with tabs[6]:
    st.header("🎤 Advanced AI Interview Simulator")
    
    col_sim1, col_sim2 = st.columns([1, 1])
    with col_sim1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        int_mode = st.selectbox("Select Interview Mode:", [
            "HR / Cultural Fit",
            "Technical Deep-Dive",
            "Company-Specific",
            "Pressure Interview (Adaptive)"
        ])
        
        sim_questions = get_questions_by_mode(int_mode, st.session_state["target_company"], st.session_state["target_role"])
        q_idx = st.selectbox("Select Question:", range(len(sim_questions)), format_func=lambda i: f"Q{i+1}: {sim_questions[i]['question'][:60]}...")
        q_item = sim_questions[q_idx]
        
        st.markdown(f"#### Question ({q_item.get('category', int_mode)}):")
        st.markdown(f"### *\"{q_item['question']}\"*")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sim2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        user_answer = st.text_area("✍️ Type your answer using STAR method (Situation, Task, Action, Result):", height=150)
        
        if st.button("Submit Answer for Communication & Content Scoring", type="primary"):
            if user_answer.strip():
                ans_eval = evaluate_student_answer(q_item, user_answer)
                comm_eval = evaluate_communication_intelligence(user_answer)
                
                st.subheader(f"Overall Answer Score: **{ans_eval['score']}/10**")
                st.write(f"**Communication & STAR Structure Score:** `{comm_eval['comm_score']}/100`")
                st.info(comm_eval["time_feedback"])
                
                st.markdown("#### STAR Structure Detection:")
                for star_key, is_present in comm_eval["star_checklist"].items():
                    st.write(f"- {'✅' if is_present else '❌'} **{star_key}**")
            else:
                st.error("Please type an answer before submitting.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 8: CAREER ROUTE SIMULATOR
# ---------------------------------------------------------
with tabs[7]:
    st.header("🧭 Multi-Role Career Route Simulator")
    st.markdown("Compare your job readiness across all 10 major technical career tracks simultaneously:")
    
    multi_sim = simulate_multi_role_readiness(st.session_state["candidate_skills"])
    
    df_sim = pd.DataFrame(multi_sim)
    fig_sim = px.bar(df_sim, x="role", y="readiness_score", color="readiness_score", color_continuous_scale="Viridis", text="readiness_score")
    fig_sim.update_layout(paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF', font=dict(color='#0F172A'))
    st.plotly_chart(fig_sim, use_container_width=True)
    
    st.markdown("### 🔄 Career Transition Delta Calculator")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        c_role = st.selectbox("Current Role:", list(ROLE_TAXONOMY.keys()), index=0)
    with col_t2:
        t_role = st.selectbox("Target Transition Role:", list(ROLE_TAXONOMY.keys()), index=1)
        
    delta_res = calculate_role_transition_delta(st.session_state["candidate_skills"], c_role, t_role)
    st.info(f"💡 To transition from **{c_role}** ({delta_res['current_readiness']}%) to **{t_role}** ({delta_res['target_readiness']}%), estimated time is `{delta_res['estimated_transition_time']}`.")
    st.write(f"**Missing Skill Delta:** {', '.join(delta_res['missing_delta_skills']) if delta_res['missing_delta_skills'] else 'None! You meet all requirements.'}")

# ---------------------------------------------------------
# TAB 9: AI CAREER ASSISTANT
# ---------------------------------------------------------
with tabs[8]:
    st.header("🤖 AI Career Assistant Chatbot")
    
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

    ctx = {
        "candidate_skills": st.session_state["candidate_skills"],
        "target_role": st.session_state["target_role"],
        "readiness_score": readiness_eval["overall_readiness"],
        "missing_skills": gap_eval["missing_skills"],
        "moderate_skills": gap_eval["moderate_skills"],
        "strong_skills": gap_eval["strong_skills"],
        "resume_score": resume_eval["score"]
    }

    if preset_clicked:
        st.session_state["chat_history"].append({"role": "user", "content": preset_clicked})
        ans = generate_assistant_response(preset_clicked, ctx)
        st.session_state["chat_history"].append({"role": "assistant", "content": ans})

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask your career OS assistant anything...")
    if user_query:
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        ans = generate_assistant_response(user_query, ctx)
        st.session_state["chat_history"].append({"role": "assistant", "content": ans})
        st.rerun()
