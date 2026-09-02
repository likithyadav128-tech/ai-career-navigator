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

st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1320px !important;
        margin: 0 auto !important;
    }

    /* ===== SMOOTH ORB-TO-CARD MORPH ENGINE ===== */
    @keyframes morphOrbToCard {
        0% {
            border-radius: 50%;
            transform: scale(0.82) rotate(-3deg);
            opacity: 0.6;
            box-shadow: 0 0 60px rgba(139, 92, 246, 0.7), inset 0 0 40px rgba(99, 102, 241, 0.6);
        }
        50% {
            border-radius: 35%;
            transform: scale(1.03) rotate(0deg);
            box-shadow: 0 0 80px rgba(192, 132, 252, 0.8), inset 0 0 30px rgba(139, 92, 246, 0.4);
        }
        100% {
            border-radius: 24px;
            transform: scale(1) rotate(0deg);
            opacity: 1;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75), 0 0 35px rgba(99, 102, 241, 0.25);
        }
    }

    @keyframes orbPulseGlow {
        0%, 100% {
            box-shadow: 0 0 45px rgba(139, 92, 246, 0.35), inset 0 0 35px rgba(99, 102, 241, 0.25);
            border-color: rgba(139, 92, 246, 0.45);
        }
        50% {
            box-shadow: 0 0 75px rgba(168, 85, 247, 0.65), inset 0 0 50px rgba(129, 140, 248, 0.4);
            border-color: rgba(192, 132, 252, 0.75);
        }
    }

    .morph-card-active {
        animation: morphOrbToCard 0.65s cubic-bezier(0.34, 1.35, 0.64, 1) forwards !important;
        background: rgba(18, 24, 38, 0.85) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(139, 92, 246, 0.35) !important;
        border-radius: 24px !important;
        padding: 34px 28px !important;
    }

    .glowing-neon-orb {
        width: 100%;
        max-width: 440px;
        min-height: 440px;
        border-radius: 50%;
        background: radial-gradient(circle at 45% 45%, rgba(99, 102, 241, 0.22) 0%, rgba(139, 92, 246, 0.12) 50%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid rgba(139, 92, 246, 0.45);
        animation: orbPulseGlow 3.5s ease-in-out infinite;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 32px;
        margin: 0 auto;
        cursor: pointer;
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .glowing-neon-orb:hover {
        transform: scale(1.03);
        box-shadow: 0 0 85px rgba(168, 85, 247, 0.75), inset 0 0 55px rgba(129, 140, 248, 0.45);
    }

    .smooth-transition-container {
        animation: morphOrbToCard 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    /* Global Input Overrides */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        color: inherit !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 12px !important;
    }
    textarea, input[type="text"], input[type="password"] {
        background: rgba(255,255,255,0.04) !important;
        color: inherit !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
    }
    textarea:focus, input:focus {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }

    /* Badges */
    .badge-strong {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34D399 !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }
    .badge-moderate {
        background: rgba(245, 158, 11, 0.15) !important;
        color: #FBBF24 !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }
    .badge-missing {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #F87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }
    .badge-target {
        background: rgba(99, 102, 241, 0.2) !important;
        color: #A5B4FC !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; display: inline-block; margin: 3px;
    }

    /* ===== PLACEMENT WEBAPP AUTH STYLES ===== */
    .brand-logo-badge {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }

    .brand-logo-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 24px rgba(168, 85, 247, 0.5);
    }

    .brand-logo-icon span {
        color: #ffffff;
        font-weight: 900;
        font-size: 1.3rem;
        letter-spacing: -1px;
    }

    .brand-title-main {
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 1.05 !important;
        margin: 0 !important;
        letter-spacing: -1px;
    }

    .brand-title-gradient {
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        line-height: 1.1 !important;
        margin: 0 0 12px 0 !important;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 45%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .brand-subtitle-text {
        font-size: 0.98rem;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 22px;
    }

    .feature-item-card {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 16px;
    }

    .feature-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(99, 102, 241, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 1.25rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .feature-text-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }

    .feature-text-desc {
        font-size: 0.84rem;
        color: #94a3b8;
        line-height: 1.35;
    }

    .auth-card-top-icon {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border: 1px solid rgba(139, 92, 246, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.35);
    }

    .auth-card-top-icon span {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #818CF8, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .auth-card-title {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-align: center;
        margin: 0 0 4px 0 !important;
    }

    .auth-card-subtitle {
        font-size: 0.88rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 20px;
    }

    .auth-input-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #818CF8;
        letter-spacing: 1px;
        margin: 12px 0 4px 0;
        text-transform: uppercase;
    }

    .auth-divider-row {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 18px 0;
        color: #64748b;
        font-size: 0.8rem;
    }

    .auth-divider-row::before, .auth-divider-row::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .auth-divider-row span {
        padding: 0 12px;
    }

    .auth-security-footer {
        text-align: center;
        margin-top: 24px;
        font-size: 0.76rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* Right Column Glass Container */
    .auth-right-card {
        background: rgba(15, 23, 42, 0.78);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 28px;
        padding: 28px 26px;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.7), 0 0 40px rgba(108, 99, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None

if "active_view" not in st.session_state:
    st.session_state["active_view"] = "auth" if not st.session_state["logged_in"] else "nav_dashboard"

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

# 5. Routing Logic: Authentication Gateway vs Authenticated Dashboard
if not st.session_state["logged_in"]:
    if "portal_view" not in st.session_state:
        st.session_state["portal_view"] = "initial"

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "Sign In"

    # Smooth Animated Container Wrapper
    st.markdown('<div class="smooth-transition-container">', unsafe_allow_html=True)

    # ==========================================
    # STAGE 1: INITIAL LANDING / HERO SCREEN
    # ==========================================
    if st.session_state["portal_view"] == "initial":
        col_left, col_right = st.columns([1.1, 1], gap="large")

        with col_left:
            st.markdown("""<div class="brand-logo-badge">
<div class="brand-logo-icon"><span>⬡</span></div>
<div>
<div style="font-size: 0.72rem; font-weight: 800; color: #818CF8; letter-spacing: 1.5px; text-transform: uppercase;">AI PLACEMENT PORTAL</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px;">CAREER INTELLIGENCE OS</div>
</div>
</div>
<div style="font-size: 3.4rem; font-weight: 900; line-height: 1.05; color: #FFFFFF; letter-spacing: -1px; margin-bottom: 8px;">
Your Dream<br>
<span style="color: #FFFFFF;">Tech Career</span><br>
<span style="background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Starts Here</span>
</div>
<div style="font-size: 1.1rem; color: #94A3B8; margin-bottom: 24px; font-weight: 500;">
Practice. Improve. Get Placed.
</div>
<div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 28px;">
<div style="display: flex; align-items: center; gap: 10px; font-size: 0.95rem; color: #E2E8F0; font-weight: 600;">
<span style="background: rgba(99,102,241,0.25); color: #818CF8; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem; border: 1px solid rgba(99,102,241,0.4);">✓</span>
14+ Company Mock Tests & Roles
</div>
<div style="display: flex; align-items: center; gap: 10px; font-size: 0.95rem; color: #E2E8F0; font-weight: 600;">
<span style="background: rgba(99,102,241,0.25); color: #818CF8; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem; border: 1px solid rgba(99,102,241,0.4);">✓</span>
AI Interview Simulator with STAR Feedback
</div>
<div style="display: flex; align-items: center; gap: 10px; font-size: 0.95rem; color: #E2E8F0; font-weight: 600;">
<span style="background: rgba(99,102,241,0.25); color: #818CF8; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem; border: 1px solid rgba(99,102,241,0.4);">✓</span>
Skill Assessments & Prerequisite Trees
</div>
<div style="display: flex; align-items: center; gap: 10px; font-size: 0.95rem; color: #E2E8F0; font-weight: 600;">
<span style="background: rgba(99,102,241,0.25); color: #818CF8; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem; border: 1px solid rgba(99,102,241,0.4);">✓</span>
Personalized 8-Stage Career Roadmap
</div>
</div>""", unsafe_allow_html=True)

            col_btn1, col_btn2 = st.columns([1.5, 1])
            with col_btn1:
                if st.button("🚀 Explore Platform & Sign In →", key="btn_initial_explore", type="primary", use_container_width=True):
                    st.session_state["portal_view"] = "login"
                    st.rerun()

        with col_right:
            # Interactive Glowing Neon Morph Orb with Embedded 3D AI Cube
            st.markdown("""<div class="glowing-neon-orb">
<svg viewBox="0 0 320 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 15px 30px rgba(0,0,0,0.6));">
<defs>
<linearGradient id="cubeTopO" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#818CF8" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#C084FC" stop-opacity="0.5"/>
</linearGradient>
<linearGradient id="cubeLeftO" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#4F46E5" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.95"/>
</linearGradient>
<linearGradient id="cubeRightO" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#7C3AED" stop-opacity="0.85"/>
<stop offset="100%" stop-color="#312E81" stop-opacity="0.95"/>
</linearGradient>
<linearGradient id="platNeonO" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#06B6D4" stop-opacity="0.7"/>
<stop offset="50%" stop-color="#8B5CF6" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#EC4899" stop-opacity="0.7"/>
</linearGradient>
</defs>
<ellipse cx="160" cy="130" rx="130" ry="40" fill="rgba(129,140,248,0.2)"/>
<polygon points="160,95 270,130 160,165 50,130" fill="#0C1022" stroke="url(#platNeonO)" stroke-width="1.8"/>
<ellipse cx="160" cy="90" rx="120" ry="38" fill="none" stroke="rgba(99,102,241,0.35)" stroke-width="1.2" stroke-dasharray="5,5" transform="rotate(-8 160 90)"/>
<g transform="translate(60, 40)"><circle cx="12" cy="12" r="12" fill="#1E1B4B" stroke="#818CF8" stroke-width="1.2"/><text x="12" y="16" font-size="9" font-weight="800" fill="#818CF8" text-anchor="middle" font-family="monospace">&lt;/&gt;</text></g>
<g transform="translate(240, 35)"><circle cx="12" cy="12" r="12" fill="#1E1B4B" stroke="#60A5FA" stroke-width="1.2"/><text x="12" y="16" font-size="9" font-weight="800" fill="#60A5FA" text-anchor="middle" font-family="monospace">&lt;/&gt;</text></g>
<g transform="translate(125, 25)">
<polygon points="35,0 70,20 35,40 0,20" fill="url(#cubeTopO)" stroke="#C7D2FE" stroke-width="1.2"/>
<polygon points="0,20 35,40 35,82 0,62" fill="url(#cubeLeftO)" stroke="rgba(129,140,248,0.5)" stroke-width="1.2"/>
<polygon points="35,40 70,20 70,62 35,82" fill="url(#cubeRightO)" stroke="rgba(192,132,252,0.5)" stroke-width="1.2"/>
<text x="17" y="58" font-size="20" font-weight="900" fill="#FFFFFF" font-family="Inter, sans-serif" transform="skewY(28) scale(0.9, 1)">AI</text>
<path d="M 35,0 L 35,40 M 0,20 L 35,40 L 70,20" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.7"/>
</g>
</svg>
<div style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; margin-top: 6px;">Welcome Back! 👋</div>
<div style="font-size: 0.88rem; color: #94A3B8; margin-top: 4px; margin-bottom: 16px;">Sign in to continue your career journey</div>
</div>""", unsafe_allow_html=True)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            col_orb_b1, col_orb_b2 = st.columns(2)
            with col_orb_b1:
                if st.button("⚡ Sign In ➔", key="btn_orb_signin", type="primary", use_container_width=True):
                    st.session_state["portal_view"] = "login"
                    st.session_state["auth_mode"] = "Sign In"
                    st.rerun()
            with col_orb_b2:
                if st.button("Create Account", key="btn_orb_signup", use_container_width=True):
                    st.session_state["portal_view"] = "login"
                    st.session_state["auth_mode"] = "Sign Up"
                    st.rerun()

    # ==========================================
    # STAGE 2: GLASSMORPHIC SIGN IN CARD VIEW
    # ==========================================
    elif st.session_state["portal_view"] == "login":
        col_nav_back, _ = st.columns([1, 4])
        with col_nav_back:
            if st.button("⬅ Back to Overview", key="btn_back_to_initial"):
                st.session_state["portal_view"] = "initial"
                st.rerun()

        col_left, col_right = st.columns([1.15, 1], gap="large")

        # Left Column
        with col_left:
            st.markdown("""<div class="brand-logo-badge">
<div class="brand-logo-icon"><span>⬡</span></div>
<div>
<div style="font-size: 0.72rem; font-weight: 800; color: #818CF8; letter-spacing: 1.5px; text-transform: uppercase;">AI PLACEMENT PORTAL</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.2px;">CAREER INTELLIGENCE OS</div>
</div>
</div>
<div style="font-size: 2.8rem; font-weight: 900; line-height: 1.1; color: #FFFFFF; letter-spacing: -1px;">
Your Dream<br>
<span style="color: #FFFFFF;">Tech Career</span><br>
<span style="background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Starts Here</span>
</div>
<div style="font-size: 0.98rem; color: #94A3B8; margin: 10px 0 18px 0; font-weight: 500;">
Practice. Improve. Get Placed.
</div>""", unsafe_allow_html=True)

            # 3D Isometric AI Cube Graphic
            st.markdown("""<div style="position:relative; width:100%; max-width:420px; display:flex; justify-content:center;">
<svg viewBox="0 0 460 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 20px 40px rgba(0,0,0,0.6));">
<defs>
<linearGradient id="cubeTop2" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#818CF8" stop-opacity="0.85"/>
<stop offset="100%" stop-color="#C084FC" stop-opacity="0.4"/>
</linearGradient>
<linearGradient id="cubeLeft2" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#4F46E5" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.95"/>
</linearGradient>
<linearGradient id="cubeRight2" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#7C3AED" stop-opacity="0.85"/>
<stop offset="100%" stop-color="#312E81" stop-opacity="0.95"/>
</linearGradient>
<linearGradient id="platformNeon2" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#06B6D4" stop-opacity="0.6"/>
<stop offset="50%" stop-color="#8B5CF6" stop-opacity="0.8"/>
<stop offset="100%" stop-color="#EC4899" stop-opacity="0.6"/>
</linearGradient>
</defs>
<ellipse cx="230" cy="185" rx="190" ry="65" fill="rgba(129,140,248,0.2)"/>
<polygon points="230,135 390,185 230,235 70,185" fill="#0C1022" stroke="url(#platformNeon2)" stroke-width="2"/>
<ellipse cx="230" cy="130" rx="180" ry="55" fill="none" stroke="rgba(99,102,241,0.3)" stroke-width="1.5" stroke-dasharray="6,6" transform="rotate(-10 230 130)"/>
<g transform="translate(85, 60)"><circle cx="16" cy="16" r="16" fill="#1E1B4B" stroke="#818CF8" stroke-width="1.5"/><text x="16" y="21" font-size="11" font-weight="800" fill="#818CF8" text-anchor="middle" font-family="monospace">&lt;/&gt;</text></g>
<g transform="translate(340, 50)"><circle cx="16" cy="16" r="16" fill="#1E1B4B" stroke="#60A5FA" stroke-width="1.5"/><text x="16" y="21" font-size="11" font-weight="800" fill="#60A5FA" text-anchor="middle" font-family="monospace">&lt;/&gt;</text></g>
<g transform="translate(370, 115)"><circle cx="15" cy="15" r="15" fill="#1E1B4B" stroke="#34D399" stroke-width="1.5"/><text x="15" y="20" font-size="11" font-weight="800" fill="#34D399" text-anchor="middle" font-family="Inter, sans-serif">📊</text></g>
<g transform="translate(60, 140)"><circle cx="15" cy="15" r="15" fill="#1E1B4B" stroke="#F472B6" stroke-width="1.5"/><text x="15" y="20" font-size="11" font-weight="800" fill="#F472B6" text-anchor="middle" font-family="Inter, sans-serif">🗄️</text></g>
<g transform="translate(180, 50)">
<polygon points="50,0 100,28 50,56 0,28" fill="url(#cubeTop2)" stroke="#C7D2FE" stroke-width="1.5"/>
<polygon points="0,28 50,56 50,116 0,88" fill="url(#cubeLeft2)" stroke="rgba(129,140,248,0.5)" stroke-width="1.5"/>
<polygon points="50,56 100,28 100,88 50,116" fill="url(#cubeRight2)" stroke="rgba(192,132,252,0.5)" stroke-width="1.5"/>
<text x="24" y="82" font-size="28" font-weight="900" fill="#FFFFFF" font-family="Inter, sans-serif" transform="skewY(28) scale(0.9, 1)">AI</text>
<path d="M 50,0 L 50,56 M 0,28 L 50,56 L 100,28" fill="none" stroke="#FFFFFF" stroke-width="1.8" opacity="0.7"/>
</g>
</svg>
</div>""", unsafe_allow_html=True)

        # Right Column (Glassmorphic Sign In Card)
        with col_right:
            st.markdown('<div class="auth-right-card morph-card-active">', unsafe_allow_html=True)
            
            # Top Icon
            st.markdown("""<div class="auth-card-top-icon"><span>A✦</span></div>""", unsafe_allow_html=True)

            if st.session_state["auth_mode"] == "Sign In":
                st.markdown('<div class="auth-card-title">Welcome Back! 👋</div>', unsafe_allow_html=True)
                st.markdown('<div class="auth-card-subtitle">Sign in to continue your career journey</div>', unsafe_allow_html=True)
            elif st.session_state["auth_mode"] == "Sign Up":
                st.markdown('<div class="auth-card-title">Create Account</div>', unsafe_allow_html=True)
                st.markdown('<div class="auth-card-subtitle">Join thousands accelerating their career with AI</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="auth-card-title">Reset Password</div>', unsafe_allow_html=True)
                st.markdown('<div class="auth-card-subtitle">Enter your registered details to set a new password</div>', unsafe_allow_html=True)

            # Segmented Toggle (Sign In / Sign Up)
            if st.session_state["auth_mode"] in ["Sign In", "Sign Up"]:
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    is_signin = (st.session_state["auth_mode"] == "Sign In")
                    if st.button("Sign In", key="btn_toggle_signin", type="primary" if is_signin else "secondary", use_container_width=True):
                        st.session_state["auth_mode"] = "Sign In"
                        st.rerun()
                with col_t2:
                    is_signup = (st.session_state["auth_mode"] == "Sign Up")
                    if st.button("Sign Up", key="btn_toggle_signup", type="primary" if is_signup else "secondary", use_container_width=True):
                        st.session_state["auth_mode"] = "Sign Up"
                        st.rerun()

            # --- SIGN IN VIEW ---
            if st.session_state["auth_mode"] == "Sign In":
                st.markdown('<div class="auth-input-label">USERNAME OR EMAIL</div>', unsafe_allow_html=True)
                l_user = st.text_input("Username or Email", placeholder="👤  Enter your email or username", key="auth_l_user", label_visibility="collapsed")
                
                col_lp1, col_lp2 = st.columns([1.5, 1])
                with col_lp1:
                    st.markdown('<div class="auth-input-label">PASSWORD</div>', unsafe_allow_html=True)
                with col_lp2:
                    if st.button("Forgot Password?", key="btn_forgot_pass"):
                        st.session_state["auth_mode"] = "Reset"
                        st.rerun()

                l_pass = st.text_input("Password", type="password", placeholder="🔒  Enter your password", key="auth_l_pass", label_visibility="collapsed")
                
                col_rem1, col_rem2 = st.columns([1, 1])
                with col_rem1:
                    st.checkbox("Remember me", value=True, key="chk_remember_me")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Sign In →", key="btn_submit_signin", type="primary", use_container_width=True):
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

                st.markdown('<div class="auth-divider-row"><span>or continue with</span></div>', unsafe_allow_html=True)

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    if st.button("🔴 Alex Rivera (Data Science)", key="demo_alex_btn", use_container_width=True):
                        auth_res = AuthService.sign_in("alex_rivera", "demo123")
                        if not auth_res["success"]:
                            AuthService.sign_up("alex_rivera", "demo123", "Alex Rivera", "United States")
                            auth_res = AuthService.sign_in("alex_rivera", "demo123")
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = auth_res
                        st.session_state["active_view"] = "nav_dashboard"
                        st.rerun()
                with col_d2:
                    if st.button("🔵 Sam Chen (Developer)", key="demo_sam_btn", use_container_width=True):
                        auth_res = AuthService.sign_in("sam_chen", "demo123")
                        if not auth_res["success"]:
                            AuthService.sign_up("sam_chen", "demo123", "Sam Chen", "Canada")
                            auth_res = AuthService.sign_in("sam_chen", "demo123")
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = auth_res
                        st.session_state["target_role"] = "Software Engineer (Full-Stack)"
                        st.session_state["active_view"] = "nav_dashboard"
                        st.rerun()

                st.markdown("<div style='text-align:center; margin-top:16px; font-size:0.86rem; color:#94A3B8;'>Don't have an account?</div>", unsafe_allow_html=True)
                if st.button("Create Account", key="btn_goto_signup", use_container_width=True):
                    st.session_state["auth_mode"] = "Sign Up"
                    st.rerun()

            # --- SIGN UP VIEW ---
            elif st.session_state["auth_mode"] == "Sign Up":
                st.markdown('<div class="auth-input-label">FULL NAME</div>', unsafe_allow_html=True)
                r_name = st.text_input("Full Name", placeholder="👤  Enter your full name", key="auth_r_name", label_visibility="collapsed")

                st.markdown('<div class="auth-input-label">USERNAME OR EMAIL</div>', unsafe_allow_html=True)
                r_user = st.text_input("Username", placeholder="✉️  Enter your username or email", key="auth_r_user", label_visibility="collapsed")

                st.markdown('<div class="auth-input-label">CHOOSE PASSWORD</div>', unsafe_allow_html=True)
                r_pass = st.text_input("Password", type="password", placeholder="🔒  At least 6 characters", key="auth_r_pass", label_visibility="collapsed")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Create Account →", key="btn_submit_signup", type="primary", use_container_width=True):
                    reg_res = AuthService.sign_up(r_user, r_pass, r_name)
                    if reg_res["success"]:
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = reg_res
                        st.session_state["onboarding_step"] = 1
                        st.session_state["active_view"] = "onboarding"
                        st.rerun()
                    else:
                        st.error(reg_res["message"])

                st.markdown("<div style='text-align:center; margin-top:16px; font-size:0.86rem; color:#94A3B8;'>Already have an account?</div>", unsafe_allow_html=True)
                if st.button("Sign In Instead", key="btn_goto_signin", use_container_width=True):
                    st.session_state["auth_mode"] = "Sign In"
                    st.rerun()

            # --- RESET PASSWORD VIEW ---
            elif st.session_state["auth_mode"] == "Reset":
                st.markdown('<div class="auth-input-label">USERNAME OR EMAIL</div>', unsafe_allow_html=True)
                rst_user = st.text_input("Username", placeholder="✉️  Enter your registered username", key="auth_rst_user", label_visibility="collapsed")

                st.markdown('<div class="auth-input-label">NEW PASSWORD</div>', unsafe_allow_html=True)
                rst_pass = st.text_input("New Password", type="password", placeholder="🔒  Enter new password", key="auth_rst_pass", label_visibility="collapsed")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Update Password →", key="btn_submit_reset", type="primary", use_container_width=True):
                    rst_res = AuthService.reset_password(rst_user, rst_pass)
                    if rst_res["success"]:
                        st.success(rst_res["message"])
                        st.session_state["auth_mode"] = "Sign In"
                        st.rerun()
                    else:
                        st.error(rst_res["message"])

                if st.button("⬅ Back to Sign In", key="btn_reset_back_signin", use_container_width=True):
                    st.session_state["auth_mode"] = "Sign In"
                    st.rerun()

            # Security note
            st.markdown('<div class="auth-security-footer">🛡️ Your data is secure with us. We never share your information.</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 6. Authenticated User Flow
user_info = st.session_state.get("user_info")
if not user_info:
    st.stop()

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
