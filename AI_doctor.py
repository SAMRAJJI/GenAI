import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
from PIL import Image
import io
genai.configure(api_key = os.getenv("google_api_key"))
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-3-flash-preview")
    res = model.generate_content([input_prompt, image[0]])
    
    return res.text


def image_setup(uploaded_file):
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        byte_data = io.BytesIO()
        img.save(byte_data, format='JPEG')
        raw_bytes = byte_data.getvalue()
        image_part = [
            {
                "mime_type" : uploaded_file.type,
                "data" : raw_bytes
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("Not file uploaded")
    
st.set_page_config(page_title="calories advisor APP")
st.header("Gemini Health App")

file = st.file_uploader("upload the image", type=["jpg", "jpeg"])
image = ""
if file is not None:
    image = Image.open(file)
    st.image(image,caption="uploaded Image", width="stretch")
    
submit = st.button("tell me about the total calories")

input_prompt = """You are an expert nutritionist. Analyze the uploaded food image and identify all visible food items.
Estimate the portion size and calories for each food item, then calculate the total calories.
Provide the output in this format: Item 1 - calories, Item 2 - calories, etc.
Also provide estimated protein, carbohydrates, fats, fiber, and sugar for the complete meal.
Finally, state whether the meal is generally healthy or unhealthy and briefly explain why.
Clearly mention that all nutritional values are estimates based only on the image and visible portion sizes.
"""


if submit:
    val = image_setup(file)
    out = get_gemini_response(input_prompt, val)
    st.write(out)
        