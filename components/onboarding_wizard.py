"""
5-Step Progressive Onboarding Wizard Component
Collects user profile, background, technical proficiencies, career aspirations, and work preferences.
"""
import streamlit as st
from config import CAREER_TRACKS
from modules.resume_analyzer import SKILL_TAXONOMY
from database.profile_repo import save_onboarding_data, save_user_profile

COUNTRIES = [
    "United States", "India", "United Kingdom", "Canada", "Germany", "Australia",
    "Singapore", "France", "Netherlands", "United Arab Emirates", "Brazil", "Japan", "Global / Other"
]

EDUCATION_LEVELS = [
    "Undergraduate Student (Pursuing Bachelor's)",
    "Recent College Graduate (Bachelor's Completed)",
    "Master's / Postgraduate Student",
    "PhD Candidate / Graduate",
    "Bootcamp Graduate / Self-Taught",
    "Working Professional (Career Switcher)"
]

EXPERIENCE_LEVELS = [
    "Student / Intern (0 years)",
    "Entry-Level Junior (0 - 2 years)",
    "Mid-Level Professional (2 - 5 years)",
    "Senior / Specialist (5+ years)"
]

WORK_PREFERENCES = [
    "Remote First (Anywhere)",
    "Hybrid (2-3 days office)",
    "On-Site (Full Office)",
    "Flexible / Open to all"
]

