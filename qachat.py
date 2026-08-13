import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("google_api_key"))

model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history = [])

def get_gemini_response(question):
    res = chat.send_message(question, stream = True)
    return res

st.set_page_config(page_title = "Q & A Demo")
st.header("Gemini LLM application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input = st.text_input("Input",key="input")
submit = st.button("ask the question")

if submit and input:
    res = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("the response is")
    for chunk in res:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("the chat history are")
for role, text, in st.session_state['chat_history']:
    st.write(f"{role}:{text}")