"""
Dashboard Metrics & Visualizations Module
Creates high-contrast, crystal-clear Plotly charts for Job Readiness Gauge, Radar Chart, and Skill Distribution.
"""

import plotly.graph_objects as go

def create_readiness_gauge(score: float):
    """Generates a high-contrast Plotly Gauge Chart for Job Readiness Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Job Readiness Score", 'font': {'size': 22, 'color': '#0F172A', 'family': 'Arial, sans-serif'}},
        number={'suffix': "%", 'font': {'size': 44, 'color': '#0F172A', 'family': 'Arial, sans-serif'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#475569", 'tickfont': {'color': '#0F172A', 'size': 14}},
            'bar': {'color': "#2563EB", 'thickness': 0.35},
            'bgcolor': "#F1F5F9",
            'borderwidth': 2,
            'bordercolor': "#CBD5E1",
            'steps': [
                {'range': [0, 45], 'color': '#FEE2E2'},    # Soft Red
                {'range': [45, 75], 'color': '#FEF3C7'},   # Soft Yellow
                {'range': [75, 100], 'color': '#DCFCE7'}   # Soft Green
            ],
            'threshold': {
                'line': {'color': "#15803D", 'width': 4},
                'thickness': 0.8,
                'value': 80
            }
        }
    ))
    fig.update_layout(
        margin=dict(l=30, r=30, t=60, b=30),
        height=300,
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#0F172A', family='Arial, sans-serif')
    )
    return fig

def create_skill_distribution_chart(strong_count: int, moderate_count: int, missing_count: int):
    """Generates a clean Donut Chart showing Strong vs Moderate vs Missing skills."""
    labels = ['Strong Skills', 'Moderate Skills', 'Missing Skills']
    values = [strong_count, moderate_count, missing_count]
    colors = ['#16A34A', '#D97706', '#DC2626']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.55,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=3)),
        textinfo='label+percent',
        textfont=dict(size=14, color='#FFFFFF', family='Arial, sans-serif'),
        hoverinfo='label+value',
        showlegend=True
    )])
    fig.update_layout(
        title={'text': "Skill Gap Matrix Breakdown", 'font': {'size': 22, 'color': '#0F172A', 'family': 'Arial, sans-serif'}},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color='#0F172A')
        ),
        margin=dict(l=30, r=30, t=60, b=50),
        height=320,
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#0F172A', family='Arial, sans-serif')
    )
    return fig

def create_competency_radar_chart(candidate_skills: list, required_skills: list):
    """Generates a Radar Chart evaluating candidate mastery across skill domains with crisp contrast."""
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
        fillcolor='rgba(37, 99, 235, 0.25)',
        line=dict(color='#2563EB', width=3)
    ))
    fig.add_trace(go.Scatterpolar(
        r=req_scores,
        theta=categories,
        fill='toself',
        name='Target Job Benchmark',
        fillcolor='rgba(217, 119, 6, 0.15)',
        line=dict(color='#D97706', width=3, dash='dash')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=12, color='#0F172A'),
                linecolor='#CBD5E1',
                gridcolor='#E2E8F0'
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color='#0F172A', family='Arial, sans-serif'),
                linecolor='#CBD5E1',
                gridcolor='#E2E8F0'
            ),
            bgcolor='#F8FAFC'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color='#0F172A')
        ),
        title={'text': "Competency Radar: Candidate vs Job Benchmark", 'font': {'size': 20, 'color': '#0F172A', 'family': 'Arial, sans-serif'}},
        margin=dict(l=40, r=40, t=60, b=50),
        height=360,
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#0F172A', family='Arial, sans-serif')
    )
    return fig
