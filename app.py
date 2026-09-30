import streamlit as st
import pandas as pd

from src.resume_parser import extract_text_from_pdf
from src.matcher import calculate_skill_match
from src.ai_matcher import calculate_ai_similarity
from src.recruiter_assistant import recruiter_query


def generate_candidate_summary(
    matched_skills,
    missing_skills,
    percentage,
    ai_percentage
):
    if matched_skills:
        matched_text = ", ".join(matched_skills)
    else:
        matched_text = "No specific matching skills found"

    if missing_skills:
        missing_text = ", ".join(missing_skills)
    else:
        missing_text = "No major skill gaps detected"

    summary = f"""
Skill Match: {percentage}%

AI Semantic Match: {ai_percentage}%

Matched Skills:
{matched_text}

Skill Gaps:
{missing_text}

The candidate should be further evaluated by a human recruiter
based on experience, education, projects and other job-specific
requirements.
"""

    return summary


# Page configuration
st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Based Recruitment Assistant Agent")

st.write(
    "AI-powered assistant for resume analysis and job-description matching."
)

st.divider()


# Resume upload
st.header("1. Upload Candidate Resumes")

resume_files = st.file_uploader(
    "Upload Candidate Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)


# Job description
st.header("2. Enter Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=250
)


# Analyze button
analyze_button = st.button(
    "🔍 Analyze Candidates"
)


if analyze_button:

    if not resume_files:

        st.warning(
            "Please upload at least one resume PDF."
        )

    elif not job_description.strip():

        st.warning(
            "Please enter a job description."
        )

    else:

        candidate_results = []

        progress = st.progress(0)

        total_candidates = len(resume_files)

        for index, resume_file in enumerate(
            resume_files,
            start=1
        ):

            with st.spinner(
                f"Analyzing Candidate {index}..."
            ):

                # Extract resume text
                resume_text = extract_text_from_pdf(
                    resume_file
                )

                # Skill-based matching
                (
                    percentage,
                    resume_skills,
                    job_skills,
                    matched_skills,
                    missing_skills
                ) = calculate_skill_match(
                    resume_text,
                    job_description
                )

                # AI semantic matching
                ai_percentage = calculate_ai_similarity(
                    resume_text,
                    job_description
                )

                # Candidate summary
                candidate_summary = generate_candidate_summary(
                    matched_skills,
                    missing_skills,
                    percentage,
                    ai_percentage
                )

                # Store result
                candidate_results.append(
                    {
                        "Candidate": resume_file.name,
                        "Skill Match (%)": percentage,
                        "AI Semantic Match (%)": ai_percentage,
                        "Matched Skills": ", ".join(
                            matched_skills
                        ),
                        "Missing Skills": ", ".join(
                            missing_skills
                        )
                    }
                )

                progress.progress(
                    index / total_candidates
                )

        st.success(
            "All candidates analyzed successfully!"
        )

        st.divider()

        # Comparison table
        st.header("📊 Candidate Comparison")

        results_df = pd.DataFrame(
            candidate_results
        )

        st.dataframe(
            results_df,
            use_container_width=True
        )

        st.divider()

        # Individual candidate details
        st.header("👤 Candidate Details")

        for index, resume_file in enumerate(
            resume_files,
            start=1
        ):

            result = candidate_results[index - 1]

            with st.expander(
                f"Candidate {index} - {resume_file.name}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "📄 Resume Information"
                    )

                    resume_text = extract_text_from_pdf(
                        resume_file
                    )

                    st.write(
                        resume_text[:3000]
                    )

                with col2:

                    st.subheader(
                        "📊 Match Analysis"
                    )

                    st.metric(
                        "Skill Match",
                        f"{result['Skill Match (%)']}%"
                    )

                    st.metric(
                        "🤖 AI Semantic Match",
                        f"{result['AI Semantic Match (%)']}%"
                    )

                    st.subheader(
                        "✅ Matched Skills"
                    )

                    if result["Matched Skills"]:

                        for skill in result[
                            "Matched Skills"
                        ].split(", "):

                            st.success(skill)

                    else:

                        st.write(
                            "No matching skills found."
                        )

                    st.subheader(
                        "⚠️ Skill Gaps"
                    )

                    if result["Missing Skills"]:

                        for skill in result[
                            "Missing Skills"
                        ].split(", "):

                            st.warning(skill)

                    else:

                        st.success(
                            "No major skill gaps detected."
                        )

                st.divider()

                st.subheader(
                    "🤖 Candidate Summary"
                )

                st.write(
                    generate_candidate_summary(
                        result["Matched Skills"].split(", ")
                        if result["Matched Skills"]
                        else [],
                        result["Missing Skills"].split(", ")
                        if result["Missing Skills"]
                        else [],
                        result["Skill Match (%)"],
                        result["AI Semantic Match (%)"]
                    )
                )


st.divider()

st.info(
    "This AI tool provides recruitment assistance only. "
    "Final hiring decisions should be made by a human recruiter."
)
st.divider()

st.header("💬 AI Recruiter Assistant")

st.write(
    "Ask questions about the analyzed candidates."
)

recruiter_query_text = st.text_input(
    "Enter your question"
)

ask_button = st.button(
    "🤖 Ask Recruiter Assistant"
)

if ask_button:

    if not recruiter_query_text.strip():

        st.warning(
            "Please enter a question."
        )

    elif "candidate_results" not in locals():

        st.warning(
            "Please analyze candidates first."
        )

    else:

        results = recruiter_query(
            recruiter_query_text,
            candidate_results
        )

        if results:

            st.success(
                "Candidates found:"
            )

            for candidate in results:

                st.write(
                    f"👤 {candidate}"
                )

        else:

            st.info(
                "No matching candidates found."
            )
            st.divider()

st.header("📈 Recruitment Insights Dashboard")

if "candidate_results" in locals() and candidate_results:

    total_candidates = len(candidate_results)

    average_skill_match = sum(
        candidate["Skill Match (%)"]
        for candidate in candidate_results
    ) / total_candidates

    average_ai_match = sum(
        candidate["AI Semantic Match (%)"]
        for candidate in candidate_results
    ) / total_candidates

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👥 Total Candidates",
            total_candidates
        )

    with col2:
        st.metric(
            "📊 Average Skill Match",
            f"{average_skill_match:.2f}%"
        )

    with col3:
        st.metric(
            "🤖 Average AI Match",
            f"{average_ai_match:.2f}%"
        )

    st.subheader("📋 Candidate Skill Information")

    for candidate in candidate_results:

        st.write(
            f"**{candidate['Candidate']}**"
        )

        if candidate["Matched Skills"]:

            st.write(
                "✅ Matched: "
                + candidate["Matched Skills"]
            )

        if candidate["Missing Skills"]:

            st.write(
                "⚠️ Skill Gaps: "
                + candidate["Missing Skills"]
            )

else:

    st.info(
        "Analyze candidates first to view recruitment insights."
    )