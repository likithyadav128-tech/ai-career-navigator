"""
GitHub Automated Profile Verifier Module
Fetches real public repository data, language breakdown, stars, and code activity via GitHub REST API.
"""

import requests

def verify_github_profile(username: str) -> dict:
    """
    Queries GitHub REST API to verify candidate developer profile:
    - User Bio & Public Repo Count
    - Language distribution dictionary & percentages
    - Verified tech detection (Docker, PyTorch, SQL, FastAPI, Jupyter)
    - Verified Developer Badge calculation
    """
    clean_user = username.strip().rstrip("/").split("/")[-1].replace("@", "")
    
    if not clean_user:
        return {"error": "Invalid GitHub username provided."}
        
    try:
        user_url = f"https://api.github.com/users/{clean_user}"
        repos_url = f"https://api.github.com/users/{clean_user}/repos?per_page=100&sort=updated"
        
        headers = {"User-Agent": "AI-Career-Copilot/1.0"}
        user_res = requests.get(user_url, headers=headers, timeout=5)
        
        if user_res.status_code != 200:
            return {
                "error": f"GitHub user '{clean_user}' not found (Status Code: {user_res.status_code}).",
                "verified": False
            }
            
        user_data = user_res.json()
        repos_res = requests.get(repos_url, headers=headers, timeout=5)
        repos_data = repos_res.json() if repos_res.status_code == 200 else []
        
        languages = {}
        verified_tech = set()
        total_stars = 0
        
        for r in repos_data:
            if isinstance(r, dict):
                lang = r.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
                    
                total_stars += r.get("stargazers_count", 0)
                
                # Tech keyword detection in repo names & descriptions
                repo_desc = (str(r.get("name")) + " " + str(r.get("description", ""))).lower()
                for tech in ["python", "pytorch", "tensorflow", "fastapi", "flask", "docker", "sql", "react", "streamlit", "mlops"]:
                    if tech in repo_desc:
                        verified_tech.add(tech.upper() if tech in ["sql", "mlops", "react"] else tech.capitalize())

        # Compute Developer Verification Score out of 100
        repo_count = user_data.get("public_repos", 0)
        score = min(100, repo_count * 5 + len(languages) * 8 + total_stars * 2 + len(verified_tech) * 6)
        
        if score >= 60:
            status_badge = "🏆 Verified Senior Developer"
            badge_color = "#16A34A"
        elif score >= 25:
            status_badge = "⚡ Verified Active Developer"
            badge_color = "#2563EB"
        else:
            status_badge = "🌱 Emerging Developer"
            badge_color = "#D97706"

        return {
            "verified": True,
            "username": clean_user,
            "name": user_data.get("name") or clean_user,
            "avatar_url": user_data.get("avatar_url"),
            "public_repos": repo_count,
            "followers": user_data.get("followers", 0),
            "total_stars": total_stars,
            "languages": languages,
            "verified_tech": sorted(list(verified_tech)),
            "developer_score": score,
            "status_badge": status_badge,
            "badge_color": badge_color,
            "profile_url": user_data.get("html_url")
        }
        
    except Exception as e:
        return {"error": f"Failed to connect to GitHub API: {str(e)}", "verified": False}
