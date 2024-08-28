from dotenv import load_dotenv 

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="PrepareU")
st.header("Seminar/Interview QA helper")
input_text = st.text_area("Interview description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully\n")

submit1 = st.button("generate questions regarding project")
submit3 = st.button("challenge my skill set")


input_prompt1 = """
    You are an experienced interviewer and you are assigned to ask questions based on the project that submit.i need you to ask maximum 
    indepth questions regarding the project submitted
"""

input_prompt3 = """
You are a skilled interviewer  with a deep understanding on Data Structures and algorithm. 
Your task is to evaluate a computer science engineer. Ask questions from the  advanced level and then travel to basic level
. First, ask toght question and from the keyword of prevous question ask next question with deeper meaning on the context .generate 10 questions
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
