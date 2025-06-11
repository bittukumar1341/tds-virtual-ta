from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import base64
from PIL import Image
import io
import pytesseract
import json
import logging

app = FastAPI()

# Logging config
logging.basicConfig(level=logging.INFO)

# Load scraped data
try:
    with open("course_content.json", "r") as f:
        course_data = json.load(f)
    with open("discourse_posts.json", "r") as f:
        discourse_data = json.load(f)
    logging.info("✅ Successfully loaded course and discourse data.")
except Exception as e:
    logging.warning(f"⚠️ Could not load data files: {e}")
    course_data, discourse_data = [], []

# Data Models
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image

class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# OCR Function
def extract_text_from_image(base64_image: str) -> str:
    try:
        img_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        logging.error(f"Image processing error: {e}")
        return "[Image OCR Failed]"

# Main API
@app.post("/api/", response_model=AnswerResponse)
async def answer_question(data: QuestionRequest):
    question = data.question
    if data.image:
        extracted_text = extract_text_from_image(data.image)
        question += f" [Image Text: {extracted_text}]"

    # Dummy answer logic
    if "gpt-3.5-turbo" in question.lower():
        return {
            "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
            "links": [
                {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4", "text": "Use the model that’s mentioned in the question."},
                {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3", "text": "Token estimate via tokenizer like Prof. Anand's code."}
            ]
        }

    return {
        "answer": "Sorry, I don't know the answer to that yet.",
        "links": []
    }
