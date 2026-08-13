from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("google_api_key"))

model = genai.GenerativeModel('gemini-2.5-flash')

def gemini_response(input, image, prompt):
    res = model.generate_content([input, image[0], prompt])
    return res.text

def image_setup(uploaded_file):
    
    if upload_file is not None:
        bytes_data= upload_file.getvalue()
        image_part = [{
            "mime_type": upload_file.type,
            "data": bytes_data
        }]
        return image_part
    else:
        raise FileNotFoundError("no file uploaded")
st.set_page_config(page_title = "Invoice AI extracter")

st.header("AI extractor")

input = st.text_input("input:" , key= "input")
upload_file = st.file_uploader("choose an image", type = ["jpg", "jpeg", "png"])
image = ""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption = "uploaded image", use_column_width = True)

submit = st.button("tell me about the invoice")
input_prompt = """
you are an expert in understand invoice. we will upload a image as invoice 
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = image_setup(upload_file)
    response = gemini_response(input, image_data, input_prompt)
    st.subheader("the response are")
    st.write(response)