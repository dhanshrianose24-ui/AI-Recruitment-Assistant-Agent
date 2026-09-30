import re


SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "machine learning",
    "deep learning",
    "statistics",
    "data science",
    "data analysis",
    "git",
    "github",
    "communication",
    "problem solving",
    "teamwork",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "mongodb",
    "html",
    "css",
    "javascript",
    "react",
    "aws",
    "docker"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_skill_match(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = []

    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    if len(job_skills) > 0:

        percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100

    else:

        percentage = 0

    return (
        round(percentage, 2),
        resume_skills,
        job_skills,
        matched_skills,
        missing_skills
    )