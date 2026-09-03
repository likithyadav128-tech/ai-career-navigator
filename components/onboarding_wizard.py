"""
5-Step Progressive Onboarding Wizard Component
Collects user profile, background, technical proficiencies, career aspirations, and work preferences.
"""
import streamlit as st
from config import CAREER_TRACKS
from modules.resume_analyzer import SKILL_TAXONOMY
from database.profile_repo import save_onboarding_data, save_user_profile

COUNTRIES = [
    "India", "United States", "United Kingdom", "Canada", "Germany", "Australia",
    "Singapore", "United Arab Emirates", "France", "Netherlands", "Brazil", "Japan", "Global / Other"
]

BRANCHES = [
    "Computer Science & Engineering (CSE)",
    "Information Technology (IT)",
    "Artificial Intelligence and Data Science (AI & DS)",
    "Artificial Intelligence & Machine Learning (AI / ML)",
    "Data Science & Analytics",
    "Information Science Engineering (ISE)",
    "Electronics & Communication Engineering (ECE)",
    "Electrical & Electronics Engineering (EEE)",
    "Mechanical Engineering",
    "Civil Engineering",
    "Computer Applications (BCA / MCA)",
    "Business Administration & Management (BBA / MBA)",
    "Commerce & Accounting (B.Com / M.Com)",
    "Other Branch / Field"
]

EDUCATION_LEVELS = [
    "Undergraduate Student (Pursuing Bachelor's)",
    "Recent College Graduate (Bachelor's Completed)",
    "Master's / Postgraduate Student",
    "PhD Candidate / Graduate",
    "Bootcamp Graduate / Self-Taught",
    "Working Professional (Career Switcher)"
]

COURSES = [
    "B.Tech / B.E (Bachelor of Technology / Engineering)",
    "BCA (Bachelor of Computer Applications)",
    "B.Sc in Computer Science / IT / Data Science",
    "B.Sc in Mathematics / Statistics / Science",
    "M.Tech / M.E (Master of Technology / Engineering)",
    "MCA (Master of Computer Applications)",
    "M.Sc in Data Science / AI / Statistics / CS",
    "MBA / PGDM (Business & Analytics)",
    "BBA / BBM (Business Administration)",
    "B.Com / M.Com (Commerce & Finance)",
    "Diploma in Engineering / PolyTech",
    "Other Course / Degree"
]

EXPERIENCE_LEVELS = [
    "Student / Intern (0 years)",
    "Entry-Level Junior (0 - 2 years)",
    "Mid-Level Professional (2 - 5 years)",
    "Senior / Specialist (5+ years)"
]

INDUSTRIES = [
    "Artificial Intelligence & Generative AI",
    "Big Data & Cloud Infrastructure",
    "Fintech & Digital Banking",
    "Healthcare & Biotechnology",
    "E-Commerce & Retail Tech",
    "SaaS & Enterprise Cloud Software",
    "Cybersecurity & Defense Tech",
    "EdTech (Education Technology)",
    "Automotive & Autonomous Systems",
    "Gaming, AR/VR & Metaverse",
    "Media, Entertainment & Social Tech",
    "Agritech & Supply Chain Tech",
    "Green Tech, Clean Energy & Sustainability",
    "Consulting & IT Services",
    "Robotics & IoT Hardware"
]

WORK_PREFERENCES = [
    "Remote First (Anywhere)",
    "Hybrid (2-3 days office)",
    "On-Site (Full Office)",
    "Flexible / Open to all"
]

TECH_CITIES = [
    "Bengaluru (Bangalore)",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Mumbai",
    "Delhi NCR (Gurugram / Noida)",
    "Kolkata",
    "Ahmedabad",
    "Kochi / Trivandrum",
    "San Francisco / Silicon Valley",
    "New York / East Coast",
    "Seattle / Pacific NW",
    "London (UK)",
    "Singapore",
    "Dubai (UAE)",
    "Berlin / Munich (Germany)",
    "Toronto / Vancouver (Canada)",
    "Remote / Anywhere",
    "Other City (Custom)"
]

