from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("google_api_key"))


model = genai.GenerativeModel("gemini-2.5-flash")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

st.set_page_config(page_title = "Q & A Demo")
st.header("gemini LLM application")

input = st.text_input("Input: ", key="input")
submit = st.button("ask the question")

if submit:
    res = get_gemini_response(input)
    st.subheader("The Response is: ")
    st.write(res)