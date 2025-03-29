from dotenv import load_dotenv
load_dotenv()  # to load all the env variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## load gemini pro vision model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_respose(input,image,user_prompt):
    response = model.generate_content([input,image[0],user_prompt])  #when working with gemini-pro model 3 params can be passed as list
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



# make streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image="" 

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

# when user clicks submit
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_respose(input_prompt,image_data,input)
    st.subheader("The response is:")
    st.write(response)