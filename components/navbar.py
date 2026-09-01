"""
Top Navigation Bar Component
Provides header branding, Dark/Light theme toggle, active target role badge, and user menu.
"""
import streamlit as st
from config import APP_NAME

def render_top_navbar(user_info: dict, target_role: str, readiness_score: float, active_theme: str = "dark"):
    """Renders the top navbar with theme switcher and active status."""
    col_brand, col_status, col_theme = st.columns([1.5, 1.2, 0.7])
    
    with col_brand:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:38px; height:38px; border-radius:10px; background: linear-gradient(135deg, #6366F1, #A855F7); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 16px rgba(168,85,247,0.4);">
                <span style="color:#FFF; font-weight:900; font-size:1.15rem;">A✦</span>
            </div>
            <div>
                <div style="font-size:1.15rem; font-weight:900; color:var(--text-main, #FFF); letter-spacing:-0.5px;">{APP_NAME}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#818CF8;">AI Career OS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_status:
        st.markdown(f"""
        <div style="background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25); border-radius: 20px; padding: 6px 14px; display:inline-flex; align-items:center; gap:10px;">
            <span style="font-size:0.82rem; color:var(--text-muted, #94A3B8);">Target: <strong style="color:#A5B4FC;">{target_role}</strong></span>
            <span style="height:12px; width:1px; background:rgba(255,255,255,0.15);"></span>
            <span style="font-size:0.82rem; font-weight:800; color:#34D399;">{readiness_score}% Ready</span>
        </div>
        """, unsafe_allow_html=True)

    with col_theme:
        theme_icon = "☀️ Light" if st.session_state.get("app_theme", "dark") == "dark" else "🌙 Dark"
        if st.button(theme_icon, key="btn_toggle_global_theme", help="Toggle Light / Dark mode"):
            new_theme = "light" if st.session_state.get("app_theme", "dark") == "dark" else "dark"
            st.session_state["app_theme"] = new_theme
            st.rerun()

    st.markdown("<div style='height: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 16px;'></div>", unsafe_allow_html=True)