def render_onboarding_wizard(user_info: dict):
    """Renders the 5-step interactive onboarding flow."""
    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = 1

    curr_step = st.session_state["onboarding_step"]

    # Header and Progress Indicator
    st.markdown(f"""
    <div style="background: rgba(15,23,42,0.75); border: 1px solid rgba(139,92,246,0.3); border-radius: 24px; padding: 32px; max-width: 760px; margin: 20px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.5);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
            <div style="display:inline-flex; align-items:center; gap:8px;">
                <span style="font-size:1.4rem;">🎯</span>
                <span style="font-size:0.95rem; font-weight:800; color:#A78BFA; text-transform:uppercase; letter-spacing:1px;">Profile Setup</span>
            </div>
            <div style="font-size:0.85rem; font-weight:800; color:#34D399; background:rgba(16,185,129,0.15); padding:4px 12px; border-radius:12px; border:1px solid rgba(16,185,129,0.3);">
                Step {curr_step} of 5
            </div>
        </div>
        <div style="height:6px; background:rgba(255,255,255,0.08); border-radius:3px; margin-bottom: 24px; overflow:hidden;">
            <div style="height:100%; width: {curr_step * 20}%; background: linear-gradient(90deg, #6366F1, #A855F7, #EC4899); border-radius:3px; transition:width 0.3s ease;"></div>
        </div>
    """, unsafe_allow_html=True)

    # Step 1: Geography & Basic Details
    if curr_step == 1:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 1: Where are you located?</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>We personalize job market insights and salary benchmarks to your region.</p>", unsafe_allow_html=True)
        sel_country = st.selectbox("Your Country / Region:", COUNTRIES, index=COUNTRIES.index(user_info.get("country", "United States")) if user_info.get("country") in COUNTRIES else 0, key="ob_country")
        st.session_state["ob_data_country"] = sel_country

        col_b1, col_b2 = st.columns([1, 1])
        with col_b2:
            if st.button("Continue ➔", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = 2
                st.rerun()

    # Step 2: Education & Background
    elif curr_step == 2:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 2: Education & Experience Level</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Tell us about your educational background and work seniority.</p>", unsafe_allow_html=True)
        edu = st.selectbox("Highest Education Level:", EDUCATION_LEVELS, key="ob_edu")
        field = st.text_input("Degree Field / Major:", value="Computer Science / Data Analytics", placeholder="e.g. Computer Science, Information Systems, Business", key="ob_field")
        exp = st.selectbox("Current Experience Level:", EXPERIENCE_LEVELS, key="ob_exp")

        st.session_state["ob_data_edu"] = edu
        st.session_state["ob_data_field"] = field
        st.session_state["ob_data_exp"] = exp

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅ Back"):
                st.session_state["onboarding_step"] = 1
                st.rerun()
        with col_b2:
            if st.button("Continue ➔", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = 3
                st.rerun()

    # Step 3: Technical Skills
    elif curr_step == 3:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 3: What skills do you already have?</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Select any programming languages, tools, or frameworks you are familiar with.</p>", unsafe_allow_html=True)
        all_skills = sorted(list(set(SKILL_TAXONOMY.values())))
        default_skills = [s for s in st.session_state.get("candidate_skills", ["SQL", "Python", "Excel"]) if s in all_skills]
        
        sel_skills = st.multiselect("Select Known Skills:", options=all_skills, default=default_skills, key="ob_skills")
        st.session_state["candidate_skills"] = sel_skills

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅ Back"):
                st.session_state["onboarding_step"] = 2
                st.rerun()
        with col_b2:
            if st.button("Continue ➔", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = 4
                st.rerun()

    # Step 4: Target Career & Interests
    elif curr_step == 4:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 4: Target Career & Interests</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Select your primary dream role and topics that excite you.</p>", unsafe_allow_html=True)
        career_list = list(CAREER_TRACKS.keys())
        target_role = st.selectbox("Primary Target Role:", career_list, index=career_list.index(st.session_state.get("target_role", "Data Analyst")) if st.session_state.get("target_role") in career_list else 0, key="ob_role")
        st.session_state["target_role"] = target_role

        interests = st.multiselect(
            "Industry Interests:",
            options=["Artificial Intelligence", "Big Data", "Cloud Computing", "Fintech", "Healthcare Tech", "E-Commerce", "SaaS Startups", "Cybersecurity", "Autonomous Systems"],
            default=["Artificial Intelligence", "Big Data"],
            key="ob_interests"
        )
        st.session_state["ob_data_interests"] = interests

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅ Back"):
                st.session_state["onboarding_step"] = 3
                st.rerun()
        with col_b2:
            if st.button("Continue ➔", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = 5
                st.rerun()

    # Step 5: Work & Location Preferences
    elif curr_step == 5:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 5: Work & Location Preferences</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>How and where do you want to work?</p>", unsafe_allow_html=True)
        pref = st.selectbox("Work Arrangement Preference:", WORK_PREFERENCES, key="ob_pref")
        target_city = st.text_input("Preferred Cities / Remote:", value="Remote / Flexible", key="ob_loc")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅ Back"):
                st.session_state["onboarding_step"] = 4
                st.rerun()
        with col_b2:
            if st.button("🚀 Complete Setup & Launch", type="primary", use_container_width=True):
                user_id = user_info["user_id"]
                save_onboarding_data(
                    user_id=user_id,
                    country=st.session_state.get("ob_data_country", "United States"),
                    education_level=st.session_state.get("ob_data_edu", EDUCATION_LEVELS[0]),
                    degree_field=st.session_state.get("ob_data_field", "Computer Science"),
                    experience_level=st.session_state.get("ob_data_exp", EXPERIENCE_LEVELS[0]),
                    interests=st.session_state.get("ob_data_interests", []),
                    work_preference=pref,
                    target_locations=target_city
                )
                
                # Save initial profile
                save_user_profile(
                    user_id=user_id,
                    target_role=st.session_state.get("target_role", "Data Analyst"),
                    target_company=st.session_state.get("target_company", "Any Company (General Industry Standard)"),
                    candidate_text=st.session_state.get("candidate_text", f"Skills: {', '.join(st.session_state.get('candidate_skills', ['SQL', 'Python', 'Excel']))}"),
                    candidate_skills=st.session_state.get("candidate_skills", ["SQL", "Python", "Excel"]),
                    github_user=st.session_state.get("github_user", "arivera"),
                    readiness_score=65.0
                )

                st.session_state["onboarding_completed"] = True
                st.session_state["active_view"] = "nav_dashboard"
                st.success("🎉 Workspace initialized! Welcome to AI Career Navigator.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
