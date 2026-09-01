"""
Charts Component
Provides theme-adaptive Plotly charts for Job Readiness gauges, Competency Radars, and Career comparisons.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def _get_theme_colors(theme: str = "dark") -> dict:
    """Returns accessible theme colors for charts."""
    if theme == "light":
        return {
            "bg": "rgba(255,255,255,0.0)",
            "text": "#1E293B",
            "grid": "rgba(0,0,0,0.08)",
            "primary": "#4F46E5",
            "secondary": "#9333EA",
            "success": "#059669",
            "warning": "#D97706",
            "card_bg": "#FFFFFF"
        }
    else:
        return {
            "bg": "rgba(0,0,0,0.0)",
            "text": "#E2E8F0",
            "grid": "rgba(255,255,255,0.08)",
            "primary": "#818CF8",
            "secondary": "#C084FC",
            "success": "#34D399",
            "warning": "#FBBF24",
            "card_bg": "#0F172A"
        }

def render_theme_gauge(score: float, title: str = "Overall Job Readiness", theme: str = "dark"):
    """Renders an accessible gauge indicator."""
    c = _get_theme_colors(theme)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': c["text"], 'family': 'Inter'}},
        number={'suffix': "%", 'font': {'size': 38, 'color': c["text"], 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': c["grid"], 'tickfont': {'color': c["text"]}},
            'bar': {'color': "#6366F1", 'thickness': 0.28},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 1,
            'bordercolor': c["grid"],
            'steps': [
                {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.25)"},
                {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.25)"},
                {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.25)"}
            ],
            'threshold': {
                'line': {'color': "#34D399", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor=c["bg"],
        plot_bgcolor=c["bg"],
        height=260,
        margin=dict(l=25, r=25, t=45, b=20)
    )
    return fig

def render_theme_radar(factors: dict, theme: str = "dark"):
    """Renders 7-factor competency radar chart."""
    c = _get_theme_colors(theme)
    categories = list(factors.keys())
    values = list(factors.values())
    
    # Close polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.3)',
        line=dict(color='#818CF8', width=2.5),
        name='Current Mastery'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=c["text"], size=9),
                gridcolor=c["grid"]
            ),
            angularaxis=dict(
                tickfont=dict(color=c["text"], size=11, family='Inter'),
                gridcolor=c["grid"]
            ),
            bgcolor=c["bg"]
        ),
        paper_bgcolor=c["bg"],
        showlegend=False,
        height=320,
        margin=dict(l=40, r=40, t=30, b=30)
    )
    return fig

def render_career_bar_chart(matched_careers: list, theme: str = "dark"):
    """Renders horizontal comparison bar chart across career tracks."""
    c = _get_theme_colors(theme)
    df = pd.DataFrame(matched_careers[:8])
    
    fig = px.bar(
        df,
        x="match_score",
        y="role",
        orientation="h",
        color="match_score",
        color_continuous_scale=[[0, '#EF4444'], [0.5, '#F59E0B'], [1, '#10B981']],
        text="match_score"
    )
    fig.update_layout(
        paper_bgcolor=c["bg"],
        plot_bgcolor=c["bg"],
        font=dict(color=c["text"], family='Inter'),
        xaxis=dict(gridcolor=c["grid"], title="Match Score %", range=[0, 105]),
        yaxis=dict(gridcolor=c["grid"], title="", categoryorder='total ascending'),
        coloraxis_showscale=False,
        height=340,
        margin=dict(l=10, r=20, t=20, b=20)
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    return fig
