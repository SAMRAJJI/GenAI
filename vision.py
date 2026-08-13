from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("google_api_key"))


model = genai.GenerativeModel("gemini-2.5-vision")
def get_gemini_response(input, image):
    if input !="":
        response = model.generate_content([input, image])

    else:
        response = model.generate_content([image])
    return response.text

st.set_page_config(page_title="image application")
st.header("gemini application")

input = st.text_input("Input: ", key="input")
uploaded_file = st.file_uploader("choose the image")
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "uploaded image")
submit = st.button("tell about the image")
if submit:
    res = get_gemini_response(input, image)
    st.subheader("the response is")
    st.write(res)