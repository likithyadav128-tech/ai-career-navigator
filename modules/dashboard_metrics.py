"""
Dashboard Metrics & Visualizations Module
Creates futuristic dark-themed Plotly charts for Job Readiness Gauge, Radar Chart, and Skill Distribution.
"""

import plotly.graph_objects as go

BG_DARK = 'rgba(0,0,0,0)'
TEXT_LIGHT = '#e2e8f0'
GRID_COLOR = 'rgba(255,255,255,0.08)'

def create_readiness_gauge(score: float):
    """Generates a futuristic dark-themed Plotly Gauge Chart for Job Readiness Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Job Readiness Score", 'font': {'size': 22, 'color': TEXT_LIGHT}},
        number={'suffix': "%", 'font': {'size': 48, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "rgba(255,255,255,0.3)", 'tickfont': {'color': TEXT_LIGHT, 'size': 13}},
            'bar': {'color': "#6C63FF", 'thickness': 0.35},
            'bgcolor': "rgba(255,255,255,0.04)",
            'borderwidth': 1,
            'bordercolor': "rgba(255,255,255,0.1)",
            'steps': [
                {'range': [0, 45], 'color': 'rgba(239,68,68,0.15)'},
                {'range': [45, 75], 'color': 'rgba(245,158,11,0.12)'},
                {'range': [75, 100], 'color': 'rgba(16,185,129,0.15)'}
            ],
            'threshold': {
                'line': {'color': "#10b981", 'width': 4},
                'thickness': 0.8,
                'value': 80
            }
        }
    ))
    fig.update_layout(
        margin=dict(l=30, r=30, t=60, b=30),
        height=300,
        paper_bgcolor=BG_DARK,
        plot_bgcolor=BG_DARK,
        font=dict(color=TEXT_LIGHT)
    )
    return fig

def create_skill_distribution_chart(strong_count: int, moderate_count: int, missing_count: int):
    """Generates a futuristic Donut Chart showing Strong vs Moderate vs Missing skills."""
    labels = ['Strong Skills', 'Moderate Skills', 'Missing Skills']
    values = [strong_count, moderate_count, missing_count]
    colors = ['#10b981', '#f59e0b', '#ef4444']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.55,
        marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.1)', width=2)),
        textinfo='label+percent',
        textfont=dict(size=13, color='#ffffff'),
        hoverinfo='label+value',
        showlegend=True
    )])
    fig.update_layout(
        title={'text': "Skill Gap Matrix Breakdown", 'font': {'size': 20, 'color': TEXT_LIGHT}},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=13, color=TEXT_LIGHT)
        ),
        margin=dict(l=30, r=30, t=60, b=50),
        height=320,
        paper_bgcolor=BG_DARK,
        plot_bgcolor=BG_DARK,
        font=dict(color=TEXT_LIGHT)
    )
    return fig

def create_competency_radar_chart(candidate_skills: list, required_skills: list):
    """Generates a futuristic Radar Chart evaluating candidate mastery across skill domains."""
    categories = ['Programming & DB', 'ML & AI Frameworks', 'Data Viz & BI', 'Cloud & DevOps', 'Soft Skills']
    
    cand_str = " ".join(candidate_skills).lower()
    req_str = " ".join(required_skills).lower()
    
    def score_cat(keywords, text):
        return sum(1 for k in keywords if k in text)

    prog_kws = ["python", "sql", "c++", "r", "javascript", "bash", "postgresql"]
    ml_kws = ["pytorch", "scikit-learn", "tensorflow", "xgboost", "pandas", "numpy", "bert", "deep learning"]
    viz_kws = ["plotly", "tableau", "power bi", "matplotlib", "seaborn"]
    cloud_kws = ["docker", "aws", "gcp", "git", "linux", "fastapi", "kubernetes", "mlops"]
    soft_kws = ["problem solving", "communication", "agile", "collaboration", "critical thinking"]

    cand_scores = [
        min(10, score_cat(prog_kws, cand_str) * 2.5),
        min(10, score_cat(ml_kws, cand_str) * 2.0),
        min(10, score_cat(viz_kws, cand_str) * 3.0),
        min(10, score_cat(cloud_kws, cand_str) * 2.5),
        min(10, score_cat(soft_kws, cand_str) * 3.5 + 4.0)
    ]
    
    req_scores = [
        min(10, max(5, score_cat(prog_kws, req_str) * 3.0)),
        min(10, max(5, score_cat(ml_kws, req_str) * 2.5)),
        min(10, max(4, score_cat(viz_kws, req_str) * 3.5)),
        min(10, max(5, score_cat(cloud_kws, req_str) * 3.0)),
        min(10, max(6, score_cat(soft_kws, req_str) * 3.5 + 5.0))
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=cand_scores,
        theta=categories,
        fill='toself',
        name='Candidate Profile',
        fillcolor='rgba(108, 99, 255, 0.2)',
        line=dict(color='#6C63FF', width=3)
    ))
    fig.add_trace(go.Scatterpolar(
        r=req_scores,
        theta=categories,
        fill='toself',
        name='Target Job Benchmark',
        fillcolor='rgba(6, 182, 212, 0.12)',
        line=dict(color='#06b6d4', width=3, dash='dash')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=11, color='rgba(255,255,255,0.5)'),
                linecolor='rgba(255,255,255,0.08)',
                gridcolor=GRID_COLOR
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color=TEXT_LIGHT),
                linecolor='rgba(255,255,255,0.08)',
                gridcolor=GRID_COLOR
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=13, color=TEXT_LIGHT)
        ),
        title={'text': "Competency Radar: Candidate vs Job Benchmark", 'font': {'size': 20, 'color': TEXT_LIGHT}},
        margin=dict(l=40, r=40, t=60, b=50),
        height=360,
        paper_bgcolor=BG_DARK,
        plot_bgcolor=BG_DARK,
        font=dict(color=TEXT_LIGHT)
    )
    return fig
