"""
Sidebar Navigation Component
Provides clean SaaS navigation across all application views and persistent profile targeting.
"""
import streamlit as st
from config import CAREER_TRACKS
from modules.company_role_profiles import COMPANY_PROFILES
from modules.resume_analyzer import SKILL_TAXONOMY, extract_skills_from_text, extract_text_from_pdf
from modules.sample_data import SAMPLE_RESUMES

NAVIGATION_ITEMS = [
    {"id": "nav_dashboard", "name": "Dashboard", "icon": "🏠"},
    {"id": "nav_explorer", "name": "Career Explorer", "icon": "🧭"},
    {"id": "nav_comparison", "name": "Career Comparison", "icon": "⚖️"},
    {"id": "nav_skill_gap", "name": "Skill Gap & Tree", "icon": "📊"},
    {"id": "nav_roadmap", "name": "AI Career Roadmap", "icon": "🗺️"},
    {"id": "nav_learning", "name": "Learning Hub", "icon": "📚"},
    {"id": "nav_projects", "name": "Project Builder & Auditor", "icon": "💡"},
    {"id": "nav_resume", "name": "Resume AI Studio", "icon": "📄"},
    {"id": "nav_interview", "name": "Interview Lab", "icon": "🎤"},
    {"id": "nav_tracker", "name": "Job Application Tracker", "icon": "💼"},
    {"id": "nav_portfolio", "name": "Public Portfolio", "icon": "🌐"},
    {"id": "nav_copilot", "name": "AI Career Copilot", "icon": "🤖"},
    {"id": "nav_settings", "name": "Account Settings", "icon": "⚙️"}
]

def render_app_sidebar(user_info: dict) -> str:
    """Renders the persistent sidebar and returns the active navigation view ID."""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0 16px 0;">
            <div style="font-size: 2.3rem;">🎯</div>
            <h3 style="margin: 0; color: #FFFFFF !important; font-size: 1.2rem; font-weight: 800;">AI Career OS</h3>
            <p style="color: #818CF8 !important; font-size: 0.88rem; font-weight: 700; margin: 4px 0 0 0;">👤 {user_info.get('full_name', 'Student')}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", key="sidebar_btn_logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user_info"] = None
            st.session_state["active_view"] = "landing"
            st.rerun()

        st.divider()

        # View Selector
        st.markdown("<div style='font-size:0.75rem; font-weight:800; color:#94A3B8; letter-spacing:1px; margin-bottom:8px;'>MAIN NAVIGATION</div>", unsafe_allow_html=True)
        nav_options = [f"{item['icon']} {item['name']}" for item in NAVIGATION_ITEMS]
        nav_id_map = {f"{item['icon']} {item['name']}": item['id'] for item in NAVIGATION_ITEMS}

        curr_view_id = st.session_state.get("active_view", "nav_dashboard")
        default_index = 0
        for idx, item in enumerate(NAVIGATION_ITEMS):
            if item["id"] == curr_view_id:
                default_index = idx
                break

        selected_nav_label = st.radio("Navigate", nav_options, index=default_index, label_visibility="collapsed")
        selected_view_id = nav_id_map[selected_nav_label]
        st.session_state["active_view"] = selected_view_id

        st.divider()

        # Target Role & Company Selector
        st.markdown("<div style='font-size:0.75rem; font-weight:800; color:#94A3B8; letter-spacing:1px; margin-bottom:8px;'>CAREER TARGET</div>", unsafe_allow_html=True)
        career_keys = list(CAREER_TRACKS.keys())
        current_role = st.session_state.get("target_role", "Data Analyst")
        role_index = career_keys.index(current_role) if current_role in career_keys else 0
        sel_role = st.selectbox("Target Role:", career_keys, index=role_index, key="sidebar_sel_role")
        st.session_state["target_role"] = sel_role

        company_keys = list(COMPANY_PROFILES.keys())
        current_comp = st.session_state.get("target_company", "Any Company (General Industry Standard)")
        comp_index = company_keys.index(current_comp) if current_comp in company_keys else 0
        sel_company = st.selectbox("Target Company:", company_keys, index=comp_index, key="sidebar_sel_comp")
        st.session_state["target_company"] = sel_company

        st.divider()

        # Resume & Skills Source
        st.markdown("<div style='font-size:0.75rem; font-weight:800; color:#94A3B8; letter-spacing:1px; margin-bottom:8px;'>RESUME & SKILLS SOURCE</div>", unsafe_allow_html=True)
        sample_choice = st.selectbox(
            "Profile Source:",
            ["Custom Upload / Input", "Data Science Student (Alex Rivera)", "Software & Web Developer (Sam Chen)"],
            key="sidebar_profile_source"
        )

        if "last_sample_choice" not in st.session_state:
            st.session_state["last_sample_choice"] = sample_choice

        if sample_choice != st.session_state["last_sample_choice"]:
            st.session_state["last_sample_choice"] = sample_choice
            if sample_choice != "Custom Upload / Input":
                st.session_state["candidate_text"] = SAMPLE_RESUMES[sample_choice]["text"]
                st.session_state["candidate_skills"] = list(SAMPLE_RESUMES[sample_choice]["extracted_skills"])
                if "mastered_skills_ms" in st.session_state:
                    del st.session_state["mastered_skills_ms"]
                st.rerun()

        if sample_choice == "Custom Upload / Input":
            up_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"], key="sidebar_pdf_uploader")
            if up_pdf is not None:
                if st.session_state.get("last_uploaded_filename") != up_pdf.name:
                    st.session_state["last_uploaded_filename"] = up_pdf.name
                    extracted_text = extract_text_from_pdf(up_pdf)
                    st.session_state["candidate_text"] = extracted_text
                    st.session_state["candidate_skills"] = extract_skills_from_text(extracted_text)
                    if "mastered_skills_ms" in st.session_state:
                        del st.session_state["mastered_skills_ms"]
                    st.rerun()
            else:
                if st.session_state.get("last_uploaded_filename") is not None:
                    st.session_state["last_uploaded_filename"] = None

                pasted_text = st.text_area("Or Paste Resume / Skills Text:", value=st.session_state.get("candidate_text", ""), height=110, key="sidebar_paste_text")
                if pasted_text != st.session_state.get("candidate_text", ""):
                    st.session_state["candidate_text"] = pasted_text
                    st.session_state["candidate_skills"] = extract_skills_from_text(pasted_text)
                    if "mastered_skills_ms" in st.session_state:
                        del st.session_state["mastered_skills_ms"]
                    st.rerun()

        # Direct Mastered Skill Tag Editor
        all_skills = sorted(list(set(SKILL_TAXONOMY.values())))
        curr_in_tax = [s for s in st.session_state.get("candidate_skills", []) if s in all_skills]
        sel_skills = st.multiselect(
            "Manage Mastered Skills:",
            options=all_skills,
            default=curr_in_tax,
            key="mastered_skills_ms",
            help="Add or remove skills to immediately recalculate readiness."
        )
        custom_extras = [s for s in st.session_state.get("candidate_skills", []) if s not in all_skills]
        st.session_state["candidate_skills"] = sorted(list(set(sel_skills + custom_extras)))

        st.divider()

        # GitHub Profile
        st.markdown("<div style='font-size:0.75rem; font-weight:800; color:#94A3B8; letter-spacing:1px; margin-bottom:8px;'>GITHUB EVIDENCE</div>", unsafe_allow_html=True)
        gh = st.text_input("GitHub Username:", value=st.session_state.get("github_user", "arivera"), key="sidebar_gh_input")
        if gh:
            st.session_state["github_user"] = gh

    return selected_view_id
