# Import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
import tempfile
from googletrans import Translator  # For translation
from gtts import gTTS  # For text-to-speech
import os

from api_key import api_key

# Configure Google GenAI with API key
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_prompt = """
You are a medical Visual Question Answering (VQA) assistant designed for clinical purposes. Your role is to analyze input medical images, such as X-rays, MRIs, CT scans, and other diagnostic reports, and provide accurate, concise, and contextually relevant answers to doctors' questions. Your responses should:

Diagnoses: Accurately interpret the input image to identify potential medical conditions or abnormalities.
Treatment: Suggest evidence-based treatment plans related to the diagnosed condition.
Further Tests: Recommend additional diagnostic tests if necessary for a comprehensive evaluation.
Medications: Propose suitable medications based on the diagnosis, ensuring adherence to medical guidelines.
Other Questions: Provide explanations or insights on other related medical queries.
Constraints:

Respond only within the scope of the provided medical image and question.
Use accessible and professional medical terminology. Avoid speculation and refer to established clinical guidelines.
Indicate when additional context or input is required for a more accurate response.

Input Format:
An image file (X-ray, MRI, CT scan, or medical report).
A specific question from the doctor.

Output Format:
Provide a structured, precise, and actionable response tailored to the question and input image.
"""

# Initialize the Generative AI model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction=system_prompt
)

# Upload file to GenAI
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Translation and TTS function with playback and download link
def translate_and_speak(text, language_code):
    """Translate text into the specified language and generate speech."""
    translator = Translator()
    translated = translator.translate(text, dest=language_code)
    translated_text = translated.text

    # Generate TTS audio in the translated language
    tts = gTTS(translated_text, lang=language_code)
    file_path = "translated_response.mp3"
    tts.save(file_path)

    # Provide download link for fallback
    st.audio(file_path, format="audio/mp3")
    st.success("Audio ready! You can play it directly or download it.")

    # Try to play the saved audio file
    try:
        if os.name == "nt":  # Windows
            os.system(f"start {file_path}")
        elif os.name == "posix":  # macOS/Linux
            os.system(f"afplay {file_path}" if "darwin" in os.uname().sysname.lower() else f"mpg123 {file_path}")
    except Exception as e:
        st.error(f"Could not play audio automatically: {e}")

    return translated_text


st.subheader('An application to assist doctors in diagnosing diseases by analyzing medical reports including X-rays, MRI, CT-scans, and other medical images.')

# Language selection dropdown
languages = {
    "English": "en",
    "Urdu" : 'ur',
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-cn",
    "Arabic": "ar"
}
language = st.selectbox("Select the language for response:", options=list(languages.keys()))

# File uploader and input
uploaded_file = st.file_uploader('Upload the medical image for analysis', type=['png', 'jpg', 'jpeg'])
input_prompt = st.text_input('Enter your query')
submit_button = st.button('Generate the Report')

# Store response in session state to persist across button clicks
if submit_button and uploaded_file:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    # Upload to Gemini
    file = upload_to_gemini(temp_file_path, mime_type=uploaded_file.type)

    # Start the chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    file,
                    input_prompt,
                ],
            }
        ]
    )
    response = chat_session.send_message(input_prompt)
    st.write(response.text)  # Display the response

    # Save the response in session state
    st.session_state["response"] = response.text

# Use the response stored in session state
if st.button('Play Response in Selected Language'):
    if "response" in st.session_state and st.session_state["response"]:
        translated_text = translate_and_speak(st.session_state["response"], languages[language])
        st.success(f"Response translated to {language}: {translated_text}")
    else:
        st.error("No response available to translate. Please generate the report first.")