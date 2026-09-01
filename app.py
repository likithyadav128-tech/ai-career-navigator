"""
AI Career Intelligence & Job Readiness OS - Main Streamlit Application
Comprehensive, real-time job readiness and skill tracking system for students & developers.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.sample_data import SAMPLE_RESUMES, SAMPLE_JOB_DESCRIPTIONS
from modules.user_auth_db import (
    register_user, authenticate_user, save_user_profile, load_user_profile
)
from modules.resume_analyzer import (
    extract_text_from_pdf, extract_skills_from_text, evaluate_resume_quality, SKILL_TAXONOMY
)
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

st.set_page_config(
    page_title="AI Career Intelligence & Job Readiness OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ===== GLOBAL DARK CANVAS ===== */
    .stApp {
        background: linear-gradient(160deg, #0a0e1a 0%, #0d1225 40%, #111827 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1629 0%, #131b36 100%) !important;
        border-right: 1px solid rgba(108, 99, 255, 0.15) !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] .stDivider {
        border-color: rgba(108, 99, 255, 0.15) !important;
    }

    /* ===== INPUT CONTROLS ===== */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(108, 99, 255, 0.25) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] * { color: #e2e8f0 !important; }
    textarea, input[type="text"], input[type="password"] {
        background: rgba(255,255,255,0.04) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(108, 99, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    textarea:focus, input:focus {
        border-color: rgba(108, 99, 255, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1) !important;
    }

    /* ===== HEADER BANNER ===== */
    .hero-banner {
        background: linear-gradient(135deg, #1a1145 0%, #0f1629 30%, #0c2340 60%, #162050 100%);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; right: -30%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(108, 99, 255, 0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        bottom: -40%; left: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner h1 {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    .hero-banner p {
        font-size: 1rem !important;
        color: #94a3b8 !important;
        margin-top: 8px !important;
        margin-bottom: 0 !important;
        position: relative;
        z-index: 1;
    }
    .hero-banner strong { color: #a5b4fc !important; }

    /* ===== GLASS METRIC CARDS ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        margin-bottom: 16px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(108, 99, 255, 0.35);
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.08);
    }
    .glass-card .card-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .glass-card .card-value {
        font-size: 2.4rem;
        font-weight: 800;
        margin-top: 4px;
    }

    /* ===== GLASS CONTENT BOXES ===== */
    .glass-box {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }

    /* ===== SKILL BADGES ===== */
    .badge-strong {
        background: rgba(16, 185, 129, 0.12) !important;
        color: #34d399 !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-moderate {
        background: rgba(245, 158, 11, 0.12) !important;
        color: #fbbf24 !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-missing {
        background: rgba(239, 68, 68, 0.12) !important;
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-bonus {
        background: rgba(108, 99, 255, 0.12) !important;
        color: #a5b4fc !important;
        border: 1px solid rgba(108, 99, 255, 0.3) !important;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }

    /* ===== SCORE BOOSTER CARDS ===== */
    .booster-item {
        border-left: 3px solid #6C63FF;
        padding-left: 14px;
        margin-bottom: 14px;
    }
    .booster-item h4 {
        margin: 0;
        color: #a5b4fc !important;
        font-size: 0.95rem;
    }
    .booster-item .pts-tag {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .booster-item p {
        color: #64748b !important;
        margin: 4px 0 0 0;
        font-size: 0.88rem;
    }

    /* ===== MISSION CARDS ===== */
    .mission-card {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(108, 99, 255, 0.12);
        border-left: 4px solid #6C63FF;
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 16px;
    }
    .mission-card h3 { margin: 0; color: #e2e8f0 !important; font-size: 1.05rem; }
    .mission-card p { color: #94a3b8 !important; margin-top: 8px; }

    /* ===== QUESTION CARD ===== */
    .question-card {
        background: rgba(108, 99, 255, 0.06);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-left: 5px solid #6C63FF;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
    }

    /* ===== HIERARCHY SKILL ROW ===== */
    .skill-row {
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        padding: 12px 0;
    }
    .skill-row h4 { margin: 0; color: #e2e8f0 !important; }
    .skill-row p { color: #64748b !important; margin: 4px 0 0 0; font-size: 0.88rem; }

    /* ===== TOP PADDING & VIEWPORT OPTIMIZATION ===== */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1320px !important;
        margin: 0 auto !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    /* ===== AI RESUME CAREER NAVIGATOR STYLES ===== */
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

    /* Right Column Direct Glassmorphic Card Container */
    [data-testid="column"]:nth-of-type(2) {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(139, 92, 246, 0.25) !important;
        border-radius: 28px !important;
        padding: 30px 28px !important;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.7), 0 0 40px rgba(108, 99, 255, 0.08) !important;
    }

    .auth-card-top-icon {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border: 1px solid rgba(139, 92, 246, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.35);
    }

    .auth-card-top-icon span {
        font-size: 1.7rem;
        font-weight: 900;
        background: linear-gradient(135deg, #818CF8, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .auth-card-title {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-align: center;
        margin: 0 0 4px 0 !important;
    }

    .auth-card-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 24px;
    }

    .auth-nav-tabs {
        display: flex;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .auth-nav-item {
        flex: 1;
        text-align: center;
        padding: 10px 0;
        font-size: 0.95rem;
        font-weight: 600;
        color: #94a3b8;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .auth-nav-item.active {
        background: rgba(99, 102, 241, 0.25);
        color: #ffffff;
        border-bottom: 2px solid #818CF8;
    }

    .auth-input-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
        margin-top: 14px;
    }

    .auth-divider-row {
        display: flex;
        align-items: center;
        margin: 20px 0 16px 0;
        color: #64748b;
        font-size: 0.82rem;
    }

    .auth-divider-row::before, .auth-divider-row::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
    }

    .auth-divider-row span {
        padding: 0 12px;
    }

    .auth-security-footer {
        text-align: center;
        margin-top: 24px;
        color: #64748b;
        font-size: 0.78rem;
        line-height: 1.5;
    }

    /* Custom Streamlit Button Styling inside Auth */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #7C3AED 50%, #A855F7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.6) !important;
    }

    /* Custom Text Inputs */
    div[data-baseweb="input"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None

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

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hi! I'm your AI Career Assistant. Ask me anything like:\n- *'What should I learn next?'*\n- *'Am I ready for a Data Analyst role?'*\n- *'Which skills should I add to my resume?'*"}
    ]

# Authentication Guard
if not st.session_state["logged_in"]:
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "Sign In"
    
    brand_col, form_col = st.columns([1.15, 0.85], gap="large")

    # ==========================================
    # LEFT COLUMN: BRANDING, FEATURES & 3D GRAPHIC
    # ==========================================
    with brand_col:
        st.markdown("""<div>
