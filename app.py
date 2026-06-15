import streamlit as st
from groq import Groq
import json
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeAI – Smart Career Documents",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1a1a2e;
}
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0fff4 100%);
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    line-height: 1.1;
    color: #1a1a2e;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}
.hero-title span {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #6b7280;
    font-weight: 300;
    margin-bottom: 2rem;
}
.section-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #667eea;
    margin-bottom: 0.5rem;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #1a1a2e;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.5rem;
}
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 24px rgba(102,126,234,0.08);
}
.doc-output {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    line-height: 1.75;
    color: #1a1a2e;
    white-space: pre-wrap;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    max-height: 600px;
    overflow-y: auto;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.02em;
    transition: transform 0.15s, box-shadow 0.15s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(102,126,234,0.35);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.5);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.4rem 1.2rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
}
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.8);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(102,126,234,0.15);
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", st.session_state.get("api_key", ""))
    if not api_key:
        return None
    return Groq(api_key=api_key)


def stream_text(prompt: str, system: str = "") -> str:
    client = get_client()
    if client is None:
        st.error("⚠️  Enter your Groq API key in the sidebar first.")
        return ""

    full = ""
    placeholder = st.empty()

    try:
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system or "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
            max_tokens=2048,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full += delta
            placeholder.markdown(
                f'<div class="doc-output">{full}▌</div>',
                unsafe_allow_html=True
            )
        placeholder.markdown(
            f'<div class="doc-output">{full}</div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return ""

    return full


def collect_profile() -> dict:
    return st.session_state.get("profile", {})


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ✦ ResumeAI")
    st.markdown("---")

    


    st.markdown("### 👤 Your Profile")

    with st.expander("Basic Info", expanded=True):
        name = st.text_input("Full Name", placeholder="Aisha Rajan")
        email = st.text_input("Email", placeholder="aisha@example.com")
        phone = st.text_input("Phone", placeholder="+91 98765 43210")
        linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/aisha")
        github = st.text_input("GitHub / Portfolio", placeholder="github.com/aisha")
        location = st.text_input("Location", placeholder="Mumbai, India")

    with st.expander("Education"):
        degree = st.text_input("Degree & Major", placeholder="B.Tech Computer Science")
        university = st.text_input("University", placeholder="IIT Delhi")
        grad_year = st.text_input("Expected Graduation", placeholder="May 2026")
        gpa = st.text_input("GPA (optional)", placeholder="3.8 / 4.0")
        courses = st.text_area("Relevant Courses", placeholder="Data Structures, ML, DBMS…", height=80)

    with st.expander("Skills"):
        tech_skills = st.text_area("Technical Skills", placeholder="Python, React, SQL, TensorFlow…", height=80)
        soft_skills = st.text_area("Soft Skills", placeholder="Leadership, Communication…", height=60)
        languages = st.text_input("Languages", placeholder="English (Fluent), Hindi (Native)")

    with st.expander("Experience"):
        experience = st.text_area(
            "Internships / Work Experience",
            placeholder="Software Intern @ Flipkart (Jun–Aug 2024): Built REST APIs reducing latency by 30%…",
            height=140,
        )

    with st.expander("Projects"):
        projects = st.text_area(
            "Projects",
            placeholder="1. SmartMed AI – LLM-powered drug interaction checker (Python, FastAPI)\n2. EcoTrack – Carbon footprint tracker (React, Node, MongoDB)…",
            height=140,
        )

    with st.expander("Achievements & Extras"):
        achievements = st.text_area(
            "Awards / Certifications / Publications",
            placeholder="Winner – HackIndia 2024; AWS Certified Developer…",
            height=100,
        )
        extracurriculars = st.text_area(
            "Clubs / Volunteering",
            placeholder="Tech Lead – Coding Club; Mentor – Girls Who Code…",
            height=80,
        )

    if st.button("💾  Save Profile"):
        st.session_state["profile"] = {
            "name": name, "email": email, "phone": phone,
            "linkedin": linkedin, "github": github, "location": location,
            "degree": degree, "university": university, "grad_year": grad_year,
            "gpa": gpa, "courses": courses,
            "tech_skills": tech_skills, "soft_skills": soft_skills, "languages": languages,
            "experience": experience, "projects": projects,
            "achievements": achievements, "extracurriculars": extracurriculars,
        }
        st.success("Profile saved! ✓")


# ── Main area ─────────────────────────────────────────────────────────────────

st.markdown("""
<div class="card">
    <div class="hero-title">Your career documents,<br><span>AI-crafted.</span></div>
    <div class="hero-subtitle">
        Fill your profile in the sidebar → choose a tool below → generate in seconds.
    </div>
</div>
""", unsafe_allow_html=True)

profile = collect_profile()
filled = sum(1 for v in profile.values() if v and str(v).strip())
total = 18
pct = int(filled / total * 100) if total else 0

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Profile Completeness", f"{pct}%")
col_m2.metric("Fields Filled", f"{filled} / {total}")
col_m3.metric("Ready to Generate", "✓ Yes" if pct >= 40 else "✗ Add more info")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Resume",
    "✉️  Cover Letter",
    "🌐 Portfolio Page",
    "💡 Interview Prep",
    "🔍 Resume Analyzer",
])


