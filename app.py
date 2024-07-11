from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()  # Load my environment variable

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro Vision model
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    """
    Generates a response based on the input prompt and the uploaded invoice image.

    Args:
        input (str): The initial input context for the AI model.
        image (list): A list containing the image details.
        prompt (str): The question prompt input by the user.

    Returns:
        str: The generated response from the AI model.
    """
    response = model.generate_content([input, image[0], prompt])
    return response.text

def image_details(uploaded_file):
    """
    Processes the uploaded image file and returns its details.

    Args:
        uploaded_file (UploadedFile): The file uploaded by the user.

    Returns:
        list: A list containing the image's MIME type and byte data.

    Raises:
        FileNotFoundError: If no file is uploaded.
    """
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initialize Streamlit App
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Gemini Multi Language Invoice Extractor")

# Input prompt from the user
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Tell me about the Invoice")

# Initial input prompt for the AI model
input_prompt = """
You are an expert in understanding invoices. 
We will upload a image as invoice and you will 
have to answer any questions based on the uploaded 
invoice image.
"""

# If the Submit button is clicked
if submit:
    image_data = image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is: ")
    st.write(response)
