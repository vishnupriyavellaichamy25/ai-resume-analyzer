import streamlit as st
import re
from pdfminer.high_level import extract_text

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# -------------------------------
# Skill Database
# -------------------------------
skills_db = [
    "python","java","c","c++","machine learning","deep learning",
    "data science","sql","power bi","tableau","excel",
    "tensorflow","pandas","numpy","nlp","computer vision",
    "html","css","javascript","flask","django","git",
    "statistics","data analysis","scikit-learn"
]

# -------------------------------
# Functions
# -------------------------------
def extract_resume_text(file):
    text = extract_text(file)
    return text


def extract_email(text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return email[0] if email else "Not Found"


def extract_phone(text):
    phone = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    return phone[0] if phone else "Not Found"


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return list(set(found))


def skill_match(resume_skills, jd_skills):

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(jd_skills)) * 100

    return matched, missing, score


# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("AI Resume Analyzer")

st.sidebar.write("Upload resume and compare with job description")

uploaded_file = st.sidebar.file_uploader("Upload Resume", type=["pdf"])

job_description = st.sidebar.text_area("Paste Job Description")


# -------------------------------
# Main UI
# -------------------------------
st.title("📄 AI Resume vs Job Description Analyzer")

st.write("Analyze how well a resume fits a job description using skill matching.")

if uploaded_file and job_description:

    resume_text = extract_resume_text(uploaded_file)

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched, missing, score = skill_match(resume_skills, jd_skills)

    # ---------------------------
    # Candidate Info
    # ---------------------------
    st.subheader("Candidate Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Email", email)

    with col2:
        st.metric("Phone", phone)

    # ---------------------------
    # Skills Section
    # ---------------------------
    st.subheader("Skills Comparison")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Resume Skills")
        st.write(resume_skills)

    with col4:
        st.markdown("### Job Required Skills")
        st.write(jd_skills)

    # ---------------------------
    # Match Score
    # ---------------------------
    st.subheader("Match Score")

    st.progress(int(score))

    st.metric("Skill Match Percentage", str(round(score,2)) + "%")

    # ---------------------------
    # Matched Skills
    # ---------------------------
    st.subheader("Matched Skills")

    st.success(matched)

    # ---------------------------
    # Missing Skills
    # ---------------------------
    st.subheader("Missing Skills")

    if missing:
        st.error(missing)
    else:
        st.success("No missing skills")

    # ---------------------------
    # Prediction
    # ---------------------------
    st.subheader("Job Fit Prediction")

    if score > 75:
        st.success("Strong Fit for the Job")

    elif score > 50:
        st.warning("Moderate Fit – Improve some skills")

    else:
        st.error("Low Fit – Needs improvement")

    # ---------------------------
    # Suggestions
    # ---------------------------
    st.subheader("Suggestions to Improve")

    if missing:
        for skill in missing:
            st.write("✔ Learn:", skill)

    else:
        st.write("Your resume already matches the job requirements.")

else:
    st.info("Upload resume and paste job description in the sidebar to begin.")