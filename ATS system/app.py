# from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import pdf2image
import io
import base64

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# load_dotenv(os.path.join(base_dir, ".env"))
# genai.configure(api_key=os.getenv("google_api_key"))


prompts = [
    """
    Analyze this resume. Give:
    1. Profile summary
    2. Key skills and strengths
    3. Weaknesses/improvements
    4. Project and experience quality
    5. ATS-friendliness
    6. Overall score /100

    Use only information present in the resume. Do not invent anything.

    RESUME:
    {resume_text}
    """,

    """
    Compare the resume with the Job Description and calculate a match score /100.

    Show:
    1. Matching skills
    2. Partial matches
    3. Missing requirements
    4. Experience/project relevance
    5. Overall match percentage and reason

    Do not invent skills not shown in the resume.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """,

    """
    Find important JD keywords missing or partially represented in the resume.

    Group into:
    - Technical skills
    - Tools/technologies
    - Responsibilities
    - Qualifications
    - Soft skills

    Show: Keyword | Importance | Missing/Partial.
    Give the top 10 important missing keywords.
    Do not recommend skills the candidate does not have.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """
]
def get_gemini_res(input, pdf_content, prompt):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    model = genai.GenerativeModel('gemini-2.5-flash')
    res = model.generate_content([input, pdf_content[0],prompt])
    usage = res.usage_metadata
    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count
    total_tokens = usage.total_token_count
    return [res.text, input_tokens, output_tokens, total_tokens]


def input_pdf_setup(upload_file):
    if upload_file is not None:
        image = pdf2image.convert_from_bytes(upload_file.read())
        first = image[0]
        
        img_byte = io.BytesIO()
        first.save(img_byte, format='JPEG')
        img_byte = img_byte.getvalue()
        
        pdf_part = [{
            "mime_type" : "image/jpeg",
            "data" : base64.b64encode(img_byte).decode()
        }]
        
        return pdf_part
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS Expert system")
st.header("ATS tracking system")
api_key = st.text_input(
    "Gemini API Key",
    type="password"
)

if not api_key:
    st.info("Enter your Gemini API key to continue.")
    st.stop()
input_text = st.text_input("Job description", key="input")
uploaded_file = st.file_uploader("upload your resume(PDF)...", type=["pdf"])
if uploaded_file is not None:
    st.write("uploaded successfully")
    
submit1 = st.button("tell me about the resume")
submit2 = st.button("percentage match with JD")
submit3 = st.button("keywords missing in resume with JD")

if submit1:
    if uploaded_file is not None:
        input1 = input_pdf_setup(uploaded_file)
        res = get_gemini_res(input_text, input1, prompts[0])
        
        st.subheader("The response is")
        st.write(res[0])
        st.subheader("The usage of tokens are")
        st.write(f"Input tokens: {res[1]}")
        st.write(f"Output tokens: {res[2]}")
        st.write(f"Total tokens: {res[3]}")
        
    else:
        st.write("upload the resume")
elif submit2:
    if uploaded_file is not None:
        input1 = input_pdf_setup(uploaded_file)
        res = get_gemini_res(input_text, input1, prompts[1])
        st.subheader("The response is")
        st.write(res[0])
        st.subheader("The usage of tokens are")
        st.write(f"Input tokens: {res[1]}")
        st.write(f"Output tokens: {res[2]}")
        st.write(f"Total tokens: {res[3]}")
    else:
        st.write("upload the resume")
elif submit3:
    if uploaded_file is not None:
        input1 = input_pdf_setup(uploaded_file)
        res = get_gemini_res(input_text, input1, prompts[2])
        
        st.subheader("The response is")
        st.write(res[0])
        st.subheader("The usage of tokens are")
        st.write(f"Input tokens: {res[1]}")
        st.write(f"Output tokens: {res[2]}")
        st.write(f"Total tokens: {res[3]}")
    else:
        st.write("upload the resume")