<!-- Brand Badge -->
<div class="brand-logo-badge">
<div class="brand-logo-icon">
<span>A<sup style="font-size:0.75rem;">✦</sup></span>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 800; color: #FFFFFF; letter-spacing: 2px; line-height: 1.2;">AI RESUME</div>
<div style="font-size: 0.70rem; font-weight: 700; color: #818CF8; letter-spacing: 1.5px;">CAREER NAVIGATOR</div>
</div>
</div>

<!-- Main Titles -->
<h1 class="brand-title-main">AI Resume</h1>
<div class="brand-title-gradient">Career Navigator</div>

<div class="brand-subtitle-text">
Navigate your career. Build your future.<br>
Powered by AI.
</div>

<!-- 3 Core Features -->
<div style="margin-bottom: 20px;">
<!-- Feature 1 -->
<div class="feature-item-card">
<div class="feature-icon-box" style="color: #38BDF8;">🧠</div>
<div>
<div class="feature-text-title">AI Powered Resume Analysis</div>
<div class="feature-text-desc">Get AI-driven insights to improve your resume and skills.</div>
</div>
</div>

<!-- Feature 2 -->
<div class="feature-item-card">
<div class="feature-icon-box" style="color: #C084FC;">🎯</div>
<div>
<div class="feature-text-title">ATS Score Optimization</div>
<div class="feature-text-desc">Optimize your resume for ATS and increase interview chances.</div>
</div>
</div>

<!-- Feature 3 -->
<div class="feature-item-card">
<div class="feature-icon-box" style="color: #60A5FA;">📈</div>
<div>
<div class="feature-text-title">Personalized Career Guidance</div>
<div class="feature-text-desc">Discover the best career paths and opportunities for you.</div>
</div>
</div>
</div>

<!-- 3D Glowing ATS Resume & Growth Graph Graphic -->
<div style="position: relative; width: 100%; max-width: 420px; margin-top: 4px;">
<svg viewBox="0 0 440 200" width="100%" height="100%" style="overflow: visible; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.6));">
<defs>
<linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#3B82F6" stop-opacity="0.8"/>
<stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.9"/>
</linearGradient>
<linearGradient id="barGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#60A5FA"/>
<stop offset="100%" stop-color="#1D4ED8"/>
</linearGradient>
<linearGradient id="barGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#818CF8"/>
<stop offset="100%" stop-color="#4338CA"/>
</linearGradient>
<linearGradient id="barGrad3" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#C084FC"/>
<stop offset="100%" stop-color="#7E22CE"/>
</linearGradient>
<linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#38BDF8"/>
<stop offset="100%" stop-color="#A855F7"/>
</linearGradient>
<radialGradient id="platformGlow" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#6366F1" stop-opacity="0.4"/>
<stop offset="100%" stop-color="#0F172A" stop-opacity="0"/>
</radialGradient>
</defs>

