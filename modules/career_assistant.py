"""
AI Career Assistant Chatbot Module
Provides conversational answers and career guidance based on active resume context, gap analysis, and target role.
"""

def generate_assistant_response(query: str, context: dict) -> str:
    """
    Generates intelligent responses for career questions using active candidate & job context.
    """
    query_lower = query.lower()
    
    cand_skills = context.get("candidate_skills", [])
    target_role = context.get("target_role", "Data Scientist")
    readiness_score = context.get("readiness_score", 65.0)
    missing_skills = [s["skill"] for s in context.get("missing_skills", [])]
    moderate_skills = [s["skill"] for s in context.get("moderate_skills", [])]
    strong_skills = [s["skill"] for s in context.get("strong_skills", [])]
    resume_score = context.get("resume_score", 82)

    # 1. Preset Question: "What should I learn next?"
    if "learn next" in query_lower or "what to learn" in query_lower or "next step" in query_lower:
        if missing_skills:
            top_missing = missing_skills[:3]
            return f"""🎯 **Recommended Next Learning Focus for {target_role}:**

Based on your skill gap analysis, prioritize learning these **high-impact missing skills** next:

1. **{top_missing[0]}** - Essential requirement for {target_role}. Start with foundational tutorials and small exercises.
{f"2. **{top_missing[1]}** - Highly valued by recruiters in this role." if len(top_missing) > 1 else ""}
{f"3. **{top_missing[2]}** - Upgrades your profile to production-ready standard." if len(top_missing) > 2 else ""}

💡 **Action Tip:** Focus on **Phase 1 & Phase 2** in your **Personalized Roadmap** tab to complete hands-on mini-projects for these tools!"""
        else:
            return f"🎉 You already have all the core required skills for **{target_role}**! Your top priority now is building **production MLOps projects** (Docker, FastAPI deployment) and practicing mock technical interviews."

    # 2. Preset Question: "Am I ready for a Data Analyst / Data Scientist role?"
    elif "ready for" in query_lower or "readiness" in query_lower or "job ready" in query_lower:
        readiness_label = "High" if readiness_score >= 80 else ("Moderate" if readiness_score >= 55 else "Low")
        
        status_emoji = "🚀" if readiness_score >= 80 else ("⚡" if readiness_score >= 55 else "🎯")
        
        return f"""{status_emoji} **Job Readiness Assessment for {target_role}:**

- **Overall Readiness Score:** `{readiness_score}%` ({readiness_label} Readiness)
- **Strong Skills Verified:** {len(strong_skills)} ({', '.join(strong_skills[:4]) if strong_skills else 'None'})
- **Skills to Upgrade:** {len(missing_skills)} missing, {len(moderate_skills)} moderate.

**Verdict:**
{"You are in a strong position to apply! Polish your portfolio and start submitting applications." if readiness_score >= 80 else ("You have a solid foundation! Bridging 2-3 key missing skills will boost your readiness score above 80% within 2-3 weeks." if readiness_score >= 55 else "Focus on closing critical skill gaps first before applying, to maximize response rates from top employers.")}"""

    # 3. Preset Question: "Which skills should I add to my resume?"
    elif "skills should i add" in query_lower or "add to my resume" in query_lower or "resume skills" in query_lower:
        to_add = missing_skills[:4] + moderate_skills[:2]
        return f"""📄 **Skills to Learn & Add to Your Resume for {target_role}:**

To optimize your resume ATS score and match target job descriptions, target adding:

{"".join([f"- **{s}** (Target High-Demand Skill)\n" for s in to_add])}
> 💡 **Important:** Avoid simply listing skills in bullet points! Integrate them into **Project descriptions** with measurable results (e.g., *"Built REST API using **FastAPI** containerized with **Docker**, handling 1,000 requests/min"*)."""

    # 4. Custom query general response logic
    else:
        return f"""🤖 **AI Career Assistant Guidance for {target_role}:**

Thank you for your question: *"{query}"*

- **Current Resume Score:** `{resume_score}/100`
- **Target Role Readiness:** `{readiness_score}%`
- **Key Skills You Master:** {', '.join(strong_skills[:3]) if strong_skills else 'Python, Data Analysis'}
- **Focus Gaps:** {', '.join(missing_skills[:3]) if missing_skills else 'Advanced MLOps & Production Tools'}

💡 **Recommendation:** Check out the **Personalized Roadmap** and **Project Recommender** tabs to build hands-on portfolio projects targeting your exact skill gaps!"""
