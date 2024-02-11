import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image


load_dotenv()


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response_image(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def get_gemini_response_text(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(["Give breif macros nutritional information about " + text +"and also tell breifly if its healthy or not and if not tell 1 or 2 alternate to eat in place of "+ text])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
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
    



st.set_page_config(page_title="KYC")

st.header("KYM(Know your Meal)")
# input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Upload an Image of your meal!", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

st.text("-----------------------OR------------------------------")

input=st.text_input("Ask about a specific Meal!!",key="input")


submit=st.button("Tell me the total calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the macro details of every food items with calories intake
               is below format that is protein in grams, carbohydrates in grams, fat in grams.s

               1. Item 1 - no of calories (Protein : "", Carbohydrates : "", Fat : "")
               2. Item 2 - no of calories
               ----
               ----

Tell me if its healthy and if not also advise on the healthy alternative replacement


"""

## If submit button is clicked

if submit:
    if uploaded_file:
        image_data=input_image_setup(uploaded_file)
        response=get_gemini_response_image(input_prompt,image_data)
        st.subheader("The Response is")
        st.write(response)
    else:
        response=get_gemini_response_text(input)
        st.subheader("The Response is")
        st.write(response)

