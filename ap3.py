import streamlit as st
import re
from pdfminer.high_level import extract_text
import streamlit_antd_components as sac

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# -------------------------
# Dark Theme
# -------------------------
st.markdown("""
<style>

.stApp{
background-color:#0E1117;
color:white;
}

[data-testid="stSidebar"]{
background-color:#111827;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Skill Database
# -------------------------
skills_db = [
"python","java","machine learning","deep learning",
"data science","sql","power bi","tableau",
"excel","tensorflow","pandas","numpy",
"nlp","computer vision","html","css",
"javascript","git","statistics","scikit-learn"
]

# -------------------------
# Functions
# -------------------------
def extract_resume_text(file):
    text = extract_text(file)
    return text

def extract_skills(text):
    text = text.lower()
    skills = []
    
    for skill in skills_db:
        if skill in text:
            skills.append(skill)
            
    return list(set(skills))

def skill_match(resume_skills, jd_skills):

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(jd_skills)) * 100

    return matched, missing, score


# -------------------------
# Sidebar Menu
# -------------------------
menu = sac.menu([
    sac.MenuItem('Dashboard', icon='house'),
    sac.MenuItem('Resume Analysis', icon='file-earmark-text'),
    sac.MenuItem('About Project', icon='info-circle')
])

# -------------------------
# Dashboard
# -------------------------
if menu == "Dashboard":

    st.title("AI Resume Analyzer Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Skills in Database", len(skills_db))

    with col2:
        st.metric("Project Type", "AI / NLP")

    with col3:
        st.metric("Interface", "Streamlit Dashboard")

    st.write("Upload a resume and compare it with a job description to analyze skill match.")

# -------------------------
# Resume Analyzer
# -------------------------
if menu == "Resume Analysis":

    st.title("Resume vs Job Description Analysis")

    uploaded_file = st.file_uploader("Upload Resume (PDF)")

    job_description = st.text_area("Paste Job Description")

    if uploaded_file and job_description:

        resume_text = extract_resume_text(uploaded_file)

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(job_description)

        matched, missing, score = skill_match(resume_skills, jd_skills)

        st.subheader("Skill Match Score")

        st.progress(int(score))
        st.metric("Match Percentage", str(round(score,2))+" %")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Skills")
            st.success(matched)

        with col2:
            st.subheader("Missing Skills")
            st.error(missing)

        st.subheader("Job Fit Prediction")

        if score > 75:
            st.success("Strong Fit for the Job")

        elif score > 50:
            st.warning("Moderate Fit – Improve some skills")

        else:
            st.error("Low Fit – Needs improvement")

        st.subheader("Skill Improvement Suggestions")

        for skill in missing:
            st.write("Learn:", skill)

# -------------------------
# About Section
# -------------------------
if menu == "About Project":

    st.title("About This Project")

    st.write("""
    This AI Resume Analyzer compares candidate resumes with job descriptions
    and predicts job suitability based on skill matching.

    Technologies Used:
    - Python
    - Streamlit
    - NLP based skill extraction
    - PDF resume parsing
    """)