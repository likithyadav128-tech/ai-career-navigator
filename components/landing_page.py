"""
Public Landing Page Component
Modern startup-grade landing page with hero, feature breakdown, interactive product journey, and FAQ.
"""
import streamlit as st
from config import APP_NAME, APP_TAGLINE, PRODUCT_JOURNEY, CAREER_TRACKS, LANDING_FAQ

def render_public_landing_page():
    """Renders the public startup landing page for non-logged in users."""
    
    # 1. Top Public Header
    col_nav1, col_nav2 = st.columns([1.8, 1])
    with col_nav1:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom: 24px;">
            <div style="width:44px; height:44px; border-radius:12px; background: linear-gradient(135deg, #6366F1, #A855F7, #EC4899); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 20px rgba(168,85,247,0.5);">
                <span style="color:#FFF; font-weight:900; font-size:1.35rem;">A✦</span>
            </div>
            <div>
                <div style="font-size:1.3rem; font-weight:900; color:#FFFFFF; letter-spacing:-0.5px;">{APP_NAME}</div>
                <div style="font-size:0.8rem; font-weight:700; color:#818CF8; letter-spacing:1px;">AI CAREER INTELLIGENCE OS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_nav2:
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Sign In", key="landing_top_signin", use_container_width=True):
                st.session_state["auth_mode"] = "Sign In"
                st.session_state["active_view"] = "auth"
                st.rerun()
        with col_btn2:
            if st.button("Get Started", key="landing_top_signup", type="primary", use_container_width=True):
                st.session_state["auth_mode"] = "Sign Up"
                st.session_state["active_view"] = "auth"
                st.rerun()

    # 2. Hero Section
    st.markdown("""
    <div style="background: radial-gradient(circle at 80% 20%, rgba(99,102,241,0.18) 0%, transparent 60%),
                            radial-gradient(circle at 20% 80%, rgba(236,72,153,0.12) 0%, transparent 50%),
                            linear-gradient(145deg, #0A0E1A 0%, #0F172A 50%, #111827 100%);
                border: 1px solid rgba(139,92,246,0.25); border-radius: 28px; padding: 50px 36px; text-align: center;
                margin-bottom: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); position: relative; overflow: hidden;">
        <div style="display:inline-flex; align-items:center; gap:8px; background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3); border-radius: 20px; padding: 6px 16px; margin-bottom: 20px;">
            <span style="color:#A855F7; font-size:0.9rem;">✨</span>
            <span style="font-size:0.85rem; font-weight:700; color:#C7D2FE; letter-spacing:0.5px;">The Operating System For Your Next Job</span>
        </div>
        <h1 style="font-size: 3.4rem !important; font-weight: 900 !important; color: #FFFFFF !important; line-height: 1.15 !important; margin: 0 0 16px 0 !important; letter-spacing: -1.5px;">
            Navigate Your Career With <span style="background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">AI Intelligence</span>
        </h1>
        <p style="font-size: 1.15rem; color: #94A3B8; max-width: 780px; margin: 0 auto 32px auto; line-height: 1.6;">
            Discover your high-growth career path, audit your prerequisite skill gaps, generate a personalized 8-stage roadmap, optimize your resume for ATS, and master technical & STAR behavioral interviews.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Hero Action Buttons
    col_cta1, col_cta2, col_cta3 = st.columns([1, 1.2, 1])
    with col_cta2:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("🚀 Build My Roadmap", key="hero_cta_roadmap", type="primary", use_container_width=True):
                st.session_state["auth_mode"] = "Sign Up"
                st.session_state["active_view"] = "auth"
                st.rerun()
        with col_c2:
            if st.button("🧭 Explore 14+ Careers", key="hero_cta_explore", use_container_width=True):
                st.session_state["auth_mode"] = "Sign In"
                st.session_state["active_view"] = "auth"
                st.rerun()

    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)

    # 3. Product Journey (9-Step Timeline)
    st.markdown("""
    <div style="text-align:center; margin-bottom: 24px;">
        <h2 style="font-size: 2rem; font-weight: 800; color: #FFFFFF !important; margin: 0 0 8px 0;">The 9-Step Career Launch Journey</h2>
        <p style="color: #94A3B8; font-size: 0.95rem;">From initial skill self-discovery to signing your top job offer.</p>
    </div>
    """, unsafe_allow_html=True)

    journey_cols = st.columns(len(PRODUCT_JOURNEY))
    for idx, (col, step_item) in enumerate(zip(journey_cols, PRODUCT_JOURNEY)):
        with col:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(99,102,241,0.15); border-radius: 14px; padding: 14px 10px; text-align: center; height: 100%;">
                <div style="font-size: 1.6rem; margin-bottom: 4px;">{step_item['icon']}</div>
                <div style="font-size: 0.85rem; font-weight: 800; color: #E2E8F0;">{step_item['name']}</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 4px;">Step {step_item['step']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # 4. Feature Spotlight Grid
    st.markdown("""
    <div style="text-align:center; margin-bottom: 28px;">
        <h2 style="font-size: 2rem; font-weight: 800; color: #FFFFFF !important; margin: 0 0 8px 0;">Engineered For Every Stage of Hiring</h2>
        <p style="color: #94A3B8; font-size: 0.95rem;">Everything you need to transform into a top 1% job candidate.</p>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">📄</div>
            <h3 style="color:#FFF !important; font-size: 1.2rem; font-weight: 800; margin:0 0 8px 0;">ATS Resume AI & STAR Rewriter</h3>
            <p style="color:#94A3B8 !important; font-size:0.9rem; line-height:1.5;">Evaluates formatting, contact density, and action verbs with instant STAR method bullet rewrites that demonstrate business impact.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">🗺️</div>
            <h3 style="color:#FFF !important; font-size: 1.2rem; font-weight: 800; margin:0 0 8px 0;">Dynamic 8-Stage Roadmap</h3>
            <p style="color:#94A3B8 !important; font-size:0.9rem; line-height:1.5;">A customized learning path generated based on your real prerequisite skill dependencies and timeline targets.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">🌳</div>
            <h3 style="color:#FFF !important; font-size: 1.2rem; font-weight: 800; margin:0 0 8px 0;">Skill Dependency Trees</h3>
            <p style="color:#94A3B8 !important; font-size:0.9rem; line-height:1.5;">Categorizes skills into Strong, Developing, and Next Immediate Learning Targets to eliminate guessing what to learn next.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">💡</div>
            <h3 style="color:#FFF !important; font-size: 1.2rem; font-weight: 800; margin:0 0 8px 0;">7D Project Auditor & Blueprints</h3>
            <p style="color:#94A3B8 !important; font-size:0.9rem; line-height:1.5;">Generate production-grade portfolio architectures with datasets, GitHub schemas, and README snippets that impress recruiters.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">🎤</div>
            <h3 style="color:#FFF !important; font-size: 1.2rem; font-weight: 800; margin:0 0 8px 0;">STAR Interview Simulation Lab</h3>
            <p style="color:#94A3B8 !important; font-size:0.9rem; line-height:1.5;">Practice Technical, HR, and Role-specific questions with real-time AI feedback on communication conciseness and STAR structure.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">💼</div>
            <h3 style="color:#FFF !important; font-size: 1.2rem; font-weight: 800; margin:0 0 8px 0;">Job Application Pipeline Tracker</h3>
            <p style="color:#94A3B8 !important; font-size:0.9rem; line-height:1.5;">Organize your job hunt with Kanban and List views across Saved, Applied, Screening, Interview, Offer, and Rejected statuses.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # 5. Career Tracks Preview
    st.markdown("""
    <div style="text-align:center; margin-bottom: 24px;">
        <h2 style="font-size: 2rem; font-weight: 800; color: #FFFFFF !important; margin: 0 0 8px 0;">Explore 14+ In-Demand Tech Tracks</h2>
        <p style="color: #94A3B8; font-size: 0.95rem;">Comprehensive taxonomies with real market salary ranges and interview guidelines.</p>
    </div>
    """, unsafe_allow_html=True)

    track_cols = st.columns(4)
    sample_tracks = list(CAREER_TRACKS.items())[:8]
    for idx, (t_name, t_info) in enumerate(sample_tracks):
        with track_cols[idx % 4]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 18px 14px; margin-bottom: 14px; text-align:center;">
                <div style="font-size: 1.8rem; margin-bottom: 6px;">{t_info['icon']}</div>
                <div style="font-weight: 800; color: #FFFFFF; font-size: 0.95rem; margin-bottom: 4px;">{t_name}</div>
                <div style="color: #34D399; font-size: 0.8rem; font-weight: 700;">{t_info['avg_salary']}</div>
                <div style="color: #64748B; font-size: 0.75rem; margin-top: 4px;">Demand: {t_info['demand_growth']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # 6. Frequently Asked Questions (FAQ)
    st.markdown("""
    <div style="text-align:center; margin-bottom: 24px;">
        <h2 style="font-size: 2rem; font-weight: 800; color: #FFFFFF !important; margin: 0 0 8px 0;">Frequently Asked Questions</h2>
        <p style="color: #94A3B8; font-size: 0.95rem;">Clear answers on how AI Career Navigator empowers your career journey.</p>
    </div>
    """, unsafe_allow_html=True)

    for item in LANDING_FAQ:
        with st.expander(f"❓ {item['q']}", expanded=False):
            st.markdown(f"<p style='color:#CBD5E1; line-height:1.6;'>{item['a']}</p>", unsafe_allow_html=True)

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # 7. Final Footer CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
                border: 1px solid rgba(139,92,246,0.4); border-radius: 24px; padding: 40px 30px; text-align: center; margin-bottom: 30px;">
        <h2 style="color: #FFFFFF !important; font-size: 2.2rem; font-weight: 900; margin: 0 0 12px 0;">Ready to Accelerate Your Career?</h2>
        <p style="color: #C7D2FE; font-size: 1.05rem; max-width: 600px; margin: 0 auto 24px auto;">
            Create your account in seconds and receive your personalized career readiness score and actionable next steps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_fcta1, col_fcta2, col_fcta3 = st.columns([1.2, 1, 1.2])
    with col_fcta2:
        if st.button("🚀 Start Free Today", key="btn_footer_signup", type="primary", use_container_width=True):
            st.session_state["auth_mode"] = "Sign Up"
            st.session_state["active_view"] = "auth"
            st.rerun()
            
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 12px 0; color: #64748B; font-size: 0.85rem; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 40px;">
        © 2026 AI Career Navigator. All rights reserved. Built for students, graduates & career switchers worldwide.
    </div>
    """, unsafe_allow_html=True)
