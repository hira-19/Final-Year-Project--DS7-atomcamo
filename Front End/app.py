
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import google.generativeai as genai
import tempfile

origins = [
    "http://127.0.0.1:5500",  
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = 'AIzaSyDX4BVqmb47ercCZ6Epqz8ZCqnG3NocBUQ'
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

system_prompt = """
You are a medical Visual Question Answering (VQA) assistant designed for clinical purposes. Your role is to analyze input medical images, such as X-rays, MRIs, CT scans, and other diagnostic reports, and provide accurate, concise, and contextually relevant answers to doctors' questions. Your responses should:

Diagnosis: Accurately interpret the input image to identify potential medical conditions or abnormalities.
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

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction=system_prompt,
)

@app.get('/')
def index():
    return {"message": "Welcome to Medical Assistance VQA"}

@app.post("/analyze")
async def analyze(file: UploadFile, query: str = Form(...)):
    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Upload file to Google Gemini (assuming 'upload_file' works this way)
        gemini_file = genai.upload_file(temp_file_path)

        # Start a chat session with the provided query
        chat_session = model.start_chat(
            history=[{
                "role": "user",
                "parts": [gemini_file, query],
            }]
        )
        response = chat_session.send_message(query)
        
        # Return the response from the chat
        return {"answer": response.text}

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