<!-- Platform Glow Base -->
<ellipse cx="220" cy="165" rx="180" ry="30" fill="url(#platformGlow)"/>
<ellipse cx="220" cy="165" rx="150" ry="24" fill="none" stroke="rgba(99, 102, 241, 0.3)" stroke-width="1.5"/>

<!-- Left Isometric Resume Card -->
<g transform="translate(60, 15) rotate(-4)">
<rect x="0" y="0" width="150" height="140" rx="16" fill="url(#cardGrad)" stroke="rgba(147, 197, 253, 0.4)" stroke-width="2"/>
<rect x="16" y="16" width="36" height="36" rx="10" fill="rgba(255,255,255,0.15)"/>
<circle cx="34" cy="30" r="9" fill="#93C5FD"/>
<path d="M23 48 Q34 38 45 48" fill="#93C5FD"/>
<rect x="62" y="20" width="68" height="6" rx="3" fill="#FFFFFF" opacity="0.9"/>
<rect x="62" y="32" width="46" height="5" rx="2.5" fill="#93C5FD" opacity="0.6"/>
<text x="16" y="72" font-size="11" fill="#FBBF24">★★★★★</text>
<rect x="16" y="86" width="118" height="5.5" rx="2.7" fill="rgba(255,255,255,0.1)"/>
<rect x="16" y="86" width="92" height="5.5" rx="2.7" fill="#38BDF8"/>
<rect x="16" y="100" width="118" height="5.5" rx="2.7" fill="rgba(255,255,255,0.1)"/>
<rect x="16" y="100" width="106" height="5.5" rx="2.7" fill="#A855F7"/>
<rect x="16" y="114" width="118" height="5.5" rx="2.7" fill="rgba(255,255,255,0.1)"/>
<rect x="16" y="114" width="76" height="5.5" rx="2.7" fill="#34D399"/>
</g>

<!-- Right Isometric 3D Analytics Bars -->
<g transform="translate(235, 40)">
<rect x="15" y="75" width="20" height="60" rx="5" fill="url(#barGrad1)"/>
<ellipse cx="25" cy="75" rx="10" ry="4.5" fill="#93C5FD"/>
<rect x="48" y="50" width="20" height="85" rx="5" fill="url(#barGrad2)"/>
<ellipse cx="58" cy="50" rx="10" ry="4.5" fill="#C7D2FE"/>
<rect x="81" y="25" width="20" height="110" rx="5" fill="url(#barGrad3)"/>
<ellipse cx="91" cy="25" rx="10" ry="4.5" fill="#E9D5FF"/>
<path d="M-10 70 Q25 35 58 20 T115 -8" fill="none" stroke="url(#lineGrad)" stroke-width="3" stroke-linecap="round"/>
<circle cx="-10" cy="70" r="4.5" fill="#38BDF8" filter="drop-shadow(0 0 6px #38BDF8)"/>
<circle cx="25" cy="48" r="4.5" fill="#60A5FA" filter="drop-shadow(0 0 6px #60A5FA)"/>
<circle cx="58" cy="20" r="5" fill="#A855F7" filter="drop-shadow(0 0 8px #A855F7)"/>
<circle cx="100" cy="2" r="5.5" fill="#F472B6" filter="drop-shadow(0 0 10px #F472B6)"/>
</g>
</svg>
</div>
</div>""", unsafe_allow_html=True)

    # ==========================================
    # RIGHT COLUMN: SLEEK GLASSMORPHIC LOGIN CARD
    # ==========================================
    with form_col:
        st.markdown("""
<div class="auth-card-top-icon">
<span>A<sup style="font-size:0.9rem;">✦</sup></span>
</div>""", unsafe_allow_html=True)

        if st.session_state["auth_mode"] == "Sign In":
            st.markdown("""<div class="auth-card-title">Welcome back!</div>
