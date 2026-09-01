"""
Toast & Notification Panel Component
Renders user milestone notifications, achievement banners, and toast alerts.
"""
import streamlit as st
from database.notification_repo import get_user_notifications, mark_notification_read

def render_notifications_panel(user_id: int):
    """Renders user milestone alerts and notifications."""
    if not user_id:
        return

    notifs = get_user_notifications(user_id)
    if not notifs:
        st.info("🔔 No new notifications. Keep completing roadmap tasks and projects to unlock achievements!")
        return

    for n in notifs:
        icon = "🏆" if n["notif_type"] == "achievement" else ("⚡" if n["notif_type"] == "milestone" else "ℹ️")
        read_badge = "" if n["is_read"] else "<span style='background:#EF4444; color:#FFF; font-size:0.65rem; padding:2px 6px; border-radius:8px; font-weight:800; margin-left:8px;'>NEW</span>"
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(99,102,241,0.2); border-left: 4px solid #818CF8;
                    border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:0.95rem; color:#FFF;">{icon} {n['title']} {read_badge}</h4>
                <span style="font-size:0.75rem; color:#64748B;">{n['created_at'][:10]}</span>
            </div>
            <p style="margin:6px 0 0 0; font-size:0.86rem; color:#94A3B8;">{n['message']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not n["is_read"]:
            if st.button("Mark as Read", key=f"btn_read_notif_{n['id']}"):
                mark_notification_read(n["id"], user_id)
                st.rerun()