# Branch to recommended career adoption mapping
BRANCH_CAREER_MAP = {
    "Computer Science & Engineering (CSE)": ["Software Engineer (Full-Stack)", "AI / LLM Engineer", "Data Scientist", "DevOps & SRE Engineer", "Data Engineer", "Cybersecurity Analyst"],
    "Information Technology (IT)": ["Software Engineer (Full-Stack)", "Cloud Solutions Architect", "DevOps & SRE Engineer", "Data Analyst", "Cybersecurity Analyst"],
    "Artificial Intelligence and Data Science (AI & DS)": ["Data Scientist", "AI / LLM Engineer", "Machine Learning Engineer", "Data Analyst", "Data Engineer", "Software Engineer (Full-Stack)"],
    "Artificial Intelligence & Machine Learning (AI / ML)": ["AI / LLM Engineer", "Machine Learning Engineer", "Data Scientist", "Data Analyst", "Data Engineer"],
    "Data Science & Analytics": ["Data Scientist", "Data Analyst", "Business Intelligence Engineer", "Data Engineer", "Machine Learning Engineer"],
    "Information Science Engineering (ISE)": ["Software Engineer (Full-Stack)", "Data Analyst", "Cloud Solutions Architect", "DevOps & SRE Engineer"],
    "Electronics & Communication Engineering (ECE)": ["Cloud Solutions Architect", "Software Engineer (Full-Stack)", "Data Analyst", "DevOps & SRE Engineer", "Cybersecurity Analyst"],
    "Electrical & Electronics Engineering (EEE)": ["Data Analyst", "Cloud Solutions Architect", "Software Engineer (Full-Stack)", "DevOps & SRE Engineer"],
    "Mechanical Engineering": ["Data Analyst", "Product Manager (Tech)", "Software Engineer (Full-Stack)", "Business Intelligence Engineer"],
    "Civil Engineering": ["Data Analyst", "Product Manager (Tech)", "Business Intelligence Engineer", "Software Engineer (Full-Stack)"],
    "Computer Applications (BCA / MCA)": ["Software Engineer (Full-Stack)", "Data Analyst", "DevOps & SRE Engineer", "Business Intelligence Engineer", "UI/UX Designer"],
    "Business Administration & Management (BBA / MBA)": ["Product Manager (Tech)", "Data Analyst", "Business Intelligence Engineer"],
    "Commerce & Accounting (B.Com / M.Com)": ["Data Analyst", "Business Intelligence Engineer", "Product Manager (Tech)"],
    "Other Branch / Field": list(CAREER_TRACKS.keys())
}