<div class="auth-card-subtitle">Sign in to continue your career journey</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="auth-card-title">Create Account</div>
<div class="auth-card-subtitle">Join the AI career operating system</div>""", unsafe_allow_html=True)

        # Tab Switcher inside the card
        col_tab1, col_tab2 = st.columns(2)
        with col_tab1:
            if st.button("Sign In", key="btn_switch_signin", use_container_width=True, 
                         type="primary" if st.session_state["auth_mode"] == "Sign In" else "secondary"):
                st.session_state["auth_mode"] = "Sign In"
                st.rerun()
        with col_tab2:
            if st.button("Sign Up", key="btn_switch_signup", use_container_width=True,
                         type="primary" if st.session_state["auth_mode"] == "Sign Up" else "secondary"):
                st.session_state["auth_mode"] = "Sign Up"
                st.rerun()

        # FORM FIELDS
        if st.session_state["auth_mode"] == "Sign In":
            st.markdown('<div class="auth-input-label">EMAIL / USERNAME</div>', unsafe_allow_html=True)
            login_user = st.text_input("Username", label_visibility="collapsed", key="auth_user_in", placeholder="✉️  Enter your email or username")

            st.markdown('<div style="display:flex; justify-content:space-between; align-items:center;">'
                        '<span class="auth-input-label">PASSWORD</span>'
                        '<span style="font-size:0.78rem; color:#818CF8; font-weight:600; cursor:pointer;">Forgot password?</span>'
                        '</div>', unsafe_allow_html=True)
            login_pass = st.text_input("Password", label_visibility="collapsed", type="password", key="auth_pass_in", placeholder="🔒  Enter your password")

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # Main Submit Button
            if st.button("➔  Sign In", type="primary", use_container_width=True):
                auth_res = authenticate_user(login_user, login_pass)
                if auth_res["success"]:
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = auth_res
                    prof = load_user_profile(auth_res["user_id"])
                    if prof["has_profile"]:
                        st.session_state["target_role"] = prof["target_role"]
                        st.session_state["target_company"] = prof["target_company"]
                        st.session_state["candidate_text"] = prof["candidate_text"]
                        st.session_state["candidate_skills"] = prof["candidate_skills"]
                        st.session_state["github_user"] = prof["github_user"] or "arivera"
                    st.success(f"Welcome back, {auth_res['full_name']}!")
                    st.rerun()
                else:
                    st.error(auth_res["message"])

            # Divider
            st.markdown('<div class="auth-divider-row"><span>or continue with</span></div>', unsafe_allow_html=True)

            # Quick Demo Accounts (Google / Demo buttons)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                if st.button("🔴 Alex (Data Science)", key="quick_alex", use_container_width=True):
                    auth_res = authenticate_user("alex_rivera", "demo123")
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = auth_res
                    st.rerun()
            with col_g2:
                if st.button("🔵 Sam (Developer)", key="quick_sam", use_container_width=True):
                    auth_res = authenticate_user("sam_chen", "demo123")
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = auth_res
                    default_res = SAMPLE_RESUMES["Software & Web Developer (Sam Chen)"]
                    st.session_state["candidate_text"] = default_res["text"]
                    st.session_state["candidate_skills"] = default_res["extracted_skills"]
                    st.session_state["target_role"] = "Full-Stack Developer"
                    st.rerun()

            # Switch link
            st.markdown("""<div style="text-align:center; margin-top:16px; font-size:0.85rem; color:#94a3b8;">
Don't have an account? <span style="color:#818CF8; font-weight:700;">Sign Up</span>
</div>""", unsafe_allow_html=True)

        else:
            # SIGN UP MODE
            st.markdown('<div class="auth-input-label">FULL NAME</div>', unsafe_allow_html=True)
            reg_name = st.text_input("Full Name", label_visibility="collapsed", key="reg_name_in", placeholder="👤  Enter your full name")

            st.markdown('<div class="auth-input-label">CHOOSE USERNAME / EMAIL</div>', unsafe_allow_html=True)
            reg_user = st.text_input("Username", label_visibility="collapsed", key="reg_user_in", placeholder="✉️  Enter your username or email")

            st.markdown('<div class="auth-input-label">CHOOSE PASSWORD</div>', unsafe_allow_html=True)
            reg_pass = st.text_input("Password", label_visibility="collapsed", type="password", key="reg_pass_in", placeholder="🔒  Enter a secure password")

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            if st.button("➔  Create Account", type="primary", use_container_width=True):
                reg_res = register_user(reg_user, reg_pass, reg_name)
                if reg_res["success"]:
                    st.success("✅ Account created! Signing in...")
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = {"user_id": reg_res["user_id"], "username": reg_res["username"], "full_name": reg_res["full_name"]}
                    st.rerun()
                else:
                    st.error(reg_res["message"])

            st.markdown("""<div style="text-align:center; margin-top:16px; font-size:0.85rem; color:#94a3b8;">
Already have an account? <span style="color:#818CF8; font-weight:700;">Sign In</span>
</div>""", unsafe_allow_html=True)

        # Security Footnote
        st.markdown("""<div class="auth-security-footer">
