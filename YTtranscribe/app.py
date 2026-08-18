import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
genai.configure(api_key=os.getenv('google_api_key'))
def extract_video_id(url):
    """Extract YouTube video ID from different YouTube URL formats."""

    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?&]+)",
        r"(?:youtube\.com/embed/)([^?&]+)",
        r"(?:youtube\.com/shorts/)([^?&]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None

def extract_transcript_details(url):
    try:
        video_id = extract_video_id(url)
        api = YouTubeTranscriptApi()
        transcript_text = api.fetch(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i.text
        return transcript
    except Exception as e:
        raise e

def generate_content(transcript, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    res= model.generate_content(prompt + transcript)
    return res.text
    
    
prompt = """
you are youtube video summarizer. you will be taking the transcript text and summarizing the entire video and providing the important summary
in points within 250 words. the transcript text will be appended here: 
"""

st.title(" Youtube transcript to detailed notes converter ")
yt_link = st.text_input("paste the link")

if yt_link:
    video_id = yt_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", width="stretch")
   
if st.button("get detailed notes"):
    transcript_text = extract_transcript_details(yt_link)
    if transcript_text:
        summary =  generate_content(transcript_text, prompt)
        st.write(summary)
        
