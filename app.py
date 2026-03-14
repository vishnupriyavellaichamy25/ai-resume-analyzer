import streamlit as st
import re
import spacy
from pdfminer.high_level import extract_text
import matplotlib.pyplot as plt

# Load NLP model

nlp = spacy.load("en_core_web_sm")

# -------- Extract Resume Text --------

def extract_resume_text(file):
text = extract_text(file)
return text

# -------- Extract Email --------

def extract_email(text):
email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,4}", text)
if email:
return email[0]
return "Not Found"

# -------- Extract Phone --------

def extract_phone(text):
phone = re.findall(r"+?\d[\d -]{8,12}\d", text)
if phone:
return phone[0]
return "Not Found"

# -------- Skills Database --------

skills_list = [
"python","machine learning","data science","deep learning",
"nlp","sql","pandas","numpy","tensorflow","tableau",
"power bi","excel","data analysis","statistics",
"matplotlib","seaborn","scikit-learn","flask",
"streamlit","git","github"
]

# -------- Extract Skills --------

def extract_skills(text):

```
text = text.lower()

found_skills = []

for skill in skills_list:
    if skill in text:
        found_skills.append(skill)

return found_skills
```

# -------- Resume Score --------

def calculate_resume_score(skills):

```
important_skills = [
    "python","machine learning","sql",
    "pandas","numpy","deep learning"
]

score = 0

for skill in important_skills:
    if skill in skills:
        score += 15

if score > 100:
    score = 100

return score
```

# -------- ATS Score --------

def ats_score(skills):

```
ats_keywords = [
    "python","machine learning","sql",
    "data analysis","pandas","numpy"
]

score = 0

for keyword in ats_keywords:
    if keyword in skills:
        score += 15

if score > 100:
    score = 100

return score
```

# -------- Job Roles --------

job_roles = {
"Data Scientist": ["python","machine learning","pandas","numpy","statistics"],
"Machine Learning Engineer": ["python","machine learning","tensorflow","deep learning"],
"Data Analyst": ["excel","sql","power bi","tableau","data analysis"]
}

# -------- Job Recommendation --------

def recommend_job(skills):

```
recommendations = []

for role, role_skills in job_roles.items():

    match = 0

    for skill in role_skills:
        if skill in skills:
            match += 1

    if match >= 2:
        recommendations.append(role)

return recommendations
```

# -------- Skill Gap --------

def skill_gap(skills):

```
important_skills = [
    "python","machine learning","sql",
    "pandas","numpy","deep learning"
]

missing = []

for skill in important_skills:
    if skill not in skills:
        missing.append(skill)

return missing
```

# -------- Resume Tips --------

def resume_tips(score):

```
tips = []

if score < 40:
    tips.append("Add more technical skills")
    tips.append("Include data science projects")

elif score < 70:
    tips.append("Add machine learning projects")
    tips.append("Include visualization tools like Tableau")

else:
    tips.append("Your resume is strong")
    tips.append("Add advanced AI projects")

return tips
```

# -------- Resume Feedback --------

def resume_feedback(skills):

```
feedback = []

if "python" not in skills:
    feedback.append("Add Python skill")

if "machine learning" not in skills:
    feedback.append("Add Machine Learning projects")

if "sql" not in skills:
    feedback.append("SQL is important for data roles")

if not feedback:
    feedback.append("Your resume contains strong data skills")

return feedback
```

# -------- Skill Chart --------

def skill_chart(skills):

```
values = [1]*len(skills)

fig, ax = plt.subplots()

ax.bar(skills, values)

plt.xticks(rotation=45)

st.pyplot(fig)
```

# -------- Streamlit UI --------

st.title("AI Powered Smart Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:

```
st.success("Resume Uploaded Successfully")

resume_text = extract_resume_text(uploaded_file)

email = extract_email(resume_text)
phone = extract_phone(resume_text)
skills = extract_skills(resume_text)

st.subheader("Extracted Information")

st.write("Email:", email)
st.write("Phone:", phone)

st.subheader("Skills Found")

if skills:
    for skill in skills:
        st.write("✔", skill)
else:
    st.write("No skills detected")


score = calculate_resume_score(skills)

st.subheader("Resume Score")
st.progress(score)
st.write(score, "/100")


ats = ats_score(skills)

st.subheader("ATS Score")
st.progress(ats)
st.write(ats, "/100")


jobs = recommend_job(skills)

st.subheader("Recommended Jobs")

if jobs:
    for job in jobs:
        st.write("✔", job)
else:
    st.write("No matching roles found")


missing = skill_gap(skills)

st.subheader("Skills To Learn")

for skill in missing:
    st.write("➜", skill)


tips = resume_tips(score)

st.subheader("Resume Improvement Tips")

for tip in tips:
    st.write("✔", tip)


st.subheader("Skill Visualization")

skill_chart(skills)


feedback = resume_feedback(skills)

st.subheader("Resume Feedback")

for f in feedback:
    st.write("➜", f)
```
