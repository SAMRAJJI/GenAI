import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai
from dotenv import load_dotenv
import os
from ui import load_css, show_header, get_inputs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

genai.configure(api_key=os.getenv('google_api_key'))

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
    