# ── TAB 1 — Resume ────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-tag">Output Type</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI-Generated Resume</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        resume_style = st.selectbox(
            "Resume Style",
            ["Professional / Corporate", "Creative / Design", "Technical / Engineering", "Research / Academic"],
        )
        job_role = st.text_input("Target Job Role", placeholder="Backend Software Engineer")
        job_desc = st.text_area(
            "Paste Job Description (optional)",
            placeholder="We're looking for a Python developer…",
            height=120,
        )
    with col2:
        resume_format = st.radio("Format", ["Chronological", "Functional", "Hybrid"])
        include_summary = st.checkbox("Include Professional Summary", value=True)
        ats_optimise = st.checkbox("ATS-Optimise (keyword dense)", value=True)
        highlight_projects = st.checkbox("Emphasise Projects Section", value=True)

    if st.button("✨  Generate Resume"):
        if not profile:
            st.warning("Save your profile first (sidebar).")
        else:
            system = (
                "You are an elite resume writer with 15 years of experience placing "
                "students at top companies. Write clean, impactful, ATS-friendly resumes. "
                "Use strong action verbs. Quantify achievements wherever possible. "
                "Output plain text suitable for direct copy-paste or PDF export."
            )
            prompt = f"""
Create a {resume_format} resume in {resume_style} style for the following student.
Target role: {job_role or 'General Software Engineering / Technology'}
{'Job description context: ' + job_desc if job_desc else ''}
{'Include a tailored professional summary.' if include_summary else ''}
{'Optimise heavily for ATS – embed relevant keywords naturally.' if ats_optimise else ''}
{'Give extra prominence to the projects section.' if highlight_projects else ''}

STUDENT PROFILE:
{json.dumps(profile, indent=2)}

Format the resume with clear sections, proper spacing, and strong bullet points.
Each bullet must start with a power verb and include a metric where possible.
"""
            with st.spinner("Crafting your resume…"):
                result = stream_text(prompt, system)
            if result:
                st.session_state["last_resume"] = result
                st.download_button(
                    "⬇️  Download Resume (.txt)",
                    result,
                    file_name=f"resume_{(profile.get('name') or 'student').replace(' ','_')}.txt",
                    mime="text/plain",
                )


