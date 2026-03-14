import streamlit as st
import re
from pdfminer.high_level import extract_text

# --------------------------------
# Skill database
# --------------------------------
skills_db = [
    "python","java","c","c++","machine learning","deep learning",
    "data science","sql","power bi","tableau","excel",
    "tensorflow","pandas","numpy","nlp","computer vision",
    "html","css","javascript","flask","django","git",
    "statistics","data analysis","scikit-learn"
]

# --------------------------------
# Extract text from PDF
# --------------------------------
def extract_resume_text(file):
    text = extract_text(file)
    return text


# --------------------------------
# Extract Email
# --------------------------------
def extract_email(text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return email[0] if email else "Not Found"


# --------------------------------
# Extract Phone
# --------------------------------
def extract_phone(text):
    phone = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    return phone[0] if phone else "Not Found"


# --------------------------------
# Extract Skills
# --------------------------------
def extract_skills(text):

    text = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# --------------------------------
# Skill Matching
# --------------------------------
def skill_match(resume_skills, jd_skills):

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(jd_skills)) * 100

    return matched, missing, score


# --------------------------------
# Streamlit UI
# --------------------------------
st.title("AI Resume vs Job Description Analyzer")

st.write("Upload resume and compare with job description.")

# Resume upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("Paste Job Description")


# --------------------------------
# Process
# --------------------------------
if uploaded_file is not None and job_description:

    st.success("Resume Uploaded")

    resume_text = extract_resume_text(uploaded_file)

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched, missing, score = skill_match(resume_skills, jd_skills)

    st.subheader("Candidate Information")

    st.write("📧 Email:", email)
    st.write("📞 Phone:", phone)

    st.subheader("Resume Skills")

    st.write(resume_skills)

    st.subheader("Job Required Skills")

    st.write(jd_skills)

    st.subheader("Skill Match Result")

    st.write("Matched Skills:", matched)

    st.write("Missing Skills:", missing)

    st.write("Match Score:", round(score,2), "%")

    # Fit prediction
    st.subheader("Job Fit Prediction")

    if score > 75:
        st.success("Strong Fit for the Job")
    elif score > 50:
        st.warning("Moderate Fit - Improve some skills")
    else:
        st.error("Low Fit - Needs major skill improvement")

    # Suggestions
    st.subheader("Suggestions to Improve")

    if missing:
        st.write("To improve your chances, learn these skills:")
        for skill in missing:
            st.write("✔", skill)
    else:
        st.write("Great! Your resume matches the job description.")

else:
    st.info("Upload resume and paste job description to start analysis.")