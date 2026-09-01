"""
AI Career Navigator - Production Main Application
Modular, responsive, multi-tenant career operating system with dark/light themes.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Configuration and Global Taxonomies
from config import APP_NAME, APP_TAGLINE, APP_VERSION, CAREER_TRACKS, PRODUCT_JOURNEY

# Database & Persistence Repositories
from database import (
    init_all_tables, register_user, authenticate_user, reset_user_password,
    save_user_profile, load_user_profile, save_onboarding_data, load_onboarding_data,
    save_task_completion, load_user_roadmap_progress,
    add_application, update_application_status, get_user_applications, delete_application,
    save_user_portfolio, get_user_portfolio, get_public_portfolio_by_username,
    add_notification, get_user_notifications
)

# Services Layer
from services import (
    AuthService, CareerMatchingService, CareerComparisonService,
    SkillGapService, RoadmapService, LearningHubService,
    ProjectService, ResumeService, CopilotService,
    InterviewService, ReadinessService, ApplicationService
)

# Reusable UI Components
from components import (
    render_metric_card, render_next_best_action_card, render_section_header,
    render_top_navbar, render_app_sidebar, render_public_landing_page,
    render_onboarding_wizard, render_theme_gauge, render_theme_radar,
    render_career_bar_chart, render_notifications_panel
)

# Legacy / Algorithm Engine Modules
from modules.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
from modules.resume_analyzer import SKILL_TAXONOMY, extract_skills_from_text, extract_text_from_pdf, evaluate_resume_quality
from modules.job_analyzer import analyze_job_description
from modules.skill_gap_engine import analyze_skill_gaps
from modules.company_role_profiles import ROLE_TAXONOMY, COMPANY_PROFILES
from modules.daily_mission_engine import generate_daily_career_mission
from modules.skill_verifier import get_assessment_for_skill, evaluate_skill_assessment
from modules.github_verifier import verify_github_profile
from modules.semantic_matcher import compute_semantic_cosine_similarity, optimize_resume_bullet

# 1. Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} — AI Career OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Global CSS & Theme Engine (Dark / Light Theme Tokens)
app_theme = st.session_state.get("app_theme", "dark")

if app_theme == "light":
    theme_css = """
    :root {
        --bg-main: #F8FAFC;
        --card-bg: #FFFFFF;
        --card-border: rgba(99, 102, 241, 0.2);
        --text-main: #0F172A;
        --text-muted: #64748B;
        --text-sub: #475569;
        --sidebar-bg: #F1F5F9;
    }
    .stApp {
        background: #F8FAFC !important;
        color: #0F172A !important;
    }
    [data-testid="stSidebar"] {
        background: #F1F5F9 !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15) !important;
    }
    """
else:
    theme_css = """
    :root {
        --bg-main: #070913;
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(99, 102, 241, 0.2);
        --text-main: #FFFFFF;
        --text-muted: #94A3B8;
        --text-sub: #64748B;
        --sidebar-bg: linear-gradient(180deg, #0C1022 0%, #111827 100%);
    }
    .stApp {
        background: radial-gradient(circle at 75% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
                    radial-gradient(circle at 20% 80%, rgba(236, 72, 153, 0.08) 0%, transparent 40%),
                    linear-gradient(145deg, #070913 0%, #0C1022 50%, #0A0D1A 100%) !important;
        color: #E2E8F0 !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C1022 0%, #111827 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15) !important;
    }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    {theme_css}

    /* Container Spacing */
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1320px !important;
        margin: 0 auto !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0px !important;
    }}

    /* Global Input Overrides */
    div[data-baseweb="select"] > div {{
        background: rgba(255,255,255,0.04) !important;
        color: inherit !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 12px !important;
    }}
    textarea, input[type="text"], input[type="password"] {{
        background: rgba(255,255,255,0.04) !important;
        color: inherit !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
    }}
    textarea:focus, input:focus {{
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }}

    /* Badges */
    .badge-strong {{
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34D399 !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }}
    .badge-moderate {{
        background: rgba(245, 158, 11, 0.15) !important;
        color: #FBBF24 !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }}
    .badge-missing {{
        background: rgba(239, 68, 68, 0.15) !important;
        color: #F87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }}
    .badge-target {{
        background: rgba(99, 102, 241, 0.2) !important;
        color: #A5B4FC !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }}

    /* Glass Content Boxes */
    .glass-box {{
        background: var(--card-bg, rgba(255, 255, 255, 0.03));
        border: 1px solid var(--card-border, rgba(99, 102, 241, 0.18));
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    }}
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None

if "active_view" not in st.session_state:
    st.session_state["active_view"] = "landing" if not st.session_state["logged_in"] else "nav_dashboard"

if "candidate_text" not in st.session_state:
    def_res = SAMPLE_RESUMES["Data Science Student (Alex Rivera)"]
    st.session_state["candidate_text"] = def_res["text"]
    st.session_state["candidate_skills"] = list(def_res["extracted_skills"])

if "target_role" not in st.session_state:
    st.session_state["target_role"] = "Data Analyst"

if "target_company" not in st.session_state:
    st.session_state["target_company"] = "Any Company (General Industry Standard)"

if "target_jd_text" not in st.session_state:
    st.session_state["target_jd_text"] = SAMPLE_JOB_DESCRIPTIONS["Data Scientist"]["text"]

if "github_user" not in st.session_state:
    st.session_state["github_user"] = "arivera"

if "verified_skills" not in st.session_state:
    st.session_state["verified_skills"] = {}

if "verified_skills_scores" not in st.session_state:
    st.session_state["verified_skills_scores"] = {}

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hi! I'm your AI Career Copilot. Ask me anything like:\n- *'What should I learn next?'*\n- *'Am I ready for a Data Analyst role?'*\n- *'Give me an industry-grade portfolio project idea.'*"}
    ]

# 4. Handle Public Shareable Portfolio View (e.g. ?portfolio=username)
query_params = st.query_params
if "portfolio" in query_params:
    target_username = query_params["portfolio"]
    public_prof = get_public_portfolio_by_username(target_username)
    if public_prof:
        if public_prof.get("is_private"):
            st.warning(f"🔒 The portfolio for '{public_prof['full_name']}' is currently set to private.")
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%); border: 1px solid rgba(139,92,246,0.3); border-radius: 24px; padding: 40px 32px; margin-bottom: 24px;">
                <div style="font-size:3rem; margin-bottom:10px;">👤</div>
                <h1 style="color:#FFF !important; margin:0 0 6px 0;">{public_prof['full_name']}</h1>
                <h3 style="color:#A78BFA !important; margin:0 0 12px 0;">{public_prof['headline']}</h3>
                <p style="color:#CBD5E1; font-size:1.05rem; max-width:700px; line-height:1.6;">{public_prof['bio']}</p>
                <div style="display:flex; gap:14px; margin-top:16px;">
                    {'<a href="' + public_prof['github_url'] + '" target="_blank" style="color:#818CF8; font-weight:700; text-decoration:none;">GitHub ↗</a>' if public_prof['github_url'] else ''}
                    {'<a href="' + public_prof['linkedin_url'] + '" target="_blank" style="color:#818CF8; font-weight:700; text-decoration:none;">LinkedIn ↗</a>' if public_prof['linkedin_url'] else ''}
                    {'<a href="' + public_prof['portfolio_url'] + '" target="_blank" style="color:#818CF8; font-weight:700; text-decoration:none;">Website ↗</a>' if public_prof['portfolio_url'] else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Verified Technical Skills")
            for sk in public_prof["skills"]:
                st.markdown(f"<span class='badge-strong'>✓ {sk}</span>", unsafe_allow_html=True)
                
            st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
            st.info(f"Verified Job Readiness Benchmark: **{public_prof['readiness_score']}% Ready for {public_prof['target_role']}**")
        st.stop()

# 5. Routing Logic: Public Landing Page vs Auth vs Authenticated Dashboard
if not st.session_state["logged_in"]:
    if st.session_state.get("active_view") == "auth":
        # Render Dedicated Authentication Modal
        col_b1, col_b2, col_b3 = st.columns([1, 1.4, 1])
        with col_b2:
            st.markdown(f"""
            <div style="text-align:center; margin-bottom: 20px;">
                <div style="width:44px; height:44px; border-radius:12px; background: linear-gradient(135deg, #6366F1, #A855F7); display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto;">
                    <span style="color:#FFF; font-weight:900; font-size:1.2rem;">A✦</span>
                </div>
                <h2 style="margin:0; color:#FFF;">{APP_NAME}</h2>
                <p style="color:#94A3B8; font-size:0.9rem;">Sign in or create your workspace</p>
            </div>
            """, unsafe_allow_html=True)

            auth_tab1, auth_tab2, auth_tab3 = st.tabs(["Sign In", "Create Account", "Reset Password"])
            
            with auth_tab1:
                st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                l_user = st.text_input("Username / Email:", key="auth_l_user", placeholder="Enter username")
                l_pass = st.text_input("Password:", type="password", key="auth_l_pass", placeholder="Enter password")
                if st.button("➔ Sign In", type="primary", use_container_width=True):
                    auth_res = AuthService.sign_in(l_user, l_pass)
                    if auth_res["success"]:
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = auth_res
                        prof = auth_res.get("profile", {})
                        if prof and prof.get("has_profile"):
                            st.session_state["target_role"] = prof["target_role"]
                            st.session_state["target_company"] = prof["target_company"]
                            st.session_state["candidate_text"] = prof["candidate_text"]
                            st.session_state["candidate_skills"] = prof["candidate_skills"]
                            st.session_state["github_user"] = prof.get("github_user", "arivera")
                        st.session_state["active_view"] = "nav_dashboard"
                        st.rerun()
                    else:
                        st.error(auth_res["message"])

                st.divider()
                st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#94A3B8; margin-bottom:8px;'>QUICK 1-CLICK DEMO ACCESS:</div>", unsafe_allow_html=True)
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    if st.button("🔴 Alex (Data Science)", use_container_width=True):
                        auth_res = AuthService.sign_in("alex_rivera", "demo123")
                        if not auth_res["success"]:
                            AuthService.sign_up("alex_rivera", "demo123", "Alex Rivera", "United States")
                            auth_res = AuthService.sign_in("alex_rivera", "demo123")
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = auth_res
                        st.session_state["active_view"] = "nav_dashboard"
                        st.rerun()
                with col_d2:
                    if st.button("🔵 Sam (Full-Stack)", use_container_width=True):
                        auth_res = AuthService.sign_in("sam_chen", "demo123")
                        if not auth_res["success"]:
                            AuthService.sign_up("sam_chen", "demo123", "Sam Chen", "Canada")
                            auth_res = AuthService.sign_in("sam_chen", "demo123")
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = auth_res
                        st.session_state["target_role"] = "Software Engineer (Full-Stack)"
                        st.session_state["active_view"] = "nav_dashboard"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with auth_tab2:
                st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                r_name = st.text_input("Full Name:", key="auth_r_name", placeholder="e.g. Likith Yadav")
                r_user = st.text_input("Choose Username:", key="auth_r_user", placeholder="e.g. likith_dev")
                r_pass = st.text_input("Choose Password:", type="password", key="auth_r_pass", placeholder="At least 6 characters")
                if st.button("➔ Create Account & Begin Setup", type="primary", use_container_width=True):
                    reg_res = AuthService.sign_up(r_user, r_pass, r_name)
                    if reg_res["success"]:
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = reg_res
                        st.session_state["onboarding_step"] = 1
                        st.session_state["active_view"] = "onboarding"
                        st.rerun()
                    else:
                        st.error(reg_res["message"])
                st.markdown('</div>', unsafe_allow_html=True)

            with auth_tab3:
                st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                rst_user = st.text_input("Enter Username:", key="auth_rst_user")
                rst_pass = st.text_input("Enter New Password:", type="password", key="auth_rst_pass")
                if st.button("Reset Password", use_container_width=True):
                    rst_res = AuthService.reset_password(rst_user, rst_pass)
                    if rst_res["success"]:
                        st.success(rst_res["message"])
                    else:
                        st.error(rst_res["message"])
                st.markdown('</div>', unsafe_allow_html=True)

            if st.button("⬅ Back to Home", key="btn_back_home"):
                st.session_state["active_view"] = "landing"
                st.rerun()

        st.stop()
    else:
        # Render Public Startup Landing Page
        render_public_landing_page()
        st.stop()

# 6. Authenticated User Flow
user_info = st.session_state["user_info"]

# Check if onboarding is needed
onboarding_state = load_onboarding_data(user_info["user_id"])
if not onboarding_state.get("is_completed") and st.session_state.get("active_view") == "onboarding":
    render_onboarding_wizard(user_info)
    st.stop()

# 7. Sidebar & Dynamic Analytics Calculation
active_view_id = render_app_sidebar(user_info)

# Dynamic Factor Calculation & Readiness Engine
role_meta = CAREER_TRACKS.get(st.session_state["target_role"], CAREER_TRACKS["Data Analyst"])
resume_eval = ResumeService.evaluate_ats_quality(st.session_state["candidate_text"], st.session_state["candidate_skills"])
gap_data = SkillGapService.evaluate_gaps(st.session_state["candidate_skills"], st.session_state["target_role"])
gap_eval = gap_data["gap_analysis"]
hierarchy_analysis = gap_data["hierarchy_tree"]

github_res = verify_github_profile(st.session_state["github_user"])
cand_lower = st.session_state["candidate_text"].lower()

# Dynamic Project Score
calc_proj = 50.0
if "project" in cand_lower: calc_proj += 15.0
if "github.com" in cand_lower or github_res.get("verified"): calc_proj += 15.0
if "deployed" in cand_lower or "streamlit" in cand_lower or "api" in cand_lower: calc_proj += 10.0
proj_score = min(100.0, max(30.0, st.session_state.get("last_project_audit_score", calc_proj)))

# Dynamic Assessment Score
verified_scores = st.session_state.get("verified_skills_scores", {})
if verified_scores:
    assess_score = round(sum(verified_scores.values()) / len(verified_scores), 1)
else:
    assess_score = round(gap_eval["readiness_score"] * 0.85, 1)

interv_score = st.session_state.get("last_interview_score", round(gap_eval["readiness_score"] * 0.8, 1))
comm_score = st.session_state.get("last_comm_score", 75.0 if "communication" in cand_lower else 60.0)
evidence_score = 90.0 if github_res.get("verified") else (70.0 if "github.com" in cand_lower else 40.0)

readiness_eval = ReadinessService.calculate_readiness(
    resume_score=resume_eval["score"],
    skill_gap_result=gap_eval,
    project_score=proj_score,
    assessment_score=assess_score,
    interview_score=interv_score,
    communication_score=comm_score,
    evidence_score=evidence_score,
    target_role=st.session_state["target_role"],
    target_company=st.session_state["target_company"]
)

# Auto-persist Profile
save_user_profile(
    user_id=user_info["user_id"],
    target_role=st.session_state["target_role"],
    target_company=st.session_state["target_company"],
    candidate_text=st.session_state["candidate_text"],
    candidate_skills=st.session_state["candidate_skills"],
    github_user=st.session_state["github_user"],
    readiness_score=readiness_eval["overall_readiness"]
)

# 8. Top Navbar
render_top_navbar(
    user_info=user_info,
    target_role=st.session_state["target_role"],
    readiness_score=readiness_eval["overall_readiness"],
    active_theme=app_theme
)

# ==========================================
# VIEW 1: PERSONALIZED DASHBOARD
# ==========================================
if active_view_id == "nav_dashboard":
    render_section_header(
        title=f"Welcome back, {user_info['full_name']}",
        subtitle=f"Targeting **{st.session_state['target_role']}** at **{st.session_state['target_company'].split('(')[0]}** • Operating System Status: Active",
        icon="🏆"
    )

    # Top Metric Cards
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        render_metric_card("Overall Readiness", f"{readiness_eval['overall_readiness']}%", "7-Factor Weighted Score", "#34D399", "🎯")
    with col_m2:
        render_metric_card("Resume ATS Quality", f"{resume_eval['score']}/100", "Keyword & Format Audit", "#818CF8", "📄")
    with col_m3:
        render_metric_card("Technical Match", f"{gap_eval['readiness_score']}%", f"{len(gap_eval['strong_skills'])} of {len(role_meta['core_skills'])} Core Skills", "#FBBF24", "📊")
    with col_m4:
        app_summary = ApplicationService.get_pipeline(user_info["user_id"])
        render_metric_card("Active Pipeline", f"{app_summary['total_count']} Jobs", f"{app_summary['interviews_count']} in Interviews", "#C084FC", "💼")

    # High-Priority NEXT BEST ACTION Card
    top_targets = hierarchy_analysis.get("next_learning_targets", [])
    if top_targets:
        nb_action = f"Master {top_targets[0]['skill']} Prerequisite"
        nb_desc = f"All prerequisites are satisfied. Acquiring {top_targets[0]['skill']} will unlock Level {top_targets[0]['level']} modeling and boost your Technical Match score."
        nb_cat = top_targets[0]["category"]
    else:
        nb_action = "Deploy Flagship Portfolio Project"
        nb_desc = "Your foundational skills are strong. Architect and deploy a live project with a structured README to elevate your evidence score."
        nb_cat = "Projects"

    render_next_best_action_card(
        action_title=nb_action,
        category=nb_cat,
        time_estimate="25 Mins",
        description=nb_desc
    )

    # 7-Factor Transparency & Competency Radar
    col_dash1, col_dash2 = st.columns([1.15, 0.85])
    with col_dash1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Transparent 7-Factor Readiness Breakdown")
        for f_name, f_val in readiness_eval["factors"].items():
            col_f1, col_f2 = st.columns([3.5, 1])
            with col_f1:
                weight_pct = int(readiness_eval["weights"].get(f_name, 0.15) * 100)
                st.write(f"**{f_name}** ({weight_pct}% weight)")
                st.progress(f_val / 100)
            with col_f2:
                st.markdown(f"<h4 style='margin:0; text-align:right; color:#818CF8;'>{f_val}%</h4>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_dash2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### ⚡ Competency Radar")
        radar_fig = render_theme_radar(readiness_eval["factors"], theme=app_theme)
        st.plotly_chart(radar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Daily Mission
    daily_mission = generate_daily_career_mission(gap_eval["missing_skills"], gap_eval["moderate_skills"], st.session_state["target_role"])
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown(f"### 🎯 Today's Career Mission — Estimated Time: `{daily_mission['estimated_time']}`")
    for task in daily_mission["tasks"]:
        col_t1, col_t2 = st.columns([4, 1])
        with col_t1:
            st.markdown(f"**{task['title']}** — `{task['category']}` (`{task['time_estimate']}`)")
            st.caption(task["description"])
        with col_t2:
            st.checkbox("Done", key=f"dash_daily_{task['id']}")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 2: CAREER EXPLORER
# ==========================================
elif active_view_id == "nav_explorer":
    render_section_header(
        title="Career Explorer & Multi-Track Matching",
        subtitle="Discover how your skills and interests align across 14+ high-growth tech specializations.",
        icon="🧭"
    )

    matched_careers = CareerMatchingService.match_all_careers(
        st.session_state["candidate_skills"],
        interests=onboarding_state.get("interests", []),
        experience_level=onboarding_state.get("experience_level", "Entry Level")
    )

    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        search_query = st.text_input("🔍 Search Career Tracks:", placeholder="Filter by title, category, or skill keyword...")
    with col_filter2:
        all_cats = ["All Categories"] + sorted(list(set(c["category"] for c in matched_careers)))
        sel_cat = st.selectbox("Filter Category:", all_cats)

    # Visual Comparison Bar Chart
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("### 📈 Match Score Overview Across Top Tracks")
    bar_chart = render_career_bar_chart(matched_careers, theme=app_theme)
    st.plotly_chart(bar_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Career Cards Grid
    for c in matched_careers:
        if sel_cat != "All Categories" and c["category"] != sel_cat:
            continue
        if search_query and search_query.lower() not in c["role"].lower() and search_query.lower() not in str(c["core_skills"]).lower():
            continue

        with st.expander(f"{c['icon']} **{c['role']}** — Match: **{c['match_score']}%** ({c['fit_badge']})", expanded=(c['role'] == st.session_state['target_role'])):
            col_c1, col_c2 = st.columns([2, 1])
            with col_c1:
                st.markdown(f"**Category:** `{c['category']}` | **Difficulty:** `{c['difficulty']}` | **Demand:** `{c['demand_growth']}`")
                st.markdown(f"**Average Compensation:** `{c['avg_salary']}`")
                st.markdown(f"<p style='color:#CBD5E1; margin:8px 0;'>{c['description']}</p>", unsafe_allow_html=True)
                st.info(f"💡 **Fit Rationale:** {c['fit_reason']}")
                
                st.markdown("##### 🛠️ Core Required Skills:")
                for sk in c["core_skills"]:
                    if sk in c["matched_skills"]:
                        st.markdown(f"<span class='badge-strong'>✓ {sk}</span>", unsafe_allow_html=True)
                    elif sk in c["developing_skills"]:
                        st.markdown(f"<span class='badge-moderate'>⚡ {sk}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='badge-missing'>+ {sk}</span>", unsafe_allow_html=True)

            with col_c2:
                st.markdown("##### 🎯 Actions:")
                if st.button(f"Set as My Target Role", key=f"btn_set_role_{c['role']}"):
                    st.session_state["target_role"] = c["role"]
                    st.success(f"Target role updated to {c['role']}!")
                    st.rerun()

                st.markdown("##### 🎤 Interview Focus:")
                st.caption(c["interview_focus"])

# ==========================================
# VIEW 3: CAREER COMPARISON
# ==========================================
elif active_view_id == "nav_comparison":
    render_section_header(
        title="Side-by-Side Career Comparator",
        subtitle="Compare required skills, transition difficulty, learning curves, and salary differentials between two roles.",
        icon="⚖️"
    )

    career_names = list(CAREER_TRACKS.keys())
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        role_a = st.selectbox("Select Career A:", career_names, index=career_names.index(st.session_state["target_role"]) if st.session_state["target_role"] in career_names else 0)
    with col_sel2:
        role_b = st.selectbox("Select Career B:", career_names, index=1 if len(career_names) > 1 else 0)

    cmp_data = CareerComparisonService.compare_careers(role_a, role_b, st.session_state["candidate_skills"])
    
    col_card_a, col_card_b = st.columns(2)
    with col_card_a:
        st.markdown(f"""
        <div class="glass-box" style="border-top: 4px solid #818CF8;">
            <h2>{cmp_data['track_a']['icon']} {cmp_data['track_a']['role']}</h2>
            <p style="color:#94A3B8;">{cmp_data['track_a']['description']}</p>
            <div style="font-size:1.3rem; font-weight:800; color:#34D399; margin:10px 0;">{cmp_data['track_a']['avg_salary']}</div>
            <p><strong>Your Match:</strong> {cmp_data['track_a']['match_score']}%</p>
            <p><strong>Difficulty:</strong> {cmp_data['track_a']['difficulty']}</p>
            <p><strong>Demand Growth:</strong> {cmp_data['track_a']['demand']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_card_b:
        st.markdown(f"""
        <div class="glass-box" style="border-top: 4px solid #EC4899;">
            <h2>{cmp_data['track_b']['icon']} {cmp_data['track_b']['role']}</h2>
            <p style="color:#94A3B8;">{cmp_data['track_b']['description']}</p>
            <div style="font-size:1.3rem; font-weight:800; color:#34D399; margin:10px 0;">{cmp_data['track_b']['avg_salary']}</div>
            <p><strong>Your Match:</strong> {cmp_data['track_b']['match_score']}%</p>
            <p><strong>Difficulty:</strong> {cmp_data['track_b']['difficulty']}</p>
            <p><strong>Demand Growth:</strong> {cmp_data['track_b']['demand']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("### 🔄 Transition Delta Analysis")
    st.info(f"Transition Difficulty Shift: **{cmp_data['transition_delta']['difficulty_shift']}** | Estimated Bridge Time: **{cmp_data['transition_delta']['estimated_time']}**")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("##### 🤝 Shared Skills:")
        for s in cmp_data["shared_skills"]:
            st.markdown(f"<span class='badge-strong'>{s}</span>", unsafe_allow_html=True)
    with col_t2:
        st.markdown("##### 🎯 Skills Needed to Switch:")
        for s in cmp_data["transition_delta"]["skills_needed"]:
            st.markdown(f"<span class='badge-missing'>+ {s}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 4: SKILL GAP & TREE
# ==========================================
elif active_view_id == "nav_skill_gap":
    render_section_header(
        title=f"Skill Gap & Prerequisite Tree — {st.session_state['target_role']}",
        subtitle="Identify prerequisite dependencies, immediate learning targets, and take verification tests.",
        icon="📊"
    )

    h_sum = hierarchy_analysis["summary"]
    hc1, hc2, hc3, hc4 = st.columns(4)
    with hc1:
        render_metric_card("Mastered Skills", f"{h_sum['mastered']} / {h_sum['total_skills']}", "Present on profile", "#34D399", "🟢")
    with hc2:
        render_metric_card("Next Targets", f"{h_sum['next_targets']} Ready", "Prereqs satisfied", "#818CF8", "🚀")
    with hc3:
        render_metric_card("Blocked", f"{h_sum['blocked']} Skills", "Prereqs missing", "#F87171", "🔒")
    with hc4:
        render_metric_card("Skill Mastery", f"{round((h_sum['mastered']/h_sum['total_skills'])*100, 1)}%", "Role requirements", "#FBBF24", "📈")

    if hierarchy_analysis["next_learning_targets"]:
        st.markdown('<div class="glass-box" style="border-left: 5px solid #818CF8;">', unsafe_allow_html=True)
        st.markdown("### 🚀 Top 5 Skills to Learn Next (Prerequisites Ready)")
        for tgt in hierarchy_analysis["next_learning_targets"]:
            prereq_str = f" (Prerequisites met: {', '.join(tgt['prereqs'])})" if tgt['prereqs'] else " (Foundational Skill)"
            st.markdown(f"- 🚀 **{tgt['skill']}** `[Level {tgt['level']} — {tgt['category']}]`{prereq_str}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🌲 Complete 4-Level Skill Tree")
    level_titles = {
        1: "Level 1: Foundations & Literacy",
        2: "Level 2: Core Tools & Data Wrangling",
        3: "Level 3: Advanced Modeling & Analysis",
        4: "Level 4: Production & Deployment"
    }
    for lvl in range(1, 5):
        items = hierarchy_analysis["levels"].get(lvl, [])
        if items:
            with st.expander(f"📍 {level_titles[lvl]} ({len(items)} Skills)", expanded=(lvl <= 2)):
                for sk in items:
                    badge_style = "badge-strong" if sk["status_code"] == "STRONG" else ("badge-target" if sk["status_code"] == "NEXT_TARGET" else "badge-missing")
                    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04);'><div><strong>{sk['skill']}</strong> — <code style='color:#94A3B8;'>{sk['category']}</code><br><span style='font-size:0.82rem; color:#64748B;'>{sk['reason']}</span></div><span class='{badge_style}'>{sk['status']}</span></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("🧪 Skill Verification Test")
    test_skill = st.selectbox("Select Skill to Verify:", ["SQL", "Python", "Power BI", "Machine Learning"])
    questions = get_assessment_for_skill(test_skill)
    user_ans = {}
    for idx, q in enumerate(questions):
        st.markdown(f"**Q{idx+1}: {q['question']}**")
        user_ans[idx] = st.radio(f"Answer Q{idx+1}:", range(len(q['options'])), format_func=lambda i: q['options'][i], key=f"q_{test_skill}_{idx}")
    if st.button(f"Submit {test_skill} Assessment", type="primary"):
        eval_res = evaluate_skill_assessment(test_skill, user_ans, questions)
        st.session_state["verified_skills"][test_skill] = eval_res["verified_level"]
        st.session_state["verified_skills_scores"][test_skill] = float(eval_res["verified_percentage"])
        st.success(f"🎉 Verification Result: **{eval_res['verified_level']}** ({eval_res['verified_percentage']}% Score)")
        st.rerun()

# ==========================================
# VIEW 5: DYNAMIC AI ROADMAP
# ==========================================
elif active_view_id == "nav_roadmap":
    render_section_header(
        title=f"Dynamic 8-Stage Career Roadmap — {st.session_state['target_role']}",
        subtitle="Interactive milestone checklist with persistent progress tracking saved to your profile.",
        icon="🗺️"
    )

    roadmap_data = RoadmapService.generate_8_stage_roadmap(
        user_id=user_info["user_id"],
        missing_skills=gap_eval["missing_skills"],
        moderate_skills=gap_eval["moderate_skills"],
        target_role=st.session_state["target_role"]
    )

    col_r1, col_r2 = st.columns([3, 1])
    with col_r1:
        st.progress(roadmap_data["overall_progress_pct"] / 100)
    with col_r2:
        st.markdown(f"<h4 style='margin:0; text-align:right; color:#34D399;'>{roadmap_data['overall_progress_pct']}% Completed</h4>", unsafe_allow_html=True)

    for phase in roadmap_data["phases"]:
        status_icon = "✅" if phase["is_phase_completed"] else "📍"
        with st.expander(f"{status_icon} **{phase['title']}** ({phase['completed_count']}/{phase['total_count']} Tasks) — ⏱️ {phase['duration']}", expanded=(phase["phase_num"] <= 2)):
            st.markdown(f"**Focus:** {phase['focus']}")
            st.markdown(f"**Difficulty:** `{phase['difficulty']}`")
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            for t in phase["tasks"]:
                chk = st.checkbox(
                    f"**{t['title']}** (⏱️ `{t['time']}` • Resource: `{t['res']}`)",
                    value=t["is_completed"],
                    key=f"chk_task_{t['id']}"
                )
                if chk != t["is_completed"]:
                    RoadmapService.toggle_task(user_info["user_id"], phase["title"], t["id"], chk)
                    st.rerun()

# ==========================================
# VIEW 6: LEARNING HUB
# ==========================================
elif active_view_id == "nav_learning":
    render_section_header(
        title="Curated Learning Hub",
        subtitle="Explore high-impact courses, documentation, and tutorials mapped directly to your skill gaps.",
        icon="📚"
    )

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        filter_skill = st.selectbox("Filter by Skill:", ["All Skills", "SQL", "Python", "Pandas", "Machine Learning", "FastAPI", "Docker", "Power BI", "Statistics"])
    with col_l2:
        filter_tier = st.selectbox("Difficulty Tier:", ["All Levels", "Beginner", "Intermediate", "Advanced"])

    resources = LearningHubService.get_resources(filter_skill, filter_tier)
    for res in resources:
        with st.expander(f"📖 **{res['title']}** — `{res['platform']}` ({res['tier']})"):
            st.markdown(f"<p style='color:#CBD5E1;'>{res['description']}</p>", unsafe_allow_html=True)
            st.markdown(f"**Estimated Duration:** `{res['duration']}` | **Skills Covered:** `{', '.join(res['skills'])}`")
            col_b1, col_b2 = st.columns([1, 4])
            with col_b1:
                st.markdown(f"<a href='{res['url']}' target='_blank' style='display:inline-block; background:#6366F1; color:#FFF; padding:6px 14px; border-radius:8px; text-decoration:none; font-weight:700;'>Open Tutorial ↗</a>", unsafe_allow_html=True)
            with col_b2:
                if st.button("⭐ Bookmark Resource", key=f"btn_bm_{res['id']}"):
                    LearningHubService.bookmark_resource(user_info["user_id"], res["id"], res["title"], res["url"], res["category"])
                    st.success("Bookmarked!")

# ==========================================
# VIEW 7: PROJECT BUILDER & AUDITOR
# ==========================================
elif active_view_id == "nav_projects":
    render_section_header(
        title="Portfolio Project Builder & 7D Auditor",
        subtitle="Architect flagship portfolio projects and audit existing implementations against engineering benchmarks.",
        icon="💡"
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🔍 7-Dimensional Project Strength Auditor")
        p_name = st.text_input("Project Name:", value="Real-Time Customer Churn Prediction Pipeline")
        p_tech = st.text_input("Tech Stack:", value="Python, Scikit-learn, XGBoost, Streamlit, Docker")
        p_desc = st.text_area("Description & Metrics:", value="Architected ML classifier on 50k customer logs with 89.2% ROC-AUC score, deployed via Streamlit.")
        p_dep = st.checkbox("Live Deployment Available", value=True)
        p_doc = st.checkbox("Has Detailed README & Architecture", value=True)

        if st.button("Audit Project Strength", type="primary"):
            audit_res = ProjectService.audit_project(p_name, p_tech, p_desc, p_dep, p_doc)
            st.session_state["last_project_audit_score"] = float(audit_res["overall_score"])
            st.subheader(f"Overall Strength: **{audit_res['overall_score']}/100**")
            for c_name, c_val in audit_res["criteria"].items():
                st.write(f"**{c_name}:** {c_val}/100")
                st.progress(c_val / 100)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_p2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🚀 AI Flagship Project Blueprint Generator")
        blueprint = ProjectService.generate_blueprint(st.session_state["candidate_skills"], st.session_state["target_role"])
        st.markdown(f"#### **{blueprint['title']}**")
        st.markdown(f"**Difficulty:** `{blueprint['difficulty']}` | **Estimated Time:** `{blueprint['estimated_time']}`")
        st.markdown(f"**Dataset:** [{blueprint['dataset_name']}]({blueprint['dataset_link']})")
        st.markdown(f"<p style='color:#CBD5E1;'>{blueprint['description']}</p>", unsafe_allow_html=True)
        st.markdown("##### 📋 Architecture Tasks:")
        for idx, task_txt in enumerate(blueprint["tasks"], 1):
            st.markdown(f"{idx}. {task_txt}")
        with st.expander("📁 GitHub File Schema & README Spec"):
            st.code(blueprint["github_structure"], language="text")
            st.code(blueprint["readme_snippet"], language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 8: RESUME AI STUDIO
# ==========================================
elif active_view_id == "nav_resume":
    render_section_header(
        title="ATS Resume AI Studio",
        subtitle="Multi-format resume analysis, keyword density check, and STAR method bullet point optimizer.",
        icon="📄"
    )

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown(f"### ATS Score: **{resume_eval['score']}/100**")
        st.progress(resume_eval['score'] / 100)
        st.markdown("#### Audit Checklist:")
        for k, v in resume_eval["checks"].items():
            st.markdown(f"- **{k}**: `{v}`")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_res2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        sim_val = ResumeService.compute_job_match_similarity(st.session_state["candidate_text"], st.session_state["target_jd_text"])
        st.markdown(f"### Job Description Similarity: **{sim_val}%**")
        st.progress(sim_val / 100)
        st.markdown("Contextual TF-IDF cosine similarity against target job requirements.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("### ✨ STAR Method Bullet Point Rewriter")
    weak_bullet = st.text_input("Paste any weak bullet point from your resume:", value="Worked on customer churn prediction model using Python")
    if st.button("🚀 Optimize Bullet Point", type="primary"):
        opt = ResumeService.optimize_bullet(weak_bullet, st.session_state["target_role"])
        st.success("✅ **STAR Optimized Bullet:**")
        st.code(opt["optimized"], language="text")
        st.caption(f"Action Verb: **{opt['action_verb']}** | Quant Impact: **{opt['impact_metric']}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 9: INTERVIEW LAB
# ==========================================
elif active_view_id == "nav_interview":
    render_section_header(
        title="STAR Interview Simulation Lab",
        subtitle="Practice Technical, HR, Behavioral, and Role-specific mock interview questions with instant STAR communication intelligence.",
        icon="🎤"
    )

    col_iv1, col_iv2 = st.columns([1, 1])
    with col_iv1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        int_mode = st.selectbox("Select Interview Mode:", InterviewService.MODES)
        questions = InterviewService.get_questions(int_mode, st.session_state["target_company"], st.session_state["target_role"])
        q_idx = st.selectbox("Select Question:", range(len(questions)), format_func=lambda i: f"Q{i+1}: {questions[i]['question'][:65]}...")
        active_q = questions[q_idx]

        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.1); border-left:5px solid #818CF8; border-radius:12px; padding:18px; margin-top:14px;">
            <div style="font-size:0.8rem; font-weight:700; color:#A5B4FC;">{active_q.get('category', int_mode)}</div>
            <h3 style="color:#FFF !important; margin:6px 0 0 0;">"{active_q['question']}"</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_iv2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        ans_text = st.text_area("✍️ Type Your Answer (STAR Method):", height=150, placeholder="Situation: ... Task: ... Action: ... Result: ...")
        if st.button("Submit Answer for AI Evaluation", type="primary"):
            if ans_text.strip():
                eval_out = InterviewService.evaluate_answer(active_q, ans_text)
                st.session_state["last_interview_score"] = float(eval_out["content_score"] * 10)
                st.session_state["last_comm_score"] = float(eval_out["comm_score"])
                st.subheader(f"Content Score: **{eval_out['content_score']}/10** | STAR Communication: **{eval_out['comm_score']}/100**")
                st.info(eval_out["time_feedback"])
                st.markdown("##### STAR Structure Checklist:")
                for k, present in eval_out["star_checklist"].items():
                    st.write(f"- {'✅' if present else '❌'} **{k}**")
                st.rerun()
            else:
                st.error("Please enter an answer first.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 10: APPLICATION TRACKER
# ==========================================
elif active_view_id == "nav_tracker":
    render_section_header(
        title="Job Application Pipeline Tracker",
        subtitle="Manage your applications across Kanban and List views with interview and offer stages.",
        icon="💼"
    )

    with st.expander("➕ Add New Job Application", expanded=False):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            a_comp = st.text_input("Company Name:", placeholder="e.g. Google, Snowflake, Stripe")
            a_role = st.text_input("Role Title:", value=st.session_state["target_role"])
            a_loc = st.text_input("Location:", value="Remote")
        with col_a2:
            a_sal = st.text_input("Salary Range:", placeholder="e.g. $110,000 - $130,000")
            a_url = st.text_input("Job URL:", placeholder="https://careers...")
            a_stat = st.selectbox("Status:", ApplicationService.STATUSES, index=0)
        a_notes = st.text_area("Notes / Interview Prep:", placeholder="Key contacts, referral info, interview dates...")
        if st.button("Save Job Application", type="primary"):
            if a_comp and a_role:
                ApplicationService.add_job(user_info["user_id"], a_comp, a_role, a_loc, a_sal, a_url, a_stat, a_notes)
                st.success("Job added to pipeline!")
                st.rerun()
            else:
                st.error("Company name and role title are required.")

    pipeline_data = ApplicationService.get_pipeline(user_info["user_id"])
    
    tab_kanban, tab_list = st.tabs(["📋 Kanban Board View", "📑 List Table View"])
    
    with tab_kanban:
        kanban_cols = st.columns(len(ApplicationService.STATUSES))
        for idx, (status_name, col) in enumerate(zip(ApplicationService.STATUSES, kanban_cols)):
            with col:
                st.markdown(f"<div style='font-size:0.85rem; font-weight:800; color:#A78BFA; margin-bottom:8px;'>{status_name} ({len(pipeline_data['kanban'][status_name])})</div>", unsafe_allow_html=True)
                for item in pipeline_data["kanban"][status_name]:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(99,102,241,0.2); border-radius:12px; padding:12px; margin-bottom:10px;">
                        <div style="font-weight:800; color:#FFF; font-size:0.95rem;">{item['company_name']}</div>
                        <div style="color:#94A3B8; font-size:0.8rem;">{item['role_title']}</div>
                        <div style="color:#64748B; font-size:0.75rem; margin-top:4px;">📍 {item['location']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    new_st = st.selectbox("Move to:", ApplicationService.STATUSES, index=ApplicationService.STATUSES.index(status_name), key=f"kb_move_{item['id']}")
                    if new_st != status_name:
                        ApplicationService.update_status(item["id"], user_info["user_id"], new_st)
                        st.rerun()

    with tab_list:
        if pipeline_data["all_applications"]:
            df_apps = pd.DataFrame(pipeline_data["all_applications"])[["id", "company_name", "role_title", "location", "status", "salary_range", "applied_date"]]
            st.dataframe(df_apps, use_container_width=True)
        else:
            st.info("No applications logged yet. Click 'Add New Job Application' above.")

# ==========================================
# VIEW 11: PUBLIC PORTFOLIO
# ==========================================
elif active_view_id == "nav_portfolio":
    render_section_header(
        title="Public Career Portfolio Builder",
        subtitle="Create a shareable, verified career profile to demonstrate skills to hiring managers.",
        icon="🌐"
    )

    port_data = get_user_portfolio(user_info["user_id"])
    col_pf1, col_pf2 = st.columns(2)
    with col_pf1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Portfolio Settings")
        pf_headline = st.text_input("Professional Headline:", value=port_data["headline"])
        pf_bio = st.text_area("Bio / Mission Statement:", value=port_data["bio"])
        pf_gh = st.text_input("GitHub Profile URL:", value=port_data["github_url"])
        pf_li = st.text_input("LinkedIn Profile URL:", value=port_data["linkedin_url"])
        pf_pub = st.checkbox("Public Visibility Enabled", value=port_data["is_public"])

        if st.button("Save Portfolio", type="primary"):
            save_user_portfolio(user_info["user_id"], pf_headline, pf_bio, pf_gh, pf_li, "", pf_pub)
            st.success("Portfolio saved!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pf2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🔗 Shareable Link Preview")
        share_url = f"http://localhost:8501/?portfolio={user_info['username']}"
        st.code(share_url, language="text")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(139,92,246,0.3); border-radius:16px; padding:20px; margin-top:14px;">
            <h3 style="margin:0 0 4px 0; color:#FFF;">{user_info['full_name']}</h3>
            <div style="color:#A78BFA; font-weight:700; margin-bottom:8px;">{pf_headline}</div>
            <p style="color:#CBD5E1; font-size:0.88rem;">{pf_bio}</p>
            <div style="margin-top:12px;">
                <span style="font-size:0.8rem; color:#34D399; font-weight:800;">✓ {readiness_eval['overall_readiness']}% Ready for {st.session_state['target_role']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 12: AI CAREER COPILOT
# ==========================================
elif active_view_id == "nav_copilot":
    render_section_header(
        title="AI Career Copilot",
        subtitle="Your personalized career assistant with real-time context of your target role and skill gaps.",
        icon="🤖"
    )

    # Prompt Chips
    st.markdown("<div style='font-size:0.82rem; font-weight:700; color:#94A3B8; margin-bottom:8px;'>SUGGESTED ACTIONS:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(3)
    preset_query = None
    for idx, prompt in enumerate(CopilotService.QUICK_PROMPTS):
        with chip_cols[idx % 3]:
            if st.button(f"💡 {prompt}", key=f"copilot_prompt_{idx}", use_container_width=True):
                preset_query = prompt

    ctx = {
        "candidate_skills": st.session_state["candidate_skills"],
        "target_role": st.session_state["target_role"],
        "readiness_score": readiness_eval["overall_readiness"],
        "missing_skills": gap_eval["missing_skills"],
        "moderate_skills": gap_eval["moderate_skills"],
        "strong_skills": gap_eval["strong_skills"],
        "resume_score": resume_eval["score"]
    }

    if preset_query:
        st.session_state["chat_history"].append({"role": "user", "content": preset_query})
        ans = CopilotService.answer_query(preset_query, ctx)
        st.session_state["chat_history"].append({"role": "assistant", "content": ans})

    # Render Chat Log
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_q = st.chat_input("Ask your AI Career Copilot anything...")
    if user_q:
        st.session_state["chat_history"].append({"role": "user", "content": user_q})
        ans = CopilotService.answer_query(user_q, ctx)
        st.session_state["chat_history"].append({"role": "assistant", "content": ans})
        st.rerun()

# ==========================================
# VIEW 13: ACCOUNT SETTINGS
# ==========================================
elif active_view_id == "nav_settings":
    render_section_header(
        title="Account Settings & Preferences",
        subtitle="Manage your profile, security credentials, and application notifications.",
        icon="⚙️"
    )

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 👤 User Information")
        st.write(f"**Full Name:** {user_info.get('full_name', 'Student')}")
        st.write(f"**Username:** `{user_info.get('username', '')}`")
        st.write(f"**Country:** {user_info.get('country', 'United States')}")
        st.write(f"**Active Theme:** `{app_theme.capitalize()}`")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🔒 Security & Password Change")
        np1 = st.text_input("New Password:", type="password", key="settings_np1")
        np2 = st.text_input("Confirm New Password:", type="password", key="settings_np2")
        if st.button("Update Password", type="primary"):
            if np1 and np1 == np2:
                res = AuthService.reset_password(user_info["username"], np1)
                if res["success"]:
                    st.success("Password updated successfully!")
                else:
                    st.error(res["message"])
            else:
                st.error("Passwords do not match or are empty.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🔔 Milestone Notifications")
        render_notifications_panel(user_info["user_id"])
        st.markdown('</div>', unsafe_allow_html=True)
