# backend/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Encode image
def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# OpenAI client setup
client = OpenAI(
    base_url= "https://openrouter.ai/api/v1",
    api_key= os.getenv('OPENAI_API_KEY'))

@app.post("/analyze-cv")
async def analyze_cv(file: UploadFile = File(...)):
    contents = await file.read()
    base64_image = encode_image_to_base64(contents)

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://example.com",
            "X-Title": "CV Analyzer App",
        },
        model="google/gemma-3-12b-it:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this CV image and provide a summary of skills, experience, and improvements."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    )
    return {"response": completion.choices[0].message.content}
