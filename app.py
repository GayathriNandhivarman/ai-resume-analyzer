"""
app.py
Streamlit dashboard for the AI Resume Analyzer and Job Recommendation System.

Run with:
    streamlit run app.py
"""

import io
import streamlit as st
import plotly.express as px

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills, flatten_skills
from job_matcher import load_job_roles, match_roles, top_n_roles
from roadmap_generator import generate_roadmap

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer & Job Recommendation System")
st.caption(
    "Upload your resume to see how well it matches different job roles, "
    "which skills you're missing, and a suggested learning roadmap. "
    "This tool is for guidance only — not an automatic hiring decision."
)

# ---------------------------------------------------------
# Sidebar: file upload + target role selection
# ---------------------------------------------------------
st.sidebar.header("1. Upload your resume")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

MAX_FILE_SIZE_MB = 5

job_roles_df = load_job_roles("data/job_roles.csv")
skill_dict_df = load_skill_dictionary("data/skill_dictionary.csv")

st.sidebar.header("2. Select target role")
target_role = st.sidebar.selectbox("Which role are you aiming for?", job_roles_df["job_role"].tolist())

analyze_clicked = st.sidebar.button("Analyze Resume", type="primary")

# ---------------------------------------------------------
# Main analysis
# ---------------------------------------------------------
if analyze_clicked:
    if uploaded_file is None:
        st.warning("Please upload a PDF or DOCX resume first.")
        st.stop()

    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"File too large ({file_size_mb:.1f} MB). Max allowed is {MAX_FILE_SIZE_MB} MB.")
        st.stop()

    st.success(f"Uploaded: {uploaded_file.name}")

    try:
        file_buffer = io.BytesIO(uploaded_file.getvalue())
        raw_text = extract_resume_text(file_buffer, uploaded_file.name)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

    if not raw_text.strip():
        st.error("No readable text was found in this file. It may be a scanned/image-based resume.")
        st.stop()

    cleaned_text = clean_text(raw_text)

    skills_by_category = extract_skills(cleaned_text, skill_dict_df)
    all_found_skills = flatten_skills(skills_by_category)

    ranked_roles = match_roles(cleaned_text, job_roles_df)
    top_roles = top_n_roles(ranked_roles, 3)

    target_score = dict(ranked_roles).get(target_role, 0.0)
    target_required = set(
        s.strip().lower()
        for s in job_roles_df.loc[job_roles_df["job_role"] == target_role, "required_skills"].values[0].split(",")
    )
    found_for_target = target_required & all_found_skills
    missing_for_target = sorted(target_required - all_found_skills)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"🎯 Match Score for {target_role}")
        st.metric(label="Match Score", value=f"{target_score}%")

        st.subheader("✅ Skills Found (Extracted)")
        if skills_by_category:
            for category, skills in skills_by_category.items():
                st.markdown(f"**{category}:** {', '.join(skills)}")
        else:
            st.info("No known skills were detected. Consider expanding the skill dictionary.")

    with col2:
        st.subheader("📊 Match Score by Role")
        chart_df = {"Role": [r for r, _ in ranked_roles], "Score (%)": [s for _, s in ranked_roles]}
        fig = px.bar(chart_df, x="Score (%)", y="Role", orientation="h", range_x=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🏆 Top 3 Recommended Roles")
        for i, (role, score) in enumerate(top_roles, start=1):
            st.write(f"{i}. **{role}** — {score}%")

    st.divider()

    col3, col4 = st.columns([1, 1])
    with col3:
        st.subheader(f"🔍 Skill Gap for {target_role}")
        st.markdown(f"**Already have:** {', '.join(sorted(found_for_target)) or 'None found'}")
        st.markdown(f"**Missing:** {', '.join(missing_for_target) or 'None — great match!'}")

    with col4:
        st.subheader("🗺️ Suggested Learning Roadmap")
        if missing_for_target:
            for line in generate_roadmap(missing_for_target):
                st.write("- " + line)
        else:
            st.success("No missing skills for this role. You're a strong match!")

    st.divider()

    found_lines = [f"- {s}" for s in sorted(found_for_target)] or ["- None"]
    missing_lines = [f"- {s}" for s in missing_for_target] or ["- None"]
    top_role_lines = [f"{i}. {role} - {score}%" for i, (role, score) in enumerate(top_roles, start=1)]
    roadmap_lines = generate_roadmap(missing_for_target) or ["No missing skills for this role."]

    report_lines = (
        [
            f"Target Role: {target_role}",
            f"Match Score: {target_score}%",
            "",
            "Skills Found:",
        ]
        + found_lines
        + ["", "Missing Skills:"]
        + missing_lines
        + ["", "Recommended Roles:"]
        + top_role_lines
        + ["", "Suggested Roadmap:"]
        + roadmap_lines
    )
    report_text = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download Analysis Report (.txt)",
        data=report_text,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )

    st.caption(
        "Note: This match score is an automated estimate based on keyword overlap. "
        "It does not evaluate your actual ability, and missing keywords do not always "
        "mean missing skills. Use this as guidance, not a final judgment."
    )

else:
    st.info("👈 Upload a resume and click **Analyze Resume** to get started.")