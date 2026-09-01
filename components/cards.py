"""
Reusable Card Components
Provides standard UI cards for metrics, Next Best Action items, score boosters, and status tags.
"""
import streamlit as st

def render_metric_card(label: str, value: str, subtext: str = "", color: str = "#6366F1", icon: str = ""):
    """Renders a modern metric card with accessible styling."""
    icon_html = f"<span style='font-size:1.4rem; margin-right:8px;'>{icon}</span>" if icon else ""
    st.markdown(f"""
    <div style="background: var(--card-bg, rgba(255,255,255,0.03));
                border: 1px solid var(--card-border, rgba(99,102,241,0.18));
                border-radius: 16px; padding: 20px 18px; text-align: center;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15); margin-bottom: 14px;">
        <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted, #94A3B8); text-transform: uppercase; letter-spacing: 1px; display:flex; align-items:center; justify-content:center;">
            {icon_html}{label}
        </div>
        <div style="font-size: 2.2rem; font-weight: 800; color: {color}; margin: 8px 0 4px 0; line-height: 1.1;">
            {value}
        </div>
        <div style="font-size: 0.82rem; color: var(--text-sub, #64748B);">
            {subtext}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_next_best_action_card(action_title: str, category: str, time_estimate: str, description: str, on_continue_key: str = "btn_next_action"):
    """Renders the high-priority Next Best Action card on the dashboard."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.08) 50%, rgba(15,23,42,0.4) 100%);
                border: 1px solid rgba(139,92,246,0.4); border-left: 6px solid #818CF8;
                border-radius: 18px; padding: 24px 26px; margin-bottom: 24px;
                box-shadow: 0 10px 30px rgba(99,102,241,0.12);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom: 8px;">
            <div style="display:inline-flex; align-items:center; gap:8px;">
                <span style="font-size:1.3rem;">⚡</span>
                <span style="font-size: 0.8rem; font-weight: 800; color: #A78BFA; text-transform: uppercase; letter-spacing: 1.5px;">YOUR NEXT BEST ACTION</span>
            </div>
            <div style="display:inline-flex; gap:8px;">
                <span style="background: rgba(99,102,241,0.2); color: #C7D2FE; font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 12px; border: 1px solid rgba(99,102,241,0.3);">
                    ⏱️ {time_estimate}
                </span>
                <span style="background: rgba(16,185,129,0.15); color: #34D399; font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 12px; border: 1px solid rgba(16,185,129,0.3);">
                    🏷️ {category}
                </span>
            </div>
        </div>
        <h3 style="margin: 0 0 8px 0; color: #FFFFFF !important; font-size: 1.35rem; font-weight: 800;">{action_title}</h3>
        <p style="margin: 0 0 14px 0; color: #CBD5E1 !important; font-size: 0.94rem; line-height: 1.5;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_section_header(title: str, subtitle: str = "", icon: str = ""):
    """Renders a clean, uniform section header across tabs."""
    icon_html = f"<span style='margin-right:10px;'>{icon}</span>" if icon else ""
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; color: var(--text-main, #FFFFFF) !important; font-size: 1.7rem; font-weight: 800; display:flex; align-items:center;">
            {icon_html}{title}
        </h2>
        <p style="margin: 6px 0 0 0; color: var(--text-muted, #94A3B8) !important; font-size: 0.95rem;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)