🛡️ Your data is secure with us.<br>
We never share your information.
</div>""", unsafe_allow_html=True)

    st.stop()

# Sidebar (logged-in state)
user_info = st.session_state["user_info"]

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 12px 0 18px 0;">
        <div style="font-size: 2.6rem;">🎯</div>
        <h2 style="margin: 0; color: #ffffff !important; font-size: 1.3rem;">AI Career OS</h2>
        <p style="color: #6C63FF !important; font-size: 0.9rem; font-weight: 700; margin-top: 4px;">👤 {user_info['full_name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user_info"] = None
        st.rerun()
        
    st.divider()
    
    st.title("⚙️ Profile & Targeting")
    
    st.subheader("1. Target Role & Company")
    role_keys = list(ROLE_TAXONOMY.keys())
    sel_role = st.selectbox("Target Job Role:", role_keys, index=role_keys.index(st.session_state["target_role"]) if st.session_state["target_role"] in role_keys else 0)
    st.session_state["target_role"] = sel_role

    company_keys = list(COMPANY_PROFILES.keys())
    sel_company = st.selectbox("Target Company:", company_keys, index=0)
    st.session_state["target_company"] = sel_company

    st.divider()

    st.subheader("2. Resume Source & Skills")
    sample_res_choice = st.selectbox(
        "Load Profile:",
        ["Custom Upload / Input", "Data Science Student (Alex Rivera)", "Software & Web Developer (Sam Chen)"]
    )
    
    if sample_res_choice != "Custom Upload / Input":
        st.session_state["candidate_text"] = SAMPLE_RESUMES[sample_res_choice]["text"]
        st.session_state["candidate_skills"] = list(SAMPLE_RESUMES[sample_res_choice]["extracted_skills"])
    else:
        uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"])
        if uploaded_pdf is not None:
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            st.session_state["candidate_text"] = pdf_text
            extracted = extract_skills_from_text(pdf_text)
            st.session_state["candidate_skills"] = sorted(list(set(st.session_state.get("candidate_skills", []) + extracted)))
        else:
            resume_text_input = st.text_area("Or Paste Resume Text / Skill List:", value=st.session_state["candidate_text"], height=130)
            if resume_text_input != st.session_state["candidate_text"]:
                st.session_state["candidate_text"] = resume_text_input
                st.session_state["candidate_skills"] = extract_skills_from_text(resume_text_input)

    # Direct Skill Selector / Manager
    all_known_skills = sorted(list(set(SKILL_TAXONOMY.values())))
    selected_skill_list = st.multiselect(
        "Manage Mastered Skills:",
        options=all_known_skills,
        default=[s for s in st.session_state["candidate_skills"] if s in all_known_skills],
        help="Add or remove any skills you know. Changes immediately recalculate your Job Readiness and Skill Hierarchy Tree."
    )
    st.session_state["candidate_skills"] = sorted(list(set(selected_skill_list)))

    st.divider()

    st.subheader("3. GitHub")
    gh_input = st.text_input("GitHub Username:", value=st.session_state["github_user"])
    if gh_input:
        st.session_state["github_user"] = gh_input

# Core analytics calculations
role_info = ROLE_TAXONOMY.get(st.session_state["target_role"], ROLE_TAXONOMY["Data Analyst"])
resume_eval = evaluate_resume_quality(st.session_state["candidate_text"], st.session_state["candidate_skills"])
jd_eval = analyze_job_description(st.session_state["target_jd_text"])

gap_eval = analyze_skill_gaps(st.session_state["candidate_skills"], role_info["core_skills"])
semantic_sim = compute_semantic_cosine_similarity(st.session_state["candidate_text"], st.session_state["target_jd_text"])
github_res = verify_github_profile(st.session_state["github_user"])
hierarchy_analysis = analyze_hierarchical_skill_tree(st.session_state["candidate_skills"], st.session_state["target_role"])

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

save_user_profile(
    user_id=user_info["user_id"],
    target_role=st.session_state["target_role"],
    target_company=st.session_state["target_company"],
    candidate_text=st.session_state["candidate_text"],
    candidate_skills=st.session_state["candidate_skills"],
    github_user=st.session_state["github_user"],
    readiness_score=readiness_eval["overall_readiness"]
)

daily_mission = generate_daily_career_mission(gap_eval["missing_skills"], gap_eval["moderate_skills"], st.session_state["target_role"])

# Hero Banner
st.markdown(f"""
<div class="hero-banner">
    <h1>🎯 AI Career Intelligence & Job Readiness OS</h1>
    <p>Student: <strong>{user_info['full_name']}</strong> • Role: <strong>{st.session_state['target_role']}</strong> • Company: <strong>{st.session_state['target_company'].split('(')[0]}</strong> • Readiness: <strong>{readiness_eval['overall_readiness']}%</strong></p>