# ── TAB 2 — Cover Letter ──────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-tag">Output Type</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Personalised Cover Letter</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        company_name = st.text_input("Company Name", placeholder="Google")
        cl_role = st.text_input("Role Applying For", placeholder="Software Engineering Intern")
        hiring_manager = st.text_input("Hiring Manager Name (if known)", placeholder="Ms. Sarah Chen")
        cl_job_desc = st.text_area(
            "Job Description / Key Requirements",
            placeholder="Paste the JD here for a perfectly tailored letter…",
            height=140,
        )
    with col2:
        cl_tone = st.select_slider(
            "Tone",
            options=["Formal", "Professional", "Warm-Professional", "Enthusiastic", "Bold"],
            value="Warm-Professional",
        )
        cl_length = st.radio("Length", ["Concise (~250 words)", "Standard (~350 words)", "Detailed (~450 words)"])
        why_company = st.text_area(
            "Why this company? (your personal reason)",
            placeholder="I've admired Google's work on AI…",
            height=80,
        )

    if st.button("✉️  Generate Cover Letter"):
        if not profile:
            st.warning("Save your profile first.")
        else:
            system = (
                "You are a professional career coach who writes compelling, authentic cover letters "
                "that get interviews. Never use clichés like 'I am writing to express my interest'. "
                "Open with a strong hook. Make the letter feel personal and specific, not templated."
            )
            prompt = f"""
Write a {cl_tone.lower()} cover letter ({cl_length}) for:
Applicant: {profile.get('name', 'the applicant')}
Company: {company_name}
Role: {cl_role}
{'Addressed to: ' + hiring_manager if hiring_manager else ''}
{'Job description: ' + cl_job_desc if cl_job_desc else ''}
{'Personal motivation: ' + why_company if why_company else ''}

Applicant profile:
{json.dumps(profile, indent=2)}

Instructions:
- Open with a memorable hook (not generic opening)
- Highlight 2-3 most relevant achievements with specifics
- Show genuine enthusiasm for the company/role
- End with a confident, action-oriented closing
"""
            with st.spinner("Writing your cover letter…"):
                result = stream_text(prompt, system)
            if result:
                st.download_button(
                    "⬇️  Download Cover Letter (.txt)",
                    result,
                    file_name=f"cover_letter_{company_name.replace(' ','_')}.txt",
                    mime="text/plain",
                )


# ── TAB 3 — Portfolio Page ────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-tag">Output Type</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Portfolio Website (HTML)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        port_style = st.selectbox(
            "Visual Style",
            ["Minimal & Clean", "Bold & Creative", "Dark Hacker Theme", "Corporate Blue", "Pastel Modern"],
        )
        port_sections = st.multiselect(
            "Sections to Include",
            ["Hero / About", "Skills", "Projects", "Experience", "Education", "Achievements", "Contact"],
            default=["Hero / About", "Skills", "Projects", "Experience", "Contact"],
        )
    with col2:
        color_accent = st.color_picker("Accent Colour", "#667eea")
        include_animations = st.checkbox("Include CSS Animations", value=True)
        dark_mode = st.checkbox("Dark Mode Base", value=False)

    if st.button("🌐  Generate Portfolio HTML"):
        if not profile:
            st.warning("Save your profile first.")
        else:
            system = (
                "You are a senior frontend developer and UI designer. "
                "Generate complete, beautiful single-file HTML portfolio websites. "
                "Include embedded CSS and vanilla JS. Make them production-ready and mobile-responsive. "
                "Output ONLY valid HTML with no extra explanation."
            )
            prompt = f"""
Generate a complete single-file HTML portfolio website.

Style: {port_style}
Sections: {', '.join(port_sections)}
Accent colour: {color_accent}
{'Include smooth CSS animations and transitions.' if include_animations else 'Minimal animations.'}
{'Dark mode background (#0f0f0f base).' if dark_mode else 'Light mode background.'}

Student profile:
{json.dumps(profile, indent=2)}

Requirements:
- Fully self-contained single HTML file (CSS + JS embedded)
- Mobile-responsive with media queries
- Smooth scroll navigation
- Modern, impressive design
- Real content from the profile (not placeholders)
- Clean semantic HTML5
- Hover effects on project cards
"""
            with st.spinner("Building your portfolio…"):
                result = stream_text(prompt, system)
            if result:
                html_match = re.search(r"```html\s*([\s\S]*?)```", result)
                html_content = html_match.group(1) if html_match else result

                fname = f"portfolio_{(profile.get('name') or 'student').replace(' ','_')}.html"
                st.download_button(
                    "⬇️  Download Portfolio HTML",
                    html_content,
                    file_name=fname,
                    mime="text/html",
                )
                with st.expander("👁️  Preview HTML Source"):
                    st.code(html_content[:3000] + ("…" if len(html_content) > 3000 else ""), language="html")