def render_onboarding_wizard(user_info: dict):
    """Renders the upgraded 5-step interactive onboarding flow."""
    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = 1

    curr_step = st.session_state["onboarding_step"]

    # Header and Progress Indicator
    st.markdown(f"""
    <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(139,92,246,0.35); border-radius: 24px; padding: 34px 32px; max-width: 780px; margin: 24px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.6);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
            <div style="display:inline-flex; align-items:center; gap:10px;">
                <span style="font-size:1.4rem;">🎯</span>
                <span style="font-size:0.95rem; font-weight:800; color:#A78BFA; text-transform:uppercase; letter-spacing:1px;">AI Career Profile Setup</span>
            </div>
            <div style="font-size:0.85rem; font-weight:800; color:#34D399; background:rgba(16,185,129,0.15); padding:4px 14px; border-radius:12px; border:1px solid rgba(16,185,129,0.3);">
                Step {curr_step} of 5
            </div>
        </div>
        <div style="height:6px; background:rgba(255,255,255,0.08); border-radius:3px; margin-bottom: 24px; overflow:hidden;">
            <div style="height:100%; width: {curr_step * 20}%; background: linear-gradient(90deg, #6366F1, #A855F7, #EC4899); border-radius:3px; transition:width 0.4s ease;"></div>
        </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # STEP 1: Country & Branch / Field of Study Dropdown
    # =========================================================================
    if curr_step == 1:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 1: Location & Branch of Study</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Tell us where you are based and which academic branch you are pursuing.</p>", unsafe_allow_html=True)
        
        sel_country = st.selectbox(
            "Your Country / Region:",
            COUNTRIES,
            index=COUNTRIES.index(st.session_state.get("ob_data_country", "India")) if st.session_state.get("ob_data_country", "India") in COUNTRIES else 0,
            key="ob_country"
        )
        st.session_state["ob_data_country"] = sel_country

        sel_branch = st.selectbox(
            "Which Branch / Field are you studying?",
            BRANCHES,
            index=BRANCHES.index(st.session_state.get("ob_data_branch", BRANCHES[0])) if st.session_state.get("ob_data_branch") in BRANCHES else 0,
            key="ob_branch"
        )

        custom_branch = ""
        if sel_branch == "Other Branch / Field":
            custom_branch = st.text_input("Specify your Branch / Field of Study:", value=st.session_state.get("ob_data_custom_branch", ""), placeholder="e.g. Bioinformatics, Chemical Engineering, Aerospace", key="ob_custom_branch")
            st.session_state["ob_data_custom_branch"] = custom_branch

        st.session_state["ob_data_branch"] = custom_branch if (sel_branch == "Other Branch / Field" and custom_branch.strip()) else sel_branch

        col_b1, col_b2 = st.columns([1, 1])
        with col_b2:
            if st.button("Continue ➔", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = 2
                st.rerun()

    # =========================================================================
    # STEP 2: Education Level, Course (with Other), and Experience
    # =========================================================================
    elif curr_step == 2:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 2: Degree Course & Experience Level</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Select your degree program and current professional seniority.</p>", unsafe_allow_html=True)
        
        edu = st.selectbox(
            "Highest Education Level:",
            EDUCATION_LEVELS,
            index=EDUCATION_LEVELS.index(st.session_state.get("ob_data_edu", EDUCATION_LEVELS[0])) if st.session_state.get("ob_data_edu") in EDUCATION_LEVELS else 0,
            key="ob_edu"
        )
        
        course_choice = st.selectbox(
            "Degree Course / Program:",
            COURSES,
            index=COURSES.index(st.session_state.get("ob_data_course_choice", COURSES[0])) if st.session_state.get("ob_data_course_choice") in COURSES else 0,
            key="ob_course_choice"
        )
        st.session_state["ob_data_course_choice"] = course_choice

        custom_course = ""
        if course_choice == "Other Course / Degree":
            custom_course = st.text_input("Specify your Course / Degree:", value=st.session_state.get("ob_data_custom_course", ""), placeholder="e.g. Integrated M.Tech, Dual Degree, BS Data Science", key="ob_custom_course")
            st.session_state["ob_data_custom_course"] = custom_course

        final_degree_field = custom_course if (course_choice == "Other Course / Degree" and custom_course.strip()) else course_choice
        st.session_state["ob_data_field"] = final_degree_field

        exp = st.selectbox(
            "Current Experience Level:",
            EXPERIENCE_LEVELS,
            index=EXPERIENCE_LEVELS.index(st.session_state.get("ob_data_exp", EXPERIENCE_LEVELS[0])) if st.session_state.get("ob_data_exp") in EXPERIENCE_LEVELS else 0,
            key="ob_exp"
        )

        st.session_state["ob_data_edu"] = edu
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

    # =========================================================================
    # STEP 3: Target Role Selection & Dynamic Role-Specific Skills
    # =========================================================================
    elif curr_step == 3:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 3: Target Role & Role-Specific Skills</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Select your target role first so we can tailor the skill checklist directly to what recruiters expect.</p>", unsafe_allow_html=True)
        
        career_list = list(CAREER_TRACKS.keys())
        user_branch = st.session_state.get("ob_data_branch", "")
        recommended_roles = BRANCH_CAREER_MAP.get(user_branch, career_list)
        default_role = recommended_roles[0] if recommended_roles else "Data Analyst"
        
        curr_role = st.session_state.get("target_role", default_role)
        target_role = st.selectbox(
            "🎯 Select Your Target Role:",
            career_list,
            index=career_list.index(curr_role) if curr_role in career_list else 0,
            key="ob_target_role_step3"
        )
        st.session_state["target_role"] = target_role

        # Dynamically fetch role-specific core skills
        role_info = CAREER_TRACKS.get(target_role, CAREER_TRACKS["Data Analyst"])
        role_core_skills = role_info.get("core_skills", ["Python", "SQL", "Excel"])
        
        st.markdown(f"""
        <div style="background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); border-radius: 14px; padding: 14px 18px; margin: 16px 0 12px 0;">
            <div style="font-size:0.88rem; font-weight:700; color:#A5B4FC;">Required & Recommended Skills for <strong style="color:#FFF;">{target_role}</strong>:</div>
            <div style="font-size:0.82rem; color:#94A3B8; margin-top:2px;">Select the skills you already have familiarity with:</div>
        </div>
        """, unsafe_allow_html=True)

        existing_skills = st.session_state.get("candidate_skills", role_core_skills[:3])

        sel_role_skills = st.multiselect(
            f"Key Skills for {target_role}:",
            options=role_core_skills,
            default=[s for s in existing_skills if s in role_core_skills] or role_core_skills[:2],
            key=f"ob_skills_{target_role}"
        )

        with st.expander("➕ Add Other Programming Languages, Tools & Frameworks"):
            all_tax_skills = sorted(list(set(SKILL_TAXONOMY.values())))
            other_skills_options = [s for s in all_tax_skills if s not in role_core_skills]
            other_selected = st.multiselect(
                "Other Known Tools:",
                options=other_skills_options,
                default=[s for s in existing_skills if s in other_skills_options],
                key="ob_other_skills"
            )

        combined_skills = list(set(sel_role_skills + other_selected))
        st.session_state["candidate_skills"] = combined_skills

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅ Back"):
                st.session_state["onboarding_step"] = 2
                st.rerun()
        with col_b2:
            if st.button("Continue ➔", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = 4
                st.rerun()

    # =========================================================================
    # STEP 4: Career Adoption Based on Study & All Modern Industry Interests
    # =========================================================================
    elif curr_step == 4:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 4: Study-Aligned Career Adoption & Industry Focus</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Discover alternative and secondary career paths suited for your field of study, and select your industry interests.</p>", unsafe_allow_html=True)
        
        user_branch = st.session_state.get("ob_data_branch", "Computer Science & Engineering (CSE)")
        recommended_adopt_roles = BRANCH_CAREER_MAP.get(user_branch, list(CAREER_TRACKS.keys()))
        
        st.markdown(f"""
        <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); border-radius: 14px; padding: 14px 18px; margin-bottom: 16px;">
            <div style="font-size:0.88rem; font-weight:700; color:#34D399;">💡 Career Paths Aligned with <u>{user_branch}</u>:</div>
            <div style="font-size:0.82rem; color:#CBD5E1; margin-top:3px;">{', '.join(recommended_adopt_roles[:4])}</div>
        </div>
        """, unsafe_allow_html=True)

        adopt_role = st.selectbox(
            "Alternative / Secondary Role you want to explore based on your study:",
            options=recommended_adopt_roles,
            index=0,
            key="ob_adopt_role"
        )
        st.session_state["ob_data_secondary_role"] = adopt_role

        interests = st.multiselect(
            "Select Industry Sectors that Excite You (Select all that apply):",
            options=INDUSTRIES,
            default=st.session_state.get("ob_data_interests", ["Artificial Intelligence & Generative AI", "Big Data & Cloud Infrastructure"]),
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

    # =========================================================================
    # STEP 5: Work & Preferred Cities Dropdown List (Bengaluru, Hyderabad, etc.)
    # =========================================================================
    elif curr_step == 5:
        st.markdown("<h3 style='margin:0 0 6px 0; color:#FFF;'>Step 5: Work Style & Preferred Tech Cities</h3><p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Select your work style and preferred job locations from our tech hub dropdown.</p>", unsafe_allow_html=True)
        
        pref = st.selectbox(
            "Work Arrangement Preference:",
            WORK_PREFERENCES,
            index=WORK_PREFERENCES.index(st.session_state.get("ob_data_pref", WORK_PREFERENCES[0])) if st.session_state.get("ob_data_pref") in WORK_PREFERENCES else 0,
            key="ob_pref"
        )
        st.session_state["ob_data_pref"] = pref

        selected_cities = st.multiselect(
            "Preferred Job Cities / Locations:",
            options=TECH_CITIES,
            default=st.session_state.get("ob_data_cities", ["Bengaluru (Bangalore)", "Hyderabad"]),
            key="ob_cities_multiselect"
        )

        custom_city = ""
        if "Other City (Custom)" in selected_cities:
            custom_city = st.text_input("Specify Other City / Location:", placeholder="e.g. Chandigarh, Jaipur, Austin", key="ob_custom_city")
        
        final_cities_list = [c for c in selected_cities if c != "Other City (Custom)"]
        if custom_city.strip():
            final_cities_list.append(custom_city.strip())

        st.session_state["ob_data_cities"] = final_cities_list
        target_locations_str = ", ".join(final_cities_list) if final_cities_list else "Remote / Flexible"

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
                    country=st.session_state.get("ob_data_country", "India"),
                    education_level=st.session_state.get("ob_data_edu", EDUCATION_LEVELS[0]),
                    degree_field=f"{st.session_state.get('ob_data_field', 'B.Tech')} ({st.session_state.get('ob_data_branch', 'CSE')})",
                    experience_level=st.session_state.get("ob_data_exp", EXPERIENCE_LEVELS[0]),
                    interests=st.session_state.get("ob_data_interests", []),
                    work_preference=pref,
                    target_locations=target_locations_str
                )
                
                cand_skills = st.session_state.get("candidate_skills", ["SQL", "Python", "Excel"])
                cand_text = f"Candidate Profile\\nTarget Role: {st.session_state.get('target_role', 'Data Analyst')}\\nBranch: {st.session_state.get('ob_data_branch', 'CSE')}\\nDegree: {st.session_state.get('ob_data_field', 'B.Tech')}\\nTechnical Skills: {', '.join(cand_skills)}\\nLocation: {target_locations_str}"
                
                save_user_profile(
                    user_id=user_id,
                    target_role=st.session_state.get("target_role", "Data Analyst"),
                    target_company=st.session_state.get("target_company", "Any Company (General Industry Standard)"),
                    candidate_text=cand_text,
                    candidate_skills=cand_skills,
                    github_user=st.session_state.get("github_user", "arivera"),
                    readiness_score=68.0
                )

                st.session_state["onboarding_completed"] = True
                st.session_state["active_view"] = "nav_dashboard"
                st.success("🎉 Workspace initialized! Welcome to AI Career Navigator.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