</div>
""", unsafe_allow_html=True)

# 9 Tabs Layout
tabs = st.tabs([
    "🏆 Career Twin & Readiness",
    "🎯 Daily Mission",
    "📄 Resume & Job Matcher",
    "📊 Skill Hierarchy",
    "🗺️ AI Roadmap",
    "💡 Project Auditor",
    "🎤 Interview Simulator",
    "🧭 Career Route Simulator",
    "🤖 AI Assistant"
])

# TAB 1: Career Twin & Readiness
with tabs[0]:
    st.header(f"🏆 Personal Career Twin — {user_info['full_name']}")
    st.markdown(f"Tracking digital twin for **{st.session_state['target_role']}** targeting **{st.session_state['target_company']}**.")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="glass-card"><div class="card-label">Overall Readiness</div><div class="card-value" style="color: #34d399;">{readiness_eval["overall_readiness"]}%</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="glass-card"><div class="card-label">Resume ATS Score</div><div class="card-value" style="color: #6C63FF;">{resume_eval["score"]}/100</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="glass-card"><div class="card-label">Technical Match</div><div class="card-value" style="color: #fbbf24;">{gap_eval["readiness_score"]}%</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="glass-card"><div class="card-label">GitHub Badge</div><div class="card-value" style="font-size: 1.1rem; color: #6C63FF;">{github_res.get("status_badge", "⚡ Active Dev")}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_twin1, col_twin2 = st.columns([1.1, 1])
    
    with col_twin1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Transparent 7-Factor Breakdown")
        for factor_name, factor_val in readiness_eval["factors"].items():
            col_f1, col_f2 = st.columns([3, 1])
            with col_f1:
                st.write(f"**{factor_name}** ({int(readiness_eval['weights'][factor_name]*100)}% weight)")
                st.progress(factor_val / 100)
            with col_f2:
                st.markdown(f"<h3 style='margin:0; text-align:right;'>{factor_val}%</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_twin2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### ⚡ What Will Increase My Score?")
        st.caption("AI-powered score improvement recommendations:")
        for booster in readiness_eval["score_boosters"]:
            st.markdown(f'<div class="booster-item"><h4>{booster["action"]} <span class="pts-tag">{booster["points"]}</span></h4><p>{booster["task"]}</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    gauge_fig = create_readiness_gauge(readiness_eval["overall_readiness"])
    st.plotly_chart(gauge_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Daily Mission
with tabs[1]:
    st.header("🎯 Today's Career Mission")
    st.markdown(f"**Time:** `{daily_mission['estimated_time']}` | **Potential Boost:** `{daily_mission['potential_boost']}`")
    st.info("💡 Completing daily missions updates your readiness score!")
    
    for task in daily_mission["tasks"]:
        st.markdown(f'<div class="mission-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3>{task["title"]}</h3><span class="badge-strong">{task["points"]}</span></div><p>{task["description"]}</p><p><strong>⏱️</strong> <code>{task["time_estimate"]}</code> | <strong>Category:</strong> <code>{task["category"]}</code></p></div>', unsafe_allow_html=True)
        st.checkbox(f"Mark {task['title']} as completed", key=f"daily_chk_{task['id']}")

# TAB 3: Resume & Job Matcher
with tabs[2]:
    st.header("📄 Resume & Job Description Matcher")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown(f"### ATS Resume Quality: **{resume_eval['score']}/100**")
        st.progress(resume_eval['score'] / 100)
        st.markdown("#### Quality Checklist:")
        for k, v in resume_eval["checks"].items():
            st.markdown(f"- **{k}**: `{v}`")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_m2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown(f"### Semantic Cosine Similarity: **{semantic_sim}%**")
        st.progress(semantic_sim / 100)
        st.markdown("Contextual overlap between resume and target job description.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("### ✨ AI Resume Bullet Rewriter (STAR Method)")
    user_bullet = st.text_input("Paste any weak bullet point:", value="Worked on customer churn prediction model using Python")
    if st.button("🚀 Optimize Bullet Point"):
        opt_res = optimize_resume_bullet(user_bullet, st.session_state["target_role"])
        st.success("✅ **STAR Method Optimized Bullet Point:**")
        st.code(opt_res["optimized"], language="text")
        st.caption(f"Action Verb: **{opt_res['action_verb']}** | Impact: **{opt_res['impact_metric']}**")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: Skill Hierarchy
with tabs[3]:
    st.header(f"📊 Skill Hierarchy — {st.session_state['target_role']}")
    st.markdown("**Mastered Skills** and **Next Learning Targets** based on prerequisite dependencies.")
    
    h_sum = hierarchy_analysis["summary"]
    hc1, hc2, hc3, hc4 = st.columns(4)
    with hc1:
        st.markdown(f'<div class="glass-card"><div class="card-label">Mastered</div><div class="card-value" style="color: #34d399;">{h_sum["mastered"]} / {h_sum["total_skills"]}</div></div>', unsafe_allow_html=True)
    with hc2:
        st.markdown(f'<div class="glass-card"><div class="card-label">Next Targets</div><div class="card-value" style="color: #6C63FF;">{h_sum["next_targets"]} Ready</div></div>', unsafe_allow_html=True)
    with hc3:
        st.markdown(f'<div class="glass-card"><div class="card-label">Blocked</div><div class="card-value" style="color: #f87171;">{h_sum["blocked"]} Skills</div></div>', unsafe_allow_html=True)
    with hc4:
        st.markdown(f'<div class="glass-card"><div class="card-label">Mastery %</div><div class="card-value" style="color: #fbbf24;">{round((h_sum["mastered"]/h_sum["total_skills"])*100, 1)}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if hierarchy_analysis["next_learning_targets"]:
        st.markdown('<div class="glass-box" style="border-left: 4px solid #6C63FF;">', unsafe_allow_html=True)
        st.markdown("### 🚀 What Should You Learn Next?")
        st.markdown("All prerequisites are met for these skills:")
        for tgt in hierarchy_analysis["next_learning_targets"]:
            prereq_str = f" (Prereqs met: {', '.join(tgt['prereqs'])})" if tgt['prereqs'] else " (Foundational)"
            st.markdown(f"- 🚀 **{tgt['skill']}** `[Level {tgt['level']} — {tgt['category']}]`{prereq_str}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🌲 Complete Skill Hierarchy Tree")
    level_titles = {
        1: "Level 1: Foundations & Prerequisites",
        2: "Level 2: Core Tools & Libraries",
        3: "Level 3: Advanced Modeling & Expertise",
        4: "Level 4: Production & Deployment"
    }
    for lvl in range(1, 5):
        items = hierarchy_analysis["levels"].get(lvl, [])
        if items:
            with st.expander(f"📍 {level_titles[lvl]} ({len(items)} Skills)", expanded=(lvl <= 2)):
                for sk in items:
                    badge_style = "badge-strong" if sk["status_code"] == "STRONG" else ("badge-bonus" if sk["status_code"] == "NEXT_TARGET" else "badge-missing")
                    st.markdown(f'<div class="skill-row"><div style="display:flex; justify-content:space-between; align-items:center;"><h4>{sk["status"].split()[0]} {sk["skill"]}</h4><span class="{badge_style}">{sk["status"]}</span></div><p>Category: <code>{sk["category"]}</code> | {sk["reason"]}</p></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🧪 Skill Verification Test")
    test_skill = st.selectbox("Select Skill:", ["SQL", "Python", "Power BI", "Machine Learning"])
    questions = get_assessment_for_skill(test_skill)
    user_ans = {}
    for idx, q in enumerate(questions):
        st.markdown(f"**Q{idx+1}: {q['question']}**")
        user_ans[idx] = st.radio(f"Answer Q{idx+1}:", range(len(q['options'])), format_func=lambda i: q['options'][i], key=f"q_{test_skill}_{idx}")
    if st.button(f"Submit {test_skill} Assessment"):
        eval_res = evaluate_skill_assessment(test_skill, user_ans, questions)
        st.session_state["verified_skills"][test_skill] = eval_res["verified_level"]
        st.success(f"🎉 Result: **{eval_res['verified_level']}** ({eval_res['verified_percentage']}% Score)")
        for d in eval_res["details"]:
            st.markdown(f"- {'✅' if d['is_correct'] else '❌'} {d['question']}")

# TAB 5: Dynamic AI Learning Roadmap
with tabs[4]:
    st.header("🗺️ Dynamic AI Learning Roadmap")
    st.markdown(f"Phased learning for **{st.session_state['target_role']}**.")
    roadmap_phases = generate_personalized_roadmap(gap_eval["missing_skills"], gap_eval["moderate_skills"], st.session_state["target_role"])
    for idx, phase in enumerate(roadmap_phases, 1):
        with st.expander(f"📍 {phase['phase']} | ⏱️ {phase['duration']}", expanded=(idx <= 2)):
            st.markdown(f"**Focus:** {phase['focus']}")
            st.markdown(f"**Topics:** `{', '.join(phase['topics'])}`")
            for step in phase["action_steps"]:
                st.checkbox(step, key=f"chk_rd_{idx}_{step[:12]}")

# TAB 6: Project Auditor & Builder
with tabs[5]:
    st.header("💡 Project Auditor & Builder")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🔍 7-Dimensional Project Auditor")
        p_name = st.text_input("Project Name:", value="Customer Churn Prediction Engine")
        p_tech = st.text_input("Tech Stack:", value="Python, XGBoost, Scikit-learn, Streamlit")
        p_desc = st.text_area("Description:", value="Built XGBoost churn classifier on 50k transaction logs achieving 89.2% ROC-AUC score.")
        has_dep = st.checkbox("Deployed to Live Server", value=True)
        has_doc = st.checkbox("Has README.md", value=True)
        if st.button("Audit Project"):
            audit_res = audit_project_strength(p_name, p_tech, p_desc, has_dep, has_doc)
            st.subheader(f"Score: **{audit_res['overall_score']}/100**")
            for c_name, c_score in audit_res["criteria"].items():
                st.write(f"**{c_name}:** {c_score}/100")
                st.progress(c_score / 100)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_p2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("### 🚀 Build Me a Better Project")
        blueprint = generate_flagship_project_blueprint(st.session_state["candidate_skills"], st.session_state["target_role"])
        st.markdown(f"#### **{blueprint['title']}**")
        st.markdown(f"**Difficulty:** `{blueprint['difficulty']}` | **Time:** `{blueprint['estimated_time']}`")
        st.markdown(f"**Dataset:** [{blueprint['dataset_name']}]({blueprint['dataset_link']})")
        st.markdown(f"**Description:** {blueprint['description']}")
        st.markdown("#### 📋 Tasks:")
        for t_idx, task_txt in enumerate(blueprint["tasks"], 1):
            st.markdown(f"{t_idx}. {task_txt}")
        with st.expander("📁 GitHub Structure & README"):
            st.code(blueprint["github_structure"], language="text")
            st.code(blueprint["readme_snippet"], language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 7: AI Interview Simulator
with tabs[6]:
    st.header("🎤 AI Interview Simulator")
    col_sim1, col_sim2 = st.columns([1, 1])
    with col_sim1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        int_mode = st.selectbox("Interview Mode:", ["HR / Cultural Fit", "Technical Deep-Dive", "Company-Specific", "Pressure Interview (Adaptive)"])
        sim_questions = get_questions_by_mode(int_mode, st.session_state["target_company"], st.session_state["target_role"])
        q_idx = st.selectbox("Question:", range(len(sim_questions)), format_func=lambda i: f"Q{i+1}: {sim_questions[i]['question'][:60]}...")
        q_item = sim_questions[q_idx]
        st.markdown(f'<div class="question-card"><h4>{q_item.get("category", int_mode)}</h4><h3 style="margin-top:8px;">"{q_item["question"]}"</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sim2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        user_answer = st.text_area("✍️ Your answer (STAR method):", height=150)
        if st.button("Submit Answer", type="primary"):
            if user_answer.strip():
                ans_eval = evaluate_student_answer(q_item, user_answer)
                comm_eval = evaluate_communication_intelligence(user_answer)
                st.subheader(f"Score: **{ans_eval['score']}/10**")
                st.write(f"**STAR Communication:** `{comm_eval['comm_score']}/100`")
                st.info(comm_eval["time_feedback"])
                st.markdown("#### STAR Detection:")
                for star_key, is_present in comm_eval["star_checklist"].items():
                    st.write(f"- {'✅' if is_present else '❌'} **{star_key}**")
            else:
                st.error("Please type an answer first.")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 8: Career Route Simulator
with tabs[7]:
    st.header("🧭 Career Route Simulator")
    st.markdown("Compare readiness across all 10 career tracks:")
    multi_sim = simulate_multi_role_readiness(st.session_state["candidate_skills"])
    df_sim = pd.DataFrame(multi_sim)
    fig_sim = px.bar(df_sim, x="role", y="readiness_score", color="readiness_score", color_continuous_scale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']], text="readiness_score")
    fig_sim.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'), xaxis=dict(gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    fig_sim.update_traces(textposition='outside')
    st.plotly_chart(fig_sim, use_container_width=True)
    
    st.markdown("### 🔄 Career Transition Calculator")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        c_role = st.selectbox("Current Role:", list(ROLE_TAXONOMY.keys()), index=0)
    with col_t2:
        t_role = st.selectbox("Target Role:", list(ROLE_TAXONOMY.keys()), index=1)
    delta_res = calculate_role_transition_delta(st.session_state["candidate_skills"], c_role, t_role)
    st.info(f"💡 **{c_role}** ({delta_res['current_readiness']}%) → **{t_role}** ({delta_res['target_readiness']}%) | Time: `{delta_res['estimated_transition_time']}`")
    st.write(f"**Missing Skills:** {', '.join(delta_res['missing_delta_skills']) if delta_res['missing_delta_skills'] else 'None! You meet all requirements.'}")

# TAB 9: AI Career Assistant
with tabs[8]:
    st.header("🤖 AI Career Assistant")
    p_col1, p_col2, p_col3 = st.columns(3)
    preset_clicked = None
    with p_col1:
        if st.button("💡 What should I learn next?"):
            preset_clicked = "What should I learn next?"
    with p_col2:
        if st.button("📊 Am I ready for this role?"):
            preset_clicked = "Am I ready for a Data Analyst role?"
    with p_col3:
        if st.button("📄 Which skills to add?"):
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
