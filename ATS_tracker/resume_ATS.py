import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai
from dotenv import load_dotenv
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

genai.configure(api_key=os.getenv('google_api_key'))




def load_css():

    st.html("""
    <style>

        .stApp {
            background: #0e1117;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            text-align: center;
            padding: 30px 20px;
        }

        .hero-title {
            font-size: 42px;
            font-weight: 800;
            color: white;
        }

        .hero-title span {
            color: #7c3aed;
        }

        .hero-subtitle {
            color: #9ca3af;
            font-size: 17px;
        }

        .card {
            background: #171a21;
            border: 1px solid #292e39;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }

        .card-title {
            font-size: 20px;
            font-weight: 700;
            color: white;
            margin-bottom: 8px;
        }

        .card-description {
            color: #8b93a1;
            font-size: 14px;
        }

        .section-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #7c3aed;
            color: white;
            font-weight: 700;
            margin-right: 10px;
        }

        .stButton > button {
            width: 100%;
            height: 52px;
            border-radius: 10px;
            border: none;
            background: #7c3aed;
            color: white;
            font-size: 16px;
            font-weight: 700;
        }

        .stButton > button:hover {
            background: #6d28d9;
            color: white;
        }

    </style>
    """)


def show_header():

    st.html("""
    <div class="hero">

        <div style="font-size:45px;">📄</div>

        <div class="hero-title">
            Smart <span>ATS</span> Tracker
        </div>

        <div class="hero-subtitle">
            Analyze your resume against a job description
            and improve your ATS compatibility.
        </div>

    </div>
    """)


def get_inputs():

    col1, col2 = st.columns([1.3, 0.7], gap="large")

    with col1:

        st.html("""
        <div class="card">

            <div class="card-title">
                <span class="section-number">1</span>
                Job Description
            </div>

            <div class="card-description">
                Paste the job description you are applying for.
            </div>

        </div>
        """)

        jd = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the job description here...",
            label_visibility="collapsed",
            key="job_description"
        )

    with col2:

        st.html("""
        <div class="card">

            <div class="card-title">
                <span class="section-number">2</span>
                Upload Resume
            </div>

            <div class="card-description">
                Upload your resume in PDF format.
            </div>

        </div>
        """)

        resume = st.file_uploader(
            "Upload Resume",
            type=["pdf"],
            label_visibility="collapsed",
            key="resume_uploader"
        )

        if resume:
            st.success(f"✓ {resume.name}")

    st.markdown("<br>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.5, 1])

    with center:

        submit = st.button(
            "🚀 Analyze My Resume",
            use_container_width=True,
            key="analyze_resume"
        )

    return jd, resume, submit




def gemini_response(input):
    model = genai.GenerativeModel('gemini-2.5-flash')
    res = model.generate_content(input)
    return res.text

def input_pdf(upload_file):
    reader = pdf.PdfReader(upload_file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text())
    return text

input_prompt = """
Act like an expert ATS (Applicant Tracking System) and professional technical recruiter with deep knowledge of software engineering, data science, data analytics, AI/ML, cloud computing, and big data engineering.

Your task is to analyze the candidate's resume against the given job description.

The job market is highly competitive, so evaluate the resume strictly and objectively. Do not give a high score simply because the resume contains many keywords. Only consider a skill as matched when there is meaningful evidence in the resume.

Analyze the following:

1. Calculate the percentage match between the resume and the job description.
2. Identify the most important keywords and technical skills required by the job description.
3. Identify which required keywords and skills are present in the resume.
4. Identify important missing keywords and skills.
5. Evaluate the relevance of the candidate's experience and projects to the job.
6. Evaluate education and certifications when relevant.
7. Identify weaknesses that could reduce the ATS score.
8. Give practical recommendations for improving the resume for this specific job.
9. Do not invent or assume any skills, experience, certifications, or qualifications that are not explicitly present in the resume.
10. Give greater importance to required skills than preferred or optional skills.

Important:

* JD Match must be a number between 0% and 100%.
* Do not use markdown.
* Do not add explanations outside the JSON.
* Do not create information that is not present in the resume.
* Prioritize important job requirements over generic keywords.
* MissingKeywords should contain only meaningful keywords that are actually required or strongly preferred by the job description.
  """

st.set_page_config(
    page_title="Smart ATS Tracker",
    page_icon="📄",
    layout="wide"
)

load_css()
show_header()
jd, upload_file, submit = get_inputs()

if submit:
    if upload_file is not None:
        data = input_pdf(upload_file)
        
        final_prompt = f"""
        {input_prompt}

        JOB DESCRIPTION:
        {jd}

        CANDIDATE RESUME:
        {data}
        """
        res = gemini_response(final_prompt)
        
        st.write(res)

