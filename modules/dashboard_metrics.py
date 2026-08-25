"""
Dashboard Metrics & Visualizations Module - Next-Level Dark Glassmorphism Edition
Creates high-contrast Plotly charts designed for dark glowing background themes.
"""

import plotly.graph_objects as go

def create_readiness_gauge(score: float):
    """Generates a glowing Plotly Gauge Chart for Job Readiness Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Job Readiness Score", 'font': {'size': 22, 'color': '#F8FAFC', 'family': 'Arial, sans-serif'}},
        number={'suffix': "%", 'font': {'size': 46, 'color': '#38BDF8', 'family': 'Arial, sans-serif'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#94A3B8", 'tickfont': {'color': '#F8FAFC', 'size': 14}},
            'bar': {'color': "#3B82F6", 'thickness': 0.35},
            'bgcolor': "rgba(30, 41, 59, 0.8)",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 45], 'color': 'rgba(239, 68, 68, 0.25)'},   # Neon Red Glow
                {'range': [45, 75], 'color': 'rgba(245, 158, 11, 0.25)'},  # Neon Amber Glow
                {'range': [75, 100], 'color': 'rgba(34, 197, 94, 0.25)'}   # Neon Green Glow
            ],
            'threshold': {
                'line': {'color': "#4ADE80", 'width': 4},
                'thickness': 0.8,
                'value': 80
            }
        }
    ))
    fig.update_layout(
        margin=dict(l=30, r=30, t=60, b=30),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Arial, sans-serif')
    )
    return fig

def create_skill_distribution_chart(strong_count: int, moderate_count: int, missing_count: int):
    """Generates a glowing Donut Chart showing Strong vs Moderate vs Missing skills."""
    labels = ['Strong Skills', 'Moderate Skills', 'Missing Skills']
    values = [strong_count, moderate_count, missing_count]
    colors = ['#22C55E', '#F59E0B', '#EF4444']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.55,
        marker=dict(colors=colors, line=dict(color='#0F172A', width=3)),
        textinfo='label+percent',
        textfont=dict(size=14, color='#FFFFFF', family='Arial, sans-serif'),
        hoverinfo='label+value',
        showlegend=True
    )])
    fig.update_layout(
        title={'text': "Skill Gap Matrix Breakdown", 'font': {'size': 22, 'color': '#F8FAFC', 'family': 'Arial, sans-serif'}},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color='#F8FAFC')
        ),
        margin=dict(l=30, r=30, t=60, b=50),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Arial, sans-serif')
    )
    return fig

def create_competency_radar_chart(candidate_skills: list, required_skills: list):
    """Generates a Radar Chart evaluating candidate mastery across skill domains with glowing cyber styling."""
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
        fillcolor='rgba(56, 189, 248, 0.3)',
        line=dict(color='#38BDF8', width=3)
    ))
    fig.add_trace(go.Scatterpolar(
        r=req_scores,
        theta=categories,
        fill='toself',
        name='Target Job Benchmark',
        fillcolor='rgba(245, 158, 11, 0.15)',
        line=dict(color='#F59E0B', width=3, dash='dash')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=12, color='#94A3B8'),
                linecolor='#334155',
                gridcolor='#334155'
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color='#F8FAFC', family='Arial, sans-serif'),
                linecolor='#334155',
                gridcolor='#334155'
            ),
            bgcolor='rgba(15, 23, 42, 0.5)'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color='#F8FAFC')
        ),
        title={'text': "Competency Radar: Candidate vs Job Benchmark", 'font': {'size': 20, 'color': '#F8FAFC', 'family': 'Arial, sans-serif'}},
        margin=dict(l=40, r=40, t=60, b=50),
        height=360,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Arial, sans-serif')
    )
    return fig