# ── TAB 4 — Interview Prep ────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-tag">Output Type</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interview Preparation Kit</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        iv_role = st.text_input("Role / Company", placeholder="Data Scientist @ Amazon")
        iv_round = st.selectbox(
            "Interview Round",
            ["HR / Screening", "Technical Round 1", "Technical Round 2", "System Design", "Behavioural / HR Final", "All Rounds"],
        )
        iv_jd = st.text_area("Job Description (optional)", height=100)
    with col2:
        iv_type = st.multiselect(
            "Question Types",
            ["Behavioural (STAR)", "Technical / DSA", "Project Deep-Dive", "Situational", "Company-Specific"],
            default=["Behavioural (STAR)", "Technical / DSA", "Project Deep-Dive"],
        )
        num_questions = st.slider("Number of Questions", 5, 20, 10)
        include_answers = st.checkbox("Include Sample Answers", value=True)

    if st.button("💡  Generate Interview Kit"):
        if not profile:
            st.warning("Save your profile first.")
        else:
            system = (
                "You are a top-tier interview coach. "
                "Generate highly specific, tailored interview questions and model answers."
            )
            prompt = f"""
Create an interview preparation kit for:
Candidate: {profile.get('name', 'the student')}
Target: {iv_role}
Round: {iv_round}
Question types: {', '.join(iv_type)}
Number of questions: {num_questions}
{'Job description: ' + iv_jd if iv_jd else ''}
{'Include detailed sample answers using STAR method where applicable.' if include_answers else 'Questions only.'}

Candidate profile:
{json.dumps(profile, indent=2)}

Make questions specific to the candidate's actual projects and experience.
Include tips on what interviewers are really looking for after each question.
"""
            with st.spinner("Preparing your interview kit…"):
                result = stream_text(prompt, system)
            if result:
                st.download_button(
                    "⬇️  Download Interview Kit (.txt)",
                    result,
                    file_name=f"interview_prep_{iv_role.replace(' ','_')[:30]}.txt",
                    mime="text/plain",
                )


# ── TAB 5 — Resume Analyzer ───────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-tag">Output Type</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Resume Feedback & Score</div>', unsafe_allow_html=True)

    existing_resume = st.text_area(
        "Paste your existing resume text here",
        placeholder="Paste your current resume…",
        height=250,
    )
    analyze_jd = st.text_area(
        "Paste the Job Description to check fit (optional)",
        height=100,
    )

    if st.button("🔍  Analyze & Score"):
        if not existing_resume.strip():
            st.warning("Paste a resume to analyze.")
        else:
            system = (
                "You are an expert ATS system and senior HR professional. "
                "Provide detailed, actionable resume feedback. Be specific and honest. "
                "Score each section numerically and give concrete improvement suggestions."
            )
            prompt = f"""
Analyze this resume and provide detailed feedback:

RESUME:
{existing_resume}

{'JOB DESCRIPTION TO MATCH AGAINST:\n' + analyze_jd if analyze_jd else ''}

Provide:
1. OVERALL SCORE: X/100 with breakdown by section
2. ATS COMPATIBILITY: score and missing keywords
3. IMPACT SCORE: how well achievements are quantified
4. SECTION-BY-SECTION FEEDBACK
5. TOP 5 IMMEDIATE IMPROVEMENTS (specific, actionable)
6. WEAK BULLETS → REWRITTEN (show 3-5 examples)
7. MISSING ELEMENTS checklist
8. FINAL VERDICT: Ready to apply? What is the number 1 change to make today?
"""
            with st.spinner("Analyzing your resume…"):
                result = stream_text(prompt, system)
            if result:
                st.download_button(
                    "⬇️  Download Analysis (.txt)",
                    result,
                    file_name="resume_analysis.txt",
                    mime="text/plain",
                )


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#9ca3af; font-size:0.8rem; padding:1rem 0;">'
    'ResumeAI · Powered by Groq (LLaMA 3.3) · Built with Streamlit · '
    'Your data stays in this session only.'
    '</div>',
    unsafe_allow_html=True,
)
