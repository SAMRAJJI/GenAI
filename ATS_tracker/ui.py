import streamlit as st


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