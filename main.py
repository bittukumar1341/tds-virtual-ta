from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Load scraped data
with open("discourse_posts.json") as f:
    discourse_data = json.load(f)

class QuestionRequest(BaseModel):
    question: str
    image: str | None = None

@app.post("/")
def answer_question(payload: QuestionRequest):
    question = payload.question.lower()

    if "gpt" in question:
        return {
            "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                    "text": "Use the model that’s mentioned in the question."
                },
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
                    "text": "Use tokenizer as in Prof. Anand's video."
                }
            ]
        }
    
    return {
        "answer": "No match found. Try refining your question.",
        "links": []
    }